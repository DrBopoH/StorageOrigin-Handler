from typing import TextIO, Self, Tuple, List, Dict, Any
import sqlite3, copy, json, os




class StorageOrigin:
	'''Base class for file-based or resource-based storage systems.
    Provides basic functionality for mounting, opening, and managing file-like resources. 
    '''

	_filePath: str = ''	

	encoding: str = 'utf-8'


	def __enter__(self: Self) -> Self:
		return self.open()

	def open(self: Self) -> Self:
		'''Open origin if file on filePath exists.'''

		if not self.path_exists(): raise FileNotFoundError(f"{self}: File on path <{self._filePath}> not exists!")

		self._origin = open(self._filePath, 'r+', encoding=self.encoding)
		return self


	def __exit__(self: Self, exc_type, exc_value, traceback): 
		self.close()

	def close(self: Self):
		self._origin.close()



	def __init__(self: Self, filePath: str = ''):
		'''Initialize and mount origin on filePath.'''
		self.mount(filePath)



	def mount(self: Self, filePath: str):
		'''Mount origin if file on filePath exists.'''
		if self.path_exists(filePath): self._filePath = filePath

	def create_and_mount(self: Self, filePath: str):
		'''Create new file, if not exists on filePath, and mount origin on filePath.'''
		if not self.path_exists(filePath): open(filePath, 'w').close()

		self.mount(filePath)



	def path_exists(self: Self, filePath: str = '') -> bool:
		'''Checking whether file path exists.
		if path == '', checked self.path.
		'''

		if filePath == '': filePath = self._filePath

		if os.path.exists(filePath): return True
		
		print(f"{self}: File on path <{filePath}> not exists.")
		return False



	def __str__(self: Self) -> str:
		'''Return exists origin filePath.'''
		return self._filePath

	def __repr__(self: Self) -> str:
		'''Return origin class hex id.'''
		return f"<{self.__class__.__name__} object at {hex(id(self))}>"




class NoteOrigin(StorageOrigin):
	'''Storage origin specialized for plain-text note files.
    Provides methods to read, add, and replace text content.
    '''

	_origin: TextIO


	def get(self: Self) -> str:
		return self._origin.read()

	def add(self: Self, text: str, offset: int = 0):
		'''Append given text to note file.
		if offset <= 0, whence == os.SEEK_END.
		'''

		self._origin.seek(0 if offset <= 0 else offset, os.SEEK_END if offset <= 0 else os.SEEK_SET)
		self._origin.write(text)

		self._origin.flush()

	def replace(self: Self, text: str, offset: int = 0):
		'''Replace entire content of note file with given text.'''

		self._origin.seek(0 if offset <= 0 else offset)
		self._origin.write(text)

		self._origin.truncate()
		self._origin.flush()



class JsonOrigin(StorageOrigin):
	'''Storage origin for JSON-formatted files.
    Provides safe and unsafe replacement and parsing of structured JSON data.
    '''

	_origin: TextIO

	indentation: int = 4
	ensure_ascii: bool = False


	def load(self: Self) -> Dict[str, Any]:
		'''Load and return JSON content.'''
		if os.path.getsize(f'{self}') == 0: 
			raise ValueError(f"{self.__repr__()}: Error trying to get data with <{self}>, JSON file is empty")

		return json.load(self._origin)



	def _safereplace(self: Self, newData: Dict[str, Any]):
		'''Replace JSON content with backup safety measures.'''

		tempFile = copy.copy(self)
		tempFile.create_and_mount(f'{self}.tmp')

		try:
			with tempFile: tempFile.replace(newData, False)

		except (PermissionError, OSError, json.JSONDecodeError) as e:
			raise RuntimeError(f"{self.__repr__()}: Error trying to save data in <{self}>, error as: {e}")

		else:
			self.close()
			os.replace(str(tempFile), f'{self}')
			self.open()
		
		finally: 
			if os.path.exists(str(tempFile)): os.remove(str(tempFile))


	def replace(self: Self, newData: Dict[str, Any], safemode: bool = True):
		'''Replace the JSON content.
		Optionally unable safemode for more fast replacement.'''
		
		if safemode: self._safereplace(newData)
		else:
			json.dump(newData, self._origin, indent=self.indentation, ensure_ascii=self.ensure_ascii)
			self._origin.truncate()
			self._origin.flush()




