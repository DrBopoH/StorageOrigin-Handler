from typing import Type, Tuple, List, Dict 
import pytest, os


EXISTS_FILEPATHS: Tuple[str, ...] = (
	'tests/test.json',
	'tests/empty.json',
	'tests/test_unvalid.json'
)

UNEXISTS_FILEPATHS: Tuple[str, ...] = (
	'tests/abracadabra.db',
	'tests/fedora64.iso',
	'tests/test.db'
)

UNVALID_FILEPATHS: Tuple[tuple[str, Type[Exception], str], ...] = (
	(f'tests/{'very'*2000}longfile.txt', OSError, f"{'[Errno 22] Invalid argument' if os.name == 'nt' else '[Errno 36] File name too long'}: 'tests/{'very'*2000}longfile.txt'"),
	('nonexistent_directory/file.txt', FileNotFoundError, "[Errno 2] No such file or directory: 'nonexistent_directory/file.txt'"),
	('', OSError, "[Errno 2] No such file or directory: ''")
)

DELETED_FILEPATHS: Tuple[str, ...] = (
	'tests/test.txt', 
	'tests/note.md'
)

JSON_EXAMPLES: Tuple[Dict, ...] = (
	{
		"widget": {
			"debug": "on",
			"window": {
				"title": "Sample Konfabulator Widget",
				"name": "main_window",
				"width": 500,
				"height": 500
			},
			"image": { 
				"src": "Images/Sun.png",
				"name": "sun1",
				"hOffset": 250,
				"vOffset": 250,
				"alignment": "center"
			},
			"text": {
				"data": "Click Here",
				"size": 36,
				"style": "bold",
				"name": "text1",
				"hOffset": 250,
				"vOffset": 100,
				"alignment": "center",
				"onMouseUp": "sun1.opacity = (sun1.opacity / 100) * 90;"
			}
		}
	},
	{
		"menu": {
			"header": "SVG Viewer",
			"items": [
				{"id": "Open"},
				{"id": "OpenNew", "label": "Open New"},
				{"id": "ZoomIn", "label": "Zoom In"},
				{"id": "ZoomOut", "label": "Zoom Out"},
				{"id": "OriginalView", "label": "Original View"},
				{"id": "Quality"},
				{"id": "Pause"},
				{"id": "Mute"},
				{"id": "Find", "label": "Find..."},
				{"id": "FindAgain", "label": "Find Again"},
				{"id": "Copy"},
				{"id": "CopyAgain", "label": "Copy Again"},
				{"id": "CopySVG", "label": "Copy SVG"},
				{"id": "ViewSVG", "label": "View SVG"},
				{"id": "ViewSource", "label": "View Source"},
				{"id": "SaveAs", "label": "Save As"},
				{"id": "Help"},
				{"id": "About", "label": "About Adobe CVG Viewer..."}
			]
		}
	},
	{
		"id":1,
		"age": 17,
		"username":"ivan",
		"email":"ivan777@gmail.com",
		"timecreated": "2024-03-22 12:00:00",
		"posts": {
			"my dog": {
				"id": 197,
				"content": "_vvv DOG vvv_",
				"timecreated": "2025-01-05 19:45:00"
			}
		}
	}
)

SQL_TEMPLATES: Tuple[Tuple[str, Tuple[Tuple[str, str], ...], Tuple[Tuple[str, str],	...], str], ...] = (
	(
		'users', 
		(
			('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'), 
			('username', 'TEXT UNIQUE NOT NULL'), 
			('email', 'TEXT UNIQUE NOT NULL'), 
			('created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
		), 
		(), 
		'CREATE TABLE IF NOT EXISTS users (\n\tid INTEGER PRIMARY KEY AUTOINCREMENT,\n\tusername TEXT UNIQUE NOT NULL,\n\temail TEXT UNIQUE NOT NULL,\n\tcreated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n)'
	),

	(
		'posts', 
		(
			('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'), 
			('user_id', 'INTEGER NOT NULL'), 
			('title', 'TEXT NOT NULL'), 
			('content', 'TEXT NOT NULL'), 
			('created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
		), 
		(
			('user_id', 'users(id)'),
		), 
		'CREATE TABLE IF NOT EXISTS posts (\n\tid INTEGER PRIMARY KEY AUTOINCREMENT,\n\tuser_id INTEGER NOT NULL,\n\ttitle TEXT NOT NULL,\n\tcontent TEXT NOT NULL,\n\tcreated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n\tFOREIGN KEY (user_id) REFERENCES users(id)\n)'
	),

	(
		'comments', 
		(
			('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'), 
			('post_id', 'INTEGER NOT NULL'), 
			('user_id', 'INTEGER NOT NULL'), 
			('text', 'TEXT NOT NULL'), 
			('created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
		), 
		(
			('post_id', 'posts(id)'),
			('user_id', 'users(id)')
		), 
		'CREATE TABLE IF NOT EXISTS comments (\n\tid INTEGER PRIMARY KEY AUTOINCREMENT,\n\tpost_id INTEGER NOT NULL,\n\tuser_id INTEGER NOT NULL,\n\ttext TEXT NOT NULL,\n\tcreated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n\tFOREIGN KEY (post_id) REFERENCES posts(id),\n\tFOREIGN KEY (user_id) REFERENCES users(id)\n)'
	)
)


@pytest.fixture(autouse=True, scope="session")
def fix_working_directory():
	root_dir = os.path.dirname(os.path.abspath(__file__))
	project_root = os.path.abspath(os.path.join(root_dir, ".."))
	os.chdir(project_root)

@pytest.fixture(autouse=True, scope='session')
def validate_required_files_exist():
	for path in EXISTS_FILEPATHS:
		assert os.path.exists(path), f"File <{path}> not found - possibly wrong working directory..."