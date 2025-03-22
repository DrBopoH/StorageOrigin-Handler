import sqlite3, os
from typing import Dict

from ..utils.filepathorigin import FilepathOrigin


class SQLitePage:
	''' '''
	page_name: str

	def __init__(self, page_name: str) -> None:
		self.page_name = page_name


class SQLiteOrigin(FilepathOrigin):
	''' '''

	fileTypeExcept = ['.db']
	active: bool
	pages: Dict[str, SQLitePage]
	connecteddb: sqlite3.Connection
	connectedcursor: sqlite3.Cursor



	def connectToDB(self) -> bool:
		''' '''
		if self.fileExist:
			try:
				self.connecteddb = sqlite3.connect(self.filePath)
				self.connectedcursor = self.connecteddb.cursor()
			except Exception as e:
				print(f"Error trying to connecting <{self.filePath}> as: {e}")
				self.active = False
		self.active = True

		self.loadPages()

		return self.active

	def loadPages(self):
		''' '''
		if self.active:
			self.connectedcursor.execute("PRAGMA table_list;")
			for info in self.connectedcursor.fetchall():
				self.pages[info[1]] = SQLitePage(info[1])


	def createPage(self, page_name: str, schema: Dict[str, str], dependecies: Dict[str, str]):
		if self.active:
			sql_command: str = f'CREATE TABLE IF NOT EXISTS {page_name} ('
			for collum_name, value_type in schema:
				sql_command+= f'\n\t{collum_name} {value_type},'
			for collum_name, reference in dependecies:
				sql_command+= f'\n\tFOREIGN KEY {collum_name} REFERENCES {reference}'

			self.connectedcursor.execute(sql_command)



	def closeActiveDB(self):
		''' '''
		if self.active:
			self.connecteddb.close()