class SQLiteOrigin(StorageOrigin):
	'''Storage origin for SQLite databases.
    Provides high-level operations on tables(pages), schema inspection, and integrity checks.
	'''

	_origin: sqlite3.Connection
	_cursor: sqlite3.Cursor


	def open(self: Self) -> Self:
		'''Open an SQLite database connection from filePath.'''

		if not self.path_exists(): raise FileNotFoundError(f"{self.__repr__()}: File on path <{self}> not exists!")
		
		self._origin = sqlite3.connect(f'{self}')
		self._cursor = self._origin.cursor()

		return self



	def check_integrity(self: Self) -> bool:
		'''Check integrity of SQLite database.'''
		self._cursor.execute("PRAGMA integrity_check;")
		result = self._cursor.fetchone()
		return result[0] == "ok"



	def get_pages(self: Self) -> List[str]: 
		'''Return list of all page(table) names in database.'''
		self._cursor.execute("PRAGMA table_list;")
		return [info[1] for info in self._cursor.fetchall()]


	def get_schema(self: Self, page_name: str) -> List[Tuple[str, str]]:
		'''Retrieve schema(column names and types) of specified page.'''
		self._cursor.execute(f"PRAGMA table_info({page_name})")
		return [(col[1], col[2]) for col in self._cursor.fetchall()]

	

	def insert_into_page(self: Self, page_name: str, data: Dict[str, Any]):
		'''Insert new record into specified page(table).'''

		keys = ", ".join(data.keys())
		values = ", ".join(["?"] * len(data))
		self._cursor.execute(f"INSERT INTO {page_name} ({keys}) VALUES ({values})", tuple(data.values()))
		self._origin.commit()


	def fetch_all(self: Self, page_name: str) -> List[Tuple]:
		'''Fetch all records from specified page(table).'''
		self._cursor.execute(f"SELECT * FROM {page_name}")
		return self._cursor.fetchall()


	def update_page(self: Self, page_name: str, update: Dict[str, Any], condition: str):
		'''Update records in page(table) using condition.'''

		set_expr = ", ".join([f"{k}=?" for k in update.keys()])
		self._cursor.execute(f"UPDATE {page_name} SET {set_expr} WHERE {condition}", tuple(update.values()))
		self._origin.commit()


	def delete_from_page(self: Self, page_name: str, condition: str):
		'''Delete records from page(table) that match condition.'''
		self._cursor.execute(f"DELETE FROM {page_name} WHERE {condition}")
		self._origin.commit()



	def generate_create_table_sql(self: Self, page_name: str, schema: Tuple[Tuple[str, str], ...], dependecies: Tuple[Tuple[str, str], ...]) -> str:
		'''Generate an SQL command to create page with given schema.'''
		sql_command: str = f'CREATE TABLE IF NOT EXISTS {page_name} ('
		
		for collum_schema in schema:
			sql_command+= f'\n\t{collum_schema[0]} {collum_schema[1]},'

		for dependece_schema in dependecies:
			sql_command+= f'\n\tFOREIGN KEY ({dependece_schema[0]}) REFERENCES {dependece_schema[1]},'
		
		return sql_command[:-1] + '\n)'

	def create_page(self: Self, page_name: str, schema: Tuple[Tuple[str, str], ...], dependecies: Tuple[Tuple[str, str], ...]):
		'''Create new page(table), if not exists, in database with specified schema.'''
		self._cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{page_name}';")
		if not self._cursor.fetchall():
			self._cursor.execute(self.generate_create_table_sql(page_name, schema, dependecies))



	def export_page_in_Json(self: Self, page_names: List[str], jsonorigin: JsonOrigin):
		'''Export list of pages(tables) to JSON under keys matching their names.'''

		json_data: Dict[str, List[Dict]] = {}

		with jsonorigin:
			for page_name in page_names:
				data: List[Tuple] = self.fetch_all(page_name)
				columns: List[str] = [col[0] for col in self.get_schema(page_name)]
				json_data[page_name] = [dict(zip(columns, row)) for row in data]

			jsonorigin.replace(json_data)


	def import_Json_in_page(self: Self, page_name: str, jsonorigin: JsonOrigin):
		'''Import JSON data into page(table) from key matching page name.'''

		with jsonorigin:
			for row in jsonorigin.load()[page_name]:
				self.insert_into_page(page_name, row)