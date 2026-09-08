#!/usr/bin/env python3
"""Build a normalized SQLite database from the event JSON fixture.

Usage:
  python scripts/events_db.py validate
  python scripts/events_db.py import
  python scripts/events_db.py export
"""

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / ".data"
EVENTS_JSON = DATA / "events.json"
DB = DATA / "events.db"
SCHEMA = DATA / "schema.sql"


def load_events():
    data = json.loads(EVENTS_JSON.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("events.json must be a JSON array")
    for i, event in enumerate(data, 1):
        for key in ("date", "title", "venue"):
            if not event.get(key):
                raise ValueError(f"event #{i}: missing {key}")
    return data


def event_id(event, index):
    return event.get("id") or f"event-{event['date']}-{index:04d}"


def venue_id(name):
    import hashlib
    return "venue-" + hashlib.sha1(name.encode("utf-8")).hexdigest()[:12]


def build_db(events):
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))

    for index, event in enumerate(events, 1):
        eid = event_id(event, index)
        venue_name = event["venue"]
        vid = venue_id(venue_name)
        conn.execute("INSERT OR IGNORE INTO venues(id,name) VALUES(?,?)", (vid, venue_name))

        budget = event.get("budget") or {}
        metadata = event.get("metadata") or {}
        total = budget.get("total_price")
        admission = budget.get("admission_price")
        drink = budget.get("drink_price")
        if total is None and admission is not None and drink is not None:
            total = admission + drink
        if total is None:
            status = "unknown"
        elif total < 1000:
            status = "under"
        else:
            status = "over"

        conn.execute(
            """INSERT INTO events
            (id,date,start_at,end_at,title,venue_id,admission_price,drink_price,
             total_price,budget_status,reservation_required,note,source_url,fetched_at)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                eid, event["date"], event.get("start"), event.get("end"),
                event["title"], vid, admission, drink, total, status,
                int(bool(event.get("reservation_required"))), event.get("note"),
                event.get("source_url"), metadata.get("checked_at"),
            ),
        )

        for artist in event.get("artists", []):
            aid = "artist-" + __import__("hashlib").sha1(artist.encode("utf-8")).hexdigest()[:12]
            conn.execute("INSERT OR IGNORE INTO artists(id,name) VALUES(?,?)", (aid, artist))
            conn.execute("INSERT OR IGNORE INTO event_artists(event_id,artist_id) VALUES(?,?)", (eid, aid))

        if event.get("source_url"):
            conn.execute(
                "INSERT OR IGNORE INTO sources(event_id,url,source_type,checked_at,confidence) VALUES(?,?,?,?,?)",
                (eid, event["source_url"], metadata.get("source_type"), metadata.get("checked_at"), metadata.get("confidence")),
            )

    conn.commit()
    conn.close()


def validate():
    events = load_events()
    print(f"validated {len(events)} events")


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if command == "validate":
        validate()
    elif command == "import":
        events = load_events()
        build_db(events)
        print(f"imported {len(events)} events into {DB}")
    elif command == "export":
        # Export is intentionally a no-op for now: events.json remains the canonical fixture.
        # This keeps the current Vue app stable while SQLite becomes a normalized build artifact.
        events = load_events()
        print(f"export source remains {EVENTS_JSON} ({len(events)} events)")
    else:
        raise SystemExit(f"unknown command: {command}")


if __name__ == "__main__":
    main()
