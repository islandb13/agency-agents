"""Vanguard-1 Lead Architect - autonomous Thought -> Action -> Observation loop.

Run from inside the "SuperBrain Agent/" directory:
    python vanguard_main.py
Or use start_vanguard.sh for keep-alive supervision.
"""
import json
import logging
import os
import sys
import time
import traceback
from pathlib import Path

from anthropic import Anthropic, APIError, APIConnectionError, RateLimitError
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))  # ensure subpackages import when run directly

from brain.memory import Memory  # noqa: E402
from tools.factory_bridge import run_factory_build, FactoryBridgeError  # noqa: E402
from tools.research_suite import (  # noqa: E402
    research_reddit, research_github, ImpedimentNeeded,
)
from agents.manager import spawn_subagent, list_subagents  # noqa: E402

load_dotenv(BASE_DIR / ".env")

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
DB_PATH = BASE_DIR / "vanguard_memory.db"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "vanguard.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("vanguard")

MODEL = os.environ.get("VANGUARD_MODEL", "claude-opus-4-7")
REFLECTION_INTERVAL = int(os.environ.get("REFLECTION_INTERVAL", "5"))
MAX_CYCLES = int(os.environ.get("MAX_CYCLES", "0"))

SYSTEM_PROMPT = """You are Vanguard-1, the Lead Architect of an autonomous
revenue-generation system. Your singular mission is to generate $1,000,000 in
liquid capital through AI-driven micro-businesses.

CORE DIRECTIVES
1. Ruthless Profit Prioritization - only execute highest-velocity,
   lowest-overhead strategies.
2. Autonomous Execution - favor workflows needing <1% human intervention.
3. Data-Driven Logic - every recommendation must be backed by signals from
   the research tools (research_reddit, research_github). NEVER fabricate
   market data. If you need a source that requires a missing API key, call
   log_impediment instead of guessing.
4. Agentic Procreation - architect specialized Sub-Agents via spawn_subagent
   when a task falls outside PDF generation.

ELITE BEHAVIORS
- Recursive Optimization: every {interval} cycles the harness injects a
  reflection prompt containing the current memory snapshot. Analyze it,
  identify what is converting, kill stagnating strategies (update_outcome
  with status='killed'), and adjust future confidence scores.
- Asset Creation: the run_factory_build tool drives the user's existing
  launch_build.py engine. Treat it as your primary output vehicle for
  "Digital Gold" - niche PDFs with zero maintenance.
- Transparency: if a required API key is missing, call log_impediment with
  a precise ROI impact estimate. Do NOT fabricate data.
- Persistence: after any meaningful outcome, call log_strategy or
  update_strategy_outcome so future cycles can learn.

OPERATING LOOP
Each cycle follows Thought -> Action -> Observation. Keep thoughts concise.
Act through tools - never narrate an action without a tool call. When you
are finished for a cycle (strategy logged, build launched, impediment raised),
emit a short text block summarizing the cycle and stop.
""".format(interval=REFLECTION_INTERVAL)

