import pytest

from scr.StorageOrigin import *




@pytest.fixture
def storageorigin() -> StorageOrigin:
	return StorageOrigin()


@pytest.fixture
def noteorigin() -> NoteOrigin:
	return NoteOrigin()


@pytest.fixture
def jsonorigin() -> JsonOrigin:
	return JsonOrigin()


@pytest.fixture
def sqliteorigin() -> SQLiteOrigin:
	return SQLiteOrigin()



