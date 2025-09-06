# Tkinter To-Do App

A modular To-Do application built with Python and Tkinter.

## Features

- CRUD tasks 

- Search and filter tasks

- Tkinter GUI for creating and managing tasks

- Mark/unmark as completed individually / all

- Automated reminder pop-up notifications

## Usage

Run the main GUI application (example):

```
python TKinter-to-do-app/ui/app.py
```

## Database

The project uses SQLite database files

- `tkinter_to_do_app.db`

## Development notes

- The code base separates UI, service, and data layer logic (look for `ui/`, `service/`, `dal/` directories). This promotes modularity and testability.

- There is an `AppState` utility (singleton) for centralized error/state tracking across the app.

## Dependencies

- Python 3.9+
- tkinter (standard library)
- sqlite3 (standard library)
