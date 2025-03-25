import pytest

from scr.utils.origin import *




@pytest.fixture
def jsonorigin() -> JSONOrigin:
	return JSONOrigin()



@pytest.fixture
def sqliteorigin() -> SQLiteOrigin:
	return SQLiteOrigin()



@pytest.fixture
def fileorigin() -> FileOrigin:
	return FileOrigin()