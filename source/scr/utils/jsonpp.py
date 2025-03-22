from typing import Dict, Any
import json

from ..utils.filepathorigin import FilepathOrigin




class JSONOrigin(FilepathOrigin):
	'''json library shell class for top-level work with JSON files'''

	fileTypeExcept = ['.json', '.secret', '.txt']
	encoding: str = 'utf-8'
	indentation: int = 4
	ensure_ascii: bool = False


	def setFormat(self, encoding: str = 'utf-8', indentation: int = 4, ensure_ascii: bool = False):
		''' '''
		self.encoding = encoding
		self.indentation = indentation
		self.ensure_ascii = ensure_ascii



	def getData(self) -> Dict[str, Any]:
		'''Reading and returning data from JSON file'''
		dataDict: Dict[str, Any] = {}

		if self.fileExist:
			with open(self.filePath, 'r', encoding=self.encoding) as file:
				try:
					dataDict = json.load(file)

				except Exception as e:
					print(f"Error trying to read <{self.filePath}> JSON file as: {e}")
		else: print("filePath in Origin is not exists")

		return dataDict



	def rebaseData(self, newData: Dict[str, Any]) -> bool:
		'''Overwriting JSON file with new data'''
		if self.fileExist:
			fileDataBackup: Dict[str, Any] = self.getData()

			with open(self.filePath, 'w', encoding=self.encoding) as file:
				try:
					json.dump(newData, file, indent=self.indentation, ensure_ascii=self.ensure_ascii)

				except Exception as e:
					print(f"Error trying to overwrite <{self.filePath}> JSON file as: {e}")
					json.dump(fileDataBackup, file)
					return False
		else: print("filePath in Origin is not exists")

		return True