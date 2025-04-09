from typing import Tuple
import pytest, os

from scr.tests.conftest import SQL_TEMPLATES, UNEXISTS_FILEPATHS
from scr.main import SQLiteOrigin



@pytest.mark.parametrize("sql_template", SQL_TEMPLATES)
def test_positive_getSQLcommand_createPage(sql_template: Tuple[str, Tuple[Tuple[str, str], ...], Tuple[Tuple[str, str],	...], str]):
	sqliteorigin = SQLiteOrigin()
	assert sqliteorigin.generate_create_table_sql(sql_template[0], sql_template[1], sql_template[2]) == sql_template[3]

@pytest.mark.parametrize("sql_template", SQL_TEMPLATES)
def test_positive_createPage(sql_template: Tuple[str, Tuple[Tuple[str, str], ...], Tuple[Tuple[str, str],	...], str]):
	sqliteorigin = SQLiteOrigin()
	sqliteorigin.create_and_mount(UNEXISTS_FILEPATHS[-1])

	with sqliteorigin:
		sqliteorigin.create_page(sql_template[0], sql_template[1], sql_template[2])


@pytest.mark.parametrize("page_names", [
	('users', 'posts', 'comments')
])
def test_positive_reloadPages(page_names: Tuple[str, ...]):
	with SQLiteOrigin(UNEXISTS_FILEPATHS[-1]) as sqliteorigin:
		for page_name in page_names:
			assert page_name in sqliteorigin.get_pages()

	if os.path.exists(UNEXISTS_FILEPATHS[-1]): os.remove(UNEXISTS_FILEPATHS[-1])