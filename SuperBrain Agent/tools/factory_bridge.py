import json
import os
import shlex
import subprocess
import sys
from pathlib import Path


class FactoryBridgeError(RuntimeError):
    pass


def run_factory_build(args: dict, timeout: int = 600) -> dict:
    """Invoke the user's launch_build.py with a JSON argument blob.

    The target script receives two invocation shapes so it can pick whichever it supports:
      1. argv:  python launch_build.py --json '<serialized>'
      2. stdin: the same serialized JSON is piped in

    Returns a dict: {exit_code, stdout, stderr, artifact_paths}.
    `artifact_paths` is best-effort extracted from the last valid JSON line of stdout
    if the script prints one (e.g. {"artifact_paths": ["out/foo.pdf"]}).
    """
    script_path = os.environ.get("FACTORY_SCRIPT_PATH", "").strip()
    if not script_path:
        raise FactoryBridgeError(
            "FACTORY_SCRIPT_PATH is not set. Point it at your launch_build.py."
        )
    script = Path(script_path)
    if not script.exists():
        raise FactoryBridgeError(f"FACTORY_SCRIPT_PATH does not exist: {script}")

    payload = json.dumps(args, sort_keys=True)
    cmd = [sys.executable, str(script), "--json", payload]

    try:
        proc = subprocess.run(
            cmd,
            input=payload,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=script.parent,
        )
    except subprocess.TimeoutExpired as e:
        raise FactoryBridgeError(f"factory build timed out after {timeout}s: {e}") from e

    artifact_paths: list[str] = []
    for line in reversed(proc.stdout.splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "artifact_paths" in obj:
            artifact_paths = list(obj["artifact_paths"])
        break

    return {
        "command": " ".join(shlex.quote(c) for c in cmd),
        "exit_code": proc.returncode,
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-2000:],
        "artifact_paths": artifact_paths,
    }
