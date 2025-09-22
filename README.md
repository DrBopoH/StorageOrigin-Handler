📦StorageOrigins, last release: v0.1a.8

StorageOrigins is a lightweight Python library that provides an extensible interface for working with file-based data origins such as plain text, JSON, and SQLite. It abstracts file/resource handling into clean, reusable classes for common storage use cases.

Features:
- 🔗 Unified API for different storage types (text, JSON, SQLite).
- 📄 NoteOrigin: Read, append, and replace plain-text content.
- 📑 JsonOrigin: Load and safely update JSON files with optional backup mode.
- 🗃️ SQLiteOrigin: Manage SQLite databases with support for:
	- Schema inspection
	- Record CRUD operations
	- Exporting/importing tables to/from JSON
	- Integrity checking and table creation with foreign keys

Ideal for:
- Tooling scripts
- Game save/load systems
- Simple local data management
- JSON↔SQL sync tools

Example usage:
```py
from StorageOrigin import JsonOrigin

with JsonOrigin("data.json") as j:
    data = j.load()
    data["new_key"] = "value"
    j.replace(data)

```