import re
from datetime import datetime, timezone
from pathlib import Path

AGENTS_DIR = Path(__file__).resolve().parent

TEMPLATE = '''"""
{name} - auto-generated Vanguard sub-agent.
Purpose: {purpose}
Created: {created_at}
"""
import os
from anthropic import Anthropic

SYSTEM_PROMPT = """{system_prompt}"""

KPI = {kpi!r}


def run(user_input: str, model: str | None = None) -> str:
    client = Anthropic()
    resp = client.messages.create(
        model=model or os.environ.get("VANGUARD_MODEL", "claude-opus-4-7"),
        max_tokens=8000,
        system=[{{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {{"type": "ephemeral"}}}}],
        messages=[{{"role": "user", "content": user_input}}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


if __name__ == "__main__":
    import sys
    print(run(sys.stdin.read() or "Report current status."))
'''


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9_]+", "_", name.lower()).strip("_")
    if not slug:
        raise ValueError("agent name produced empty slug")
    if not slug.isidentifier():
        slug = f"agent_{slug}"
    return slug


def spawn_subagent(name: str, purpose: str, system_prompt: str, kpi: str) -> dict:
    """Generate a new sub-agent .py file and return metadata.

    Security: name is slugified; arbitrary user text only enters the file as a
    Python triple-quoted string (escaped) or a repr()'d literal, never as code.
    """
    slug = _slugify(name)
    target = AGENTS_DIR / f"{slug}.py"
    if target.exists():
        return {
            "created": False,
            "reason": "file_exists",
            "path": str(target),
            "module": f"agents.{slug}",
        }

    safe_prompt = system_prompt.replace('"""', '\\"\\"\\"')
    rendered = TEMPLATE.format(
        name=name,
        purpose=purpose,
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        system_prompt=safe_prompt,
        kpi=kpi,
    )
    target.write_text(rendered, encoding="utf-8")
    return {
        "created": True,
        "path": str(target),
        "module": f"agents.{slug}",
        "kpi": kpi,
    }


def list_subagents() -> list[str]:
    return sorted(
        p.stem for p in AGENTS_DIR.glob("*.py")
        if p.name not in ("__init__.py", "manager.py")
    )
