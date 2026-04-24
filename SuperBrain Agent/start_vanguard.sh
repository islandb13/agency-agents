#!/usr/bin/env bash
# Keep-alive supervisor for Vanguard-1.
# - resolves its own directory (handles the space in "SuperBrain Agent")
# - activates a venv if present (.venv)
# - restarts on non-zero exit with capped exponential backoff
# - exits cleanly on Ctrl-C (SIGINT) or SIGTERM
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

LOG_DIR="$HERE/logs"
mkdir -p "$LOG_DIR"

if [ -f "$HERE/.venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source "$HERE/.venv/bin/activate"
fi

PY="${PYTHON:-python3}"

backoff=2
max_backoff=300

shutdown() {
    echo "[start_vanguard] caught signal, exiting."
    exit 0
}
trap shutdown INT TERM

while true; do
    ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "[start_vanguard] $ts launching vanguard_main.py"
    "$PY" "$HERE/vanguard_main.py" 2>&1 | tee -a "$LOG_DIR/supervisor.log"
    rc=${PIPESTATUS[0]}

    if [ "$rc" -eq 0 ]; then
        echo "[start_vanguard] clean exit; sleeping 5s then restarting."
        sleep 5
        backoff=2
        continue
    fi

    if [ "$rc" -eq 130 ]; then
        echo "[start_vanguard] interrupted (rc=130); stopping supervisor."
        exit 0
    fi

    echo "[start_vanguard] exit rc=$rc; backing off ${backoff}s"
    sleep "$backoff"
    backoff=$(( backoff * 2 ))
    [ "$backoff" -gt "$max_backoff" ] && backoff=$max_backoff
done
