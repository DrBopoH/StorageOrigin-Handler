from typing import List
import os

class FilepathOrigin:
	''' '''

	filePath: str
	fileExist: bool = False
	fileTypeExcept: List[str]

	def createOrigin(self, filePath: str) -> bool:
		'''Checking for existence of a file on new path'''
		exist: bool = os.path.exists(filePath)
		fileType: str = os.path.splitext(filePath)[1]

		if exist and fileType in (self.fileTypeExcept if self.fileTypeExcept[0] != '' else [fileType]):
			self.filePath = filePath

			self.fileExist = True
		else: self.fileExist = False
		
		return self.fileExist