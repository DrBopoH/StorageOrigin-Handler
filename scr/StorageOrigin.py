from typing import Self, Dict, Any
import sqlite3, json, os




class StorageOrigin:
	''' '''

	encoding: str = 'utf-8'

	_filePath: str = ''
	_origin = None


	def open(self: Self):
		if self.checkPathExists(): self._origin = open(self._filePath, 'r+', encoding=self.encoding)

	def close(self: Self):
		if self._origin is not None: self._origin = self._origin.close()



	def __enter__(self: Self) -> Self:
		self.open()
		return self

	def __exit__(self: Self):
		self.close()



	def checkPathExists(self: Self, filePath: str | None = None) -> bool:
		'''

		Checking for existence of a file on filePath.
		If new path == None, checking now path(self._filePath).

		Return (if path == EXISTS).
		
		'''
		if filePath is None: filePath = self._filePath

		if not os.path.exists(filePath): 
			print(f'<{self}>: File on path <{filePath}> not exists.')
			return False

		return True



	def mountOrigin(self: Self, filePath: str):
		if self.checkPathExists(filePath): self._filePath = filePath

	def createOrigin(self: Self, filePath: str):
		if not self.checkPathExists(filePath): open(filePath, 'w').close()

		self.mountOrigin(filePath)




class NoteOrigin(StorageOrigin):
	''' '''

	def getText(self: Self) -> str:
		return self._origin.read()

	def addText(self: Self, additionalText: str, cookie: int | None = None):
		self._origin.seek(0 if cookie is None else cookie, 2 if cookie is None else 0)
		self._origin.write(additionalText)

	def replaceText(self: Self, newText: str, cookie: int | None = None):
		self._origin.seek(0 if cookie is None else cookie, 0 if cookie is None else 2)
		self._origin.write(newText)
		self._origin.truncate()



class JsonOrigin(StorageOrigin):
	'''json library shell class for top-level work with JSON files'''

	indentation: int = 4
	ensure_ascii: bool = False


	def getJson(self: Self) -> Dict[str, Any]:
		'''Reading and returning data from JSON file'''
		if os.path.getsize(self._filePath) == 0: 
			raise ValueError(f"Error trying to get data with <{self._filePath}> JSONOrigin, JSON file is empty")

		return json.load(self._origin)



	def replaceJson(self: Self, newData: Dict[str, Any]):
		'''Overwriting JSON file with new data'''
		tempFilePath: str = f"{self._filePath}.tmp"

		try:
			with open(tempFilePath, 'w', encoding=self.encoding) as tempFile: 
				json.dump(newData, tempFile, indent=self.indentation, ensure_ascii=self.ensure_ascii)

		except (OSError, PermissionError, json.JSONDecodeError) as e:
			raise RuntimeError(f"Error trying to save data in <{self._filePath}>, error as: {e}")

		else: os.replace(tempFilePath, self._filePath)
		
		finally: 
			if os.path.exists(tempFilePath): os.remove(tempFilePath)




class SQLitePage:
	''' '''

	page_name: str


	def __init__(self: Self, page_name: str):
		self.page_name = page_name




class SQLiteOrigin(StorageOrigin):
	''' '''

	pages: Dict[str, SQLitePage] = {}
	_cursor: sqlite3.Cursor | None


	def open(self: Self):
		''' '''
		if self.checkPathExists():
			self._origin = sqlite3.connect(self._filePath)
			self._cursor = self._origin.cursor()

	def close(self: Self):
		if self._origin is not None: 
			self._origin = self._origin.close()
			self._cursor = None
	



	def reloadPages(self: Self): 
		''' '''
		self._cursor.execute("PRAGMA table_list;")
		for info in self._cursor.fetchall():
			self.pages[info[1]] = SQLitePage(info[1])



	def createPage(self: Self, page_name: str, schema: Dict[str, str], dependecies: Dict[str, str]):
		''' '''
		self._cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{page_name}';")
		if self._cursor.fetchall():

			sql_command: str = f'CREATE TABLE IF NOT EXISTS {page_name} ('
			for collum_name, value_type in schema.items():
				sql_command+= f'\n\t{collum_name} {value_type},'
			for collum_name, reference in dependecies.items():
				sql_command+= f'\n\tFOREIGN KEY ({collum_name}) REFERENCES {reference},'
			sql_command = sql_command[:-1] + '\n)'

			self._cursor.execute(sql_command)