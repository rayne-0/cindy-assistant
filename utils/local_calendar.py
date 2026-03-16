"""
Local Calendar — stores events in data/calendar.json.
Fully offline, no Google account needed.
"""
import os
import json
import datetime

CALENDAR_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'calendar.json')


def _load() -> list:
    if not os.path.exists(CALENDAR_PATH):
        return []
    try:
        with open(CALENDAR_PATH, 'r') as f:
            return json.load(f)
    except Exception:
        return []


def _save(events: list):
    os.makedirs(os.path.dirname(CALENDAR_PATH), exist_ok=True)
    with open(CALENDAR_PATH, 'w') as f:
        json.dump(events, f, indent=2)


def add_event(title: str, date_str: str = None, time_str: str = None) -> str:
    """
    Add a new calendar event.
    date_str: 'YYYY-MM-DD' or 'today' or 'tomorrow'. Defaults to today.
    time_str: 'HH:MM' (24h). Optional.
    """
    if date_str is None or date_str == "today":
        date = datetime.date.today().isoformat()
    elif date_str == "tomorrow":
        date = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    else:
        date = date_str

    events = _load()
    event = {"title": title, "date": date, "time": time_str or ""}
    events.append(event)
    events.sort(key=lambda e: (e["date"], e.get("time", "")))
    _save(events)
    time_part = f" at {time_str}" if time_str else ""
    return f"Event added: '{title}' on {date}{time_part}."


def get_todays_events() -> str:
    """Return a summary of today's events."""
    today = datetime.date.today().isoformat()
    events = [e for e in _load() if e.get("date") == today]
    if not events:
        return "You have nothing scheduled for today."
    lines = ["Here's your schedule for today:"]
    for e in events:
        t = f" at {e['time']}" if e.get("time") else ""
        lines.append(f"  - {e['title']}{t}")
    return "\n".join(lines)


def get_upcoming_events(days: int = 7) -> str:
    """Return events for the next N days."""
    today = datetime.date.today()
    future = today + datetime.timedelta(days=days)
    events = [
        e for e in _load()
        if today.isoformat() <= e.get("date", "") <= future.isoformat()
    ]
    if not events:
        return f"No events in the next {days} days."
    lines = [f"Upcoming events (next {days} days):"]
    for e in events:
        t = f" at {e['time']}" if e.get("time") else ""
        lines.append(f"  - {e['date']}: {e['title']}{t}")
    return "\n".join(lines)


def remove_event(title: str) -> str:
    """Remove an event by title (case-insensitive, partial match)."""
    events = _load()
    original_count = len(events)
    events = [e for e in events if title.lower() not in e.get("title", "").lower()]
    if len(events) == original_count:
        return f"No event found matching '{title}'."
    _save(events)
    return f"Removed event(s) matching '{title}'."
