import json
import os

NOTES_FILE = "data/notes.json"


def load_notes():

    if not os.path.exists(NOTES_FILE):
        return []

    try:
        with open(NOTES_FILE, "r") as f:
            data = f.read().strip()

            if not data:
                return []

            return json.loads(data)

    except Exception:
        return []


def save_notes(notes):

    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)


def add_note(note):

    notes = load_notes()

    notes.append(note)

    save_notes(notes)


def get_notes():

    return load_notes()