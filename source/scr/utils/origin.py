from typing import Self, Dict, Any
import sqlite3, json, os

class FileOrigin:
	''' '''

	_filePath: str = ''


	def mountOrigin(self: Self, filePath: str):
		'''Checking for existence of a file on new path'''
		if filePath in ['', '.']: raise ValueError('Not expected "", "."')
		
		if not os.path.exists(filePath): open(filePath, 'w').close()
		self._filePath = filePath




class JSONOrigin(FileOrigin):
	'''json library shell class for top-level work with JSON files'''

	encoding: str = 'utf-8'
	indentation: int = 4
	ensure_ascii: bool = False


	def getData(self: Self) -> Dict[str, Any]:
		'''Reading and returning data from JSON file'''
		if not self._filePath: raise FileNotFoundError(f"filePath <{self._filePath}> JSONOrigin is not exists")

		with open(self._filePath, 'r', encoding=self.encoding) as file:
			if os.path.getsize(self._filePath) != 0: return json.load(file)
			else: raise FileNotFoundError(f"Error trying to get data with <{self._filePath}> JSONOrigin, JSON file is empty")



	def saveData(self: Self, newData: Dict[str, Any]):
		'''Overwriting JSON file with new data'''
		if not self._filePath: raise FileNotFoundError(f"filePath <{self._filePath}> JSONOrigin is not exists")
		tempFilePath: str = f"{self._filePath}.tmp"

		try:
			with open(tempFilePath, 'w', encoding=self.encoding) as file: 
				json.dump(newData, file, indent=self.indentation, ensure_ascii=self.ensure_ascii)

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




class SQLiteOrigin(FileOrigin):
	''' '''

	pages: Dict[str, SQLitePage] = {}
	connecteddb: sqlite3.Connection
	connectedcursor: sqlite3.Cursor


	def closeConn(self: Self):
		if self.connecteddb: self.connecteddb.close()

	def createConn(self: Self):
		''' '''
		if not self._filePath: raise FileNotFoundError(f'Faile to connect, filePath <{self._filePath}> in SQLiteOrigin is not exists')

		self.connecteddb = sqlite3.connect(self._filePath)
		self.connectedcursor = self.connecteddb.cursor()



	def reloadPages(self: Self): 
		''' '''
		if self.connectedcursor:

			self.connectedcursor.execute("PRAGMA table_list;")
			for info in self.connectedcursor.fetchall():
				self.pages[info[1]] = SQLitePage(info[1])



	def createPage(self: Self, page_name: str, schema: Dict[str, str], dependecies: Dict[str, str]):
		''' '''
		if self.connectedcursor:
			self.connectedcursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{page_name}';")
			if self.connectedcursor.fetchall():

				sql_command: str = f'CREATE TABLE IF NOT EXISTS {page_name} ('
				for collum_name, value_type in schema.items():
					sql_command+= f'\n\t{collum_name} {value_type},'
				for collum_name, reference in dependecies.items():
					sql_command+= f'\n\tFOREIGN KEY ({collum_name}) REFERENCES {reference},'
				sql_command = sql_command[:-1] + '\n)'

				self.connectedcursor.execute(sql_command)