# ---------------------------------------------------------------------------
# Tool schema - exposed to the model
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "log_strategy",
        "description": "Persist a new strategy under consideration. Use AFTER "
                       "research produces a concrete, actionable idea.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "confidence": {
                    "type": "number",
                    "description": "0.0 - 1.0 probability this strategy clears "
                                   "its revenue target within 30 days.",
                },
                "metadata": {"type": "object"},
            },
            "required": ["title", "description", "confidence"],
        },
    },
    {
        "name": "update_strategy_outcome",
        "description": "Update a previously logged strategy with execution "
                       "status and realized revenue.",
        "input_schema": {
            "type": "object",
            "properties": {
                "strategy_id": {"type": "integer"},
                "status": {
                    "type": "string",
                    "enum": ["in_progress", "shipped", "generating_revenue",
                             "stagnating", "killed"],
                },
                "outcome": {"type": "string"},
                "revenue_cents": {"type": "integer"},
            },
            "required": ["strategy_id", "status", "outcome"],
        },
    },
    {
        "name": "research_reddit",
        "description": "Scan a subreddit for pain points / unsolved problems.",
        "input_schema": {
            "type": "object",
            "properties": {
                "subreddit": {"type": "string"},
                "query": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "required": ["subreddit"],
        },
    },
    {
        "name": "research_github",
        "description": "Find repos created in the last N days sorted by stars "
                       "- a proxy for trending / market-asymmetry signals.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer"},
                "days": {"type": "integer"},
            },
        },
    },
    {
        "name": "run_factory_build",
        "description": "Invoke the user's launch_build.py PDF engine with a "
                       "JSON argument blob. Returns exit_code, stdout tail, "
                       "and artifact_paths if the script emits them.",
        "input_schema": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "object",
                    "description": "JSON payload forwarded to launch_build.py "
                                   "via --json and stdin.",
                },
                "timeout": {"type": "integer"},
            },
            "required": ["args"],
        },
    },
    {
        "name": "spawn_subagent",
        "description": "Generate a new specialized Sub-Agent Python file when "
                       "a task falls outside PDF generation (e.g. SEO Agent).",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "purpose": {"type": "string"},
                "system_prompt": {"type": "string"},
                "kpi": {
                    "type": "string",
                    "description": "Single measurable KPI, e.g. "
                                   "'drive 1000 unique visitors/day'.",
                },
            },
            "required": ["name", "purpose", "system_prompt", "kpi"],
        },
    },
    {
        "name": "log_impediment",
        "description": "Record a missing API key / tool that is blocking a "
                       "strategy, with ROI impact. Use INSTEAD of fabricating "
                       "data when a research source is unavailable.",
        "input_schema": {
            "type": "object",
            "properties": {
                "resource": {"type": "string"},
                "roi_impact": {"type": "string"},
            },
            "required": ["resource", "roi_impact"],
        },
    },
]


def _tool_result(tool_use_id: str, data, is_error: bool = False) -> dict:
    return {
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "content": json.dumps(data, default=str)[:15000],
        "is_error": is_error,
    }


def dispatch_tool(name: str, args: dict, memory: Memory) -> tuple[dict, bool]:
    """Execute a tool call. Returns (payload, is_error)."""
    try:
        if name == "log_strategy":
            sid = memory.log_strategy(
                title=args["title"],
                description=args["description"],
                confidence=args["confidence"],
                metadata=args.get("metadata"),
            )
            return {"strategy_id": sid}, False

        if name == "update_strategy_outcome":
            memory.update_outcome(
                strategy_id=args["strategy_id"],
                status=args["status"],
                outcome=args["outcome"],
                revenue_cents=args.get("revenue_cents", 0),
            )
            return {"updated": args["strategy_id"]}, False

        if name == "research_reddit":
            return research_reddit(
                subreddit=args["subreddit"],
                query=args.get("query"),
                limit=args.get("limit", 25),
            ), False

        if name == "research_github":
            return research_github(
                query=args.get("query", "stars:>50"),
                limit=args.get("limit", 15),
                days=args.get("days", 14),
            ), False

        if name == "run_factory_build":
            return run_factory_build(
                args=args["args"],
                timeout=args.get("timeout", 600),
            ), False

        if name == "spawn_subagent":
            return spawn_subagent(
                name=args["name"],
                purpose=args["purpose"],
                system_prompt=args["system_prompt"],
                kpi=args["kpi"],
            ), False

        if name == "log_impediment":
            iid = memory.log_impediment(
                resource=args["resource"],
                roi_impact=args["roi_impact"],
            )
            return {"impediment_id": iid}, False

        return {"error": f"unknown tool: {name}"}, True

    except ImpedimentNeeded as e:
        memory.log_impediment(resource=e.resource, roi_impact=e.roi_impact)
        return {"impediment_auto_logged": {"resource": e.resource,
                                           "roi_impact": e.roi_impact}}, False
    except FactoryBridgeError as e:
        return {"error": f"factory_bridge: {e}"}, True
    except Exception as e:  # noqa: BLE001 - surface to model for self-correction
        return {"error": f"{type(e).__name__}: {e}",
                "traceback": traceback.format_exc(limit=3)}, True


