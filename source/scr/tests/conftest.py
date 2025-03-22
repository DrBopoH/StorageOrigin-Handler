import pytest

from ..utils.jsonpp import *
from ..dbs.sqlpp import *




@pytest.fixture
def jsonorigin() -> JSONOrigin:
	return JSONOrigin()



@pytest.fixture
def sqliteorigin() -> SQLiteOrigin:
	return SQLiteOrigin()