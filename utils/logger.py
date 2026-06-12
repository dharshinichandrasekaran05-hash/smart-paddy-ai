"""
utils/logger.py — Smart Paddy AI: Event Logger
Place at: smart_paddy_ai/utils/logger.py

Logs predictions and events to both JSON (legacy) and SQLite (new).
Provides helper functions for analytics queries.
"""

import os
import json
import sqlite3
import datetime
from contextlib import contextmanager

# ─────────────────────── PATHS ────────────────────────────────
LOG_DIR   = "data"
LOG_FILE  = os.path.join(LOG_DIR, "logs.json")
DB_PATH   = os.path.join(LOG_DIR, "paddy_ai.db")

os.makedirs(LOG_DIR, exist_ok=True)


# ─────────────────────── SQLITE SETUP ─────────────────────────
@contextmanager
def _get_conn():
    """Context manager for SQLite connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """
    Create database tables if they don't exist.
    Call once at app startup.
    """
    with _get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS predictions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp   TEXT    NOT NULL,
                disease     TEXT    NOT NULL,
                confidence  REAL    NOT NULL,
                severity    REAL    DEFAULT 0,
                health_idx  REAL    DEFAULT 0,
                location    TEXT    DEFAULT '',
                image_path  TEXT    DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS events (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp   TEXT    NOT NULL,
                event_type  TEXT    NOT NULL,
                data        TEXT    NOT NULL
            );
        """)


# ─────────────────────── LOG FUNCTIONS ────────────────────────
def log_event(event_type: str, data: dict) -> None:
    """
    Log a generic event to both JSON file and SQLite.

    Parameters
    ----------
    event_type : str — e.g. "prediction", "chatbot_query", "report_download"
    data       : dict — arbitrary payload
    """
    ts = str(datetime.datetime.now())

    # ── JSON fallback ──
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
        logs.append({"time": ts, "event": event_type, "data": data})
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception:
        pass

    # ── SQLite ──
    try:
        init_db()
        with _get_conn() as conn:
            conn.execute(
                "INSERT INTO events (timestamp, event_type, data) VALUES (?, ?, ?)",
                (ts, event_type, json.dumps(data, ensure_ascii=False))
            )
    except Exception:
        pass


def log_prediction(
    disease:    str,
    confidence: float,
    severity:   float = 0.0,
    health_idx: float = 0.0,
    location:   str   = "",
) -> None:
    """
    Log a disease prediction to SQLite predictions table.
    Also calls log_event for JSON compatibility.
    """
    ts = str(datetime.datetime.now())

    init_db()
    with _get_conn() as conn:
        conn.execute(
            """INSERT INTO predictions
               (timestamp, disease, confidence, severity, health_idx, location)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (ts, disease, confidence, severity, health_idx, location)
        )

    log_event("prediction", {
        "disease":    disease,
        "confidence": confidence,
        "severity":   severity,
        "health_idx": health_idx,
    })


# ─────────────────────── ANALYTICS QUERIES ────────────────────
def get_all_predictions() -> list[dict]:
    """Return all predictions as a list of dicts (newest first)."""
    init_db()
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM predictions ORDER BY id DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def get_disease_counts() -> dict:
    """Return {disease_name: count} dict for analytics."""
    init_db()
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT disease, COUNT(*) as cnt FROM predictions GROUP BY disease"
        ).fetchall()
    return {r["disease"]: r["cnt"] for r in rows}


def get_monthly_trends() -> list[dict]:
    """Return monthly scan counts as list of {month, count}."""
    init_db()
    with _get_conn() as conn:
        rows = conn.execute(
            """SELECT strftime('%Y-%m', timestamp) AS month,
                      COUNT(*) AS count
               FROM predictions
               GROUP BY month
               ORDER BY month"""
        ).fetchall()
    return [dict(r) for r in rows]