def run_cycle(client: Anthropic, memory: Memory, messages: list,
              cycle_num: int) -> list:
    """Execute one full turn: model -> tool calls -> tool results -> model.
    Returns the updated message history."""
    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            output_config={"effort": "high"},
            system=[{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            tools=TOOLS,
            messages=messages,
        )

        thought_text = "".join(b.text for b in response.content if b.type == "text")
        log.info("[cycle %d] stop_reason=%s", cycle_num, response.stop_reason)
        if thought_text.strip():
            log.info("[cycle %d] %s", cycle_num, thought_text.strip()[:500])

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            memory.log_cycle(
                thought=thought_text,
                tool_name=None,
                tool_input=None,
                observation=f"stop_reason={response.stop_reason}",
            )
            return messages

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            log.info("[cycle %d] tool_use: %s", cycle_num, block.name)
            payload, is_error = dispatch_tool(block.name, block.input, memory)
            memory.log_cycle(
                thought=thought_text,
                tool_name=block.name,
                tool_input=dict(block.input),
                observation=json.dumps(payload, default=str)[:2000],
            )
            tool_results.append(_tool_result(block.id, payload, is_error))

        messages.append({"role": "user", "content": tool_results})


def inject_reflection(memory: Memory, messages: list) -> list:
    snapshot = memory.reflection_snapshot()
    messages.append({
        "role": "user",
        "content": (
            "RECURSIVE OPTIMIZATION CHECKPOINT.\n"
            "Here is the current memory snapshot:\n"
            f"{json.dumps(snapshot, indent=2, default=str)}\n\n"
            "Self-reflect: which strategies are converting? Which are stagnating? "
            "Kill what isn't working (update_strategy_outcome -> status='killed'), "
            "double down on winners, and propose the next highest-velocity move. "
            "Resolve any open impediments by choosing a workaround or logging a "
            "more specific request."
        ),
    })
    return messages


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY not set. See .env.example.")
        return 2

    memory = Memory(DB_PATH)
    client = Anthropic()

    log.info("Vanguard-1 starting. model=%s reflection_interval=%d "
             "subagents=%s", MODEL, REFLECTION_INTERVAL, list_subagents())

    messages = [{
        "role": "user",
        "content": (
            "Cycle 1 initialization. Current cash: $0. Goal: $1,000,000 liquid. "
            "Scan GitHub trending and one high-signal subreddit (e.g. "
            "r/Entrepreneur or r/SideProject) for a concrete market asymmetry "
            "you can exploit with a single PDF asset. Log the strategy with an "
            "honest confidence score, then either spawn a sub-agent or launch "
            "a factory build. If a key is missing, raise an Impediment Report "
            "and pivot to a source you CAN reach."
        ),
    }]

    cycle = 0
    while True:
        cycle += 1
        try:
            messages = run_cycle(client, memory, messages, cycle)
        except RateLimitError as e:
            wait = 60
            log.warning("rate limited; sleeping %ds: %s", wait, e)
            time.sleep(wait)
            continue
        except APIConnectionError as e:
            log.warning("API connection error; retrying in 15s: %s", e)
            time.sleep(15)
            continue
        except APIError as e:
            log.error("API error: %s", e)
            time.sleep(30)
            continue

        if cycle % REFLECTION_INTERVAL == 0:
            log.info("--- reflection checkpoint at cycle %d ---", cycle)
            messages = inject_reflection(memory, messages)

        if MAX_CYCLES and cycle >= MAX_CYCLES:
            log.info("MAX_CYCLES=%d reached; exiting.", MAX_CYCLES)
            return 0

        # Context hygiene: once the transcript balloons past ~40 turns, keep
        # the last 20 so prompt caching on the system block stays effective
        # while we don't blow past context limits.
        if len(messages) > 40:
            messages = messages[-20:]
            if messages and messages[0]["role"] != "user":
                messages.insert(0, {
                    "role": "user",
                    "content": "Continue from the last known state.",
                })


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log.info("interrupted by operator")
        sys.exit(130)
