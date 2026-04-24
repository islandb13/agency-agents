import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_FILENAME = "vanguard_memory.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS strategies (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT NOT NULL,
    confidence      REAL NOT NULL,
    status          TEXT NOT NULL DEFAULT 'proposed',
    outcome         TEXT,
    revenue_cents   INTEGER NOT NULL DEFAULT 0,
    metadata        TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS impediments (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  TEXT NOT NULL,
    resource    TEXT NOT NULL,
    roi_impact  TEXT NOT NULL,
    resolved    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS cycles (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  TEXT NOT NULL,
    thought     TEXT NOT NULL,
    tool_name   TEXT,
    tool_input  TEXT,
    observation TEXT
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Memory:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.executescript(SCHEMA)

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def log_strategy(self, title: str, description: str, confidence: float,
                     metadata: dict | None = None) -> int:
        ts = _now()
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO strategies (created_at, updated_at, title, description, "
                "confidence, metadata) VALUES (?, ?, ?, ?, ?, ?)",
                (ts, ts, title, description, float(confidence),
                 json.dumps(metadata or {}, sort_keys=True)),
            )
            return cur.lastrowid

    def update_outcome(self, strategy_id: int, status: str, outcome: str,
                       revenue_cents: int = 0) -> None:
        with self._conn() as c:
            c.execute(
                "UPDATE strategies SET status=?, outcome=?, revenue_cents=?, updated_at=? "
                "WHERE id=?",
                (status, outcome, int(revenue_cents), _now(), strategy_id),
            )

    def recent_strategies(self, limit: int = 20) -> list[dict]:
        with self._conn() as c:
            rows = c.execute(
                "SELECT * FROM strategies ORDER BY updated_at DESC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]

    def reflection_snapshot(self) -> dict:
        with self._conn() as c:
            totals = c.execute(
                "SELECT COUNT(*) AS n, COALESCE(SUM(revenue_cents), 0) AS rev "
                "FROM strategies"
            ).fetchone()
            by_status = c.execute(
                "SELECT status, COUNT(*) AS n, AVG(confidence) AS avg_conf "
                "FROM strategies GROUP BY status"
            ).fetchall()
            top = c.execute(
                "SELECT id, title, confidence, status, revenue_cents "
                "FROM strategies ORDER BY revenue_cents DESC, confidence DESC LIMIT 5"
            ).fetchall()
            stagnating = c.execute(
                "SELECT id, title, confidence, updated_at FROM strategies "
                "WHERE status IN ('proposed','in_progress') "
                "ORDER BY updated_at ASC LIMIT 5"
            ).fetchall()
            impediments = c.execute(
                "SELECT resource, roi_impact FROM impediments WHERE resolved = 0"
            ).fetchall()
        return {
            "total_strategies": totals["n"],
            "total_revenue_cents": totals["rev"],
            "by_status": [dict(r) for r in by_status],
            "top_performers": [dict(r) for r in top],
            "stagnating": [dict(r) for r in stagnating],
            "open_impediments": [dict(r) for r in impediments],
        }

    def log_impediment(self, resource: str, roi_impact: str) -> int:
        with self._conn() as c:
            cur = c.execute(
                "INSERT INTO impediments (created_at, resource, roi_impact) VALUES (?, ?, ?)",
                (_now(), resource, roi_impact),
            )
            return cur.lastrowid

    def log_cycle(self, thought: str, tool_name: str | None,
                  tool_input: dict | None, observation: str) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT INTO cycles (created_at, thought, tool_name, tool_input, observation) "
                "VALUES (?, ?, ?, ?, ?)",
                (_now(), thought, tool_name,
                 json.dumps(tool_input or {}, sort_keys=True), observation),
            )
