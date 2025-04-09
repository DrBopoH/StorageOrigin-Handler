from typing import Type
import pytest, os, re

from scr.tests.conftest import DELETED_FILEPATHS, EXISTS_FILEPATHS, UNEXISTS_FILEPATHS, UNVALID_FILEPATHS
from scr.main import StorageOrigin



@pytest.mark.parametrize("filePath", EXISTS_FILEPATHS)
def test_positive_checkPathExists(filePath: str):
	assert StorageOrigin().path_exists(filePath) and os.path.exists(filePath)

@pytest.mark.parametrize("filePath", UNEXISTS_FILEPATHS)
def test_negative_checkPathExists(filePath: str):
	assert not (StorageOrigin().path_exists(filePath) and os.path.exists(filePath))


@pytest.mark.parametrize("filePath", EXISTS_FILEPATHS)
def test_positive_mountOrigin(filePath: str):
	storageorigin = StorageOrigin(filePath)

	assert storageorigin._filePath == filePath

@pytest.mark.parametrize("filePath", UNEXISTS_FILEPATHS)
def test_negative_mountOrigin(filePath: str):
	storageorigin = StorageOrigin(filePath)

	assert storageorigin._filePath == ''


def test_noinit_checkPathExists_noargs():
	assert not StorageOrigin().path_exists()


@pytest.mark.parametrize("filePath", EXISTS_FILEPATHS)
def test_positive_checkPathExists_noargs(filePath: str):
	assert StorageOrigin(filePath).path_exists()

@pytest.mark.parametrize("filePath", UNEXISTS_FILEPATHS)
def test_negative_checkPathExists_noargs(filePath: str):
	assert not StorageOrigin(filePath).path_exists()


@pytest.mark.parametrize("filePath", EXISTS_FILEPATHS+UNEXISTS_FILEPATHS)
def test_positive_createOrigin(filePath: str):
	storageorigin = StorageOrigin()
	storageorigin.create_and_mount(filePath)

	assert storageorigin.path_exists() and storageorigin._filePath == filePath
	if os.path.exists(filePath) and filePath not in EXISTS_FILEPATHS: os.remove(filePath)

@pytest.mark.parametrize("filePath, exception, exc_out", UNVALID_FILEPATHS)
def test_negative_createOrigin(filePath: str, exception: Type[Exception], exc_out: str):
	storageorigin = StorageOrigin()

	with pytest.raises(exception, match=re.escape(exc_out)):
		storageorigin.create_and_mount(filePath)
	

	assert not (storageorigin.path_exists() and storageorigin._filePath == filePath)
	if os.path.exists(filePath): os.remove(filePath)


def with_helloworld(storageorigin: StorageOrigin):
	with storageorigin:
		storageorigin._origin.seek(0)
		storageorigin._origin.write('Hello world!')
		storageorigin._origin.truncate()

@pytest.mark.parametrize("filePath", DELETED_FILEPATHS)
def test_positive_with(filePath: str):
	storageorigin = StorageOrigin()
	storageorigin.create_and_mount(filePath)

	with_helloworld(storageorigin)

	with storageorigin:
		assert storageorigin._origin.read() == 'Hello world!'

@pytest.mark.parametrize("filePath", DELETED_FILEPATHS)
def test_negative_with(filePath: str):
	storageorigin = StorageOrigin(filePath)

	if os.path.exists(filePath): os.remove(filePath)

	with pytest.raises(FileNotFoundError, match=f'{storageorigin}: File on path <{filePath}> not exists!'):
		with_helloworld(storageorigin)