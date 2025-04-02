from typing import List
import pytest, os, re




exists_filePaths: List[str] = [
	'tests/test.json',
	'tests/test_unvalid.json'
]
unexists_filePaths: List[str] = [
	'tests/abracadabra.db',
	'tests/fedora64.iso'
]
unvalid_filepaths: List[List[str | Exception]] = [
	['tests/test_unv*lid.json', OSError, "[Errno 22] Invalid argument: 'tests/test_unv*lid.json'"],
	['nonexistent_directory/file.txt', FileNotFoundError, "[Errno 2] No such file or directory: 'nonexistent_directory/file.txt'"],
	['', OSError, "[Errno 2] No such file or directory: ''"],
	['tests/' + 'very'*100 + 'longfile.txt', OSError, "[Errno 22] Invalid argument: '" + 'tests/' + 'very'*100 + 'longfile.txt' + "'"]
]
#['scr/tests/test_lockedaccess.json', PermissionError, 'Access to file is locked'],



@pytest.mark.parametrize("filePath", exists_filePaths)
def test_positive_checkPathExists(storageorigin, filePath: str):
	assert storageorigin.checkPathExists(filePath) and os.path.exists(filePath)

@pytest.mark.parametrize("filePath", unexists_filePaths)
def test_negative_checkPathExists(storageorigin, filePath: str):
	assert not (storageorigin.checkPathExists(filePath) and os.path.exists(filePath))


@pytest.mark.parametrize("filePath", exists_filePaths)
def test_positive_mountOrigin(storageorigin, filePath: str):
	storageorigin.mountOrigin(filePath)

	assert storageorigin._filePath == filePath

@pytest.mark.parametrize("filePath", unexists_filePaths)
def test_negative_mountOrigin(storageorigin, filePath: str):
	storageorigin.mountOrigin(filePath)

	assert storageorigin._filePath == ''


def test_noinit_checkPathExists_noargs(storageorigin):
	assert not storageorigin.checkPathExists()


@pytest.mark.parametrize("filePath", exists_filePaths)
def test_positive_checkPathExists_noargs(storageorigin, filePath: str):
	storageorigin.mountOrigin(filePath)

	assert storageorigin.checkPathExists()

@pytest.mark.parametrize("filePath", unexists_filePaths)
def test_negative_checkPathExists_noargs(storageorigin, filePath: str):
	storageorigin.mountOrigin(filePath)

	assert not storageorigin.checkPathExists()


@pytest.mark.parametrize("filePath", exists_filePaths+unexists_filePaths)
def test_positive_createOrigin(storageorigin, filePath: str):
	storageorigin.createOrigin(filePath)

	assertion: bool = storageorigin.checkPathExists() and storageorigin._filePath == filePath
	if os.path.exists(filePath) and filePath not in exists_filePaths: os.remove(filePath)

	assert assertion

@pytest.mark.parametrize("filePath, exception, exc_out", unvalid_filepaths)
def test_negative_createOrigin(storageorigin, filePath: str, exception: Exception, exc_out: str):
	with pytest.raises(exception, match=re.escape(exc_out)):
		storageorigin.createOrigin(filePath)
	

	assertion: bool = not (storageorigin.checkPathExists() and storageorigin._filePath == filePath)
	if os.path.exists(filePath): os.remove(filePath)

	assert assertion


# if '*' in exc_out else exc_out