import pytest, os

@pytest.mark.parametrize("filePath", [
		'scr/tests/test.db'])
def test_positive_mountOrigin(sqliteorigin, filePath: str):
	assert sqliteorigin.mountOrigin(filePath)

@pytest.mark.parametrize("filePath", [
		'scr/tests/test.json',
		'scr/tests/test_empty.json'])
def test_negative_mountOrigin(sqliteorigin, filePath: str):
	assert not sqliteorigin.mountOrigin(filePath)


def test_positive_connectToDB(sqliteorigin):
	sqliteorigin.mountOrigin('scr/tests/test.db')
	
	assert sqliteorigin.connectToDB()

	sqliteorigin.closeActiveDB()


@pytest.mark.parametrize("page_name, scheme, dependecies, sql_command", [
		[
			'users', 
			{'id':'INTEGER PRIMARY KEY AUTOINCREMENT', 'username':'TEXT UNIQUE NOT NULL', 'email':'TEXT UNIQUE NOT NULL', 'created_at':'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'}, 
			{}, 
			'CREATE TABLE IF NOT EXISTS users (\n\tid INTEGER PRIMARY KEY AUTOINCREMENT,\n\tusername TEXT UNIQUE NOT NULL,\n\temail TEXT UNIQUE NOT NULL,\n\tcreated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n)'
		],[
			'posts', 
			{'id':'INTEGER PRIMARY KEY AUTOINCREMENT', 'user_id':'INTEGER NOT NULL', 'title':'TEXT NOT NULL', 'content':'TEXT NOT NULL', 'created_at':'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'}, 
			{'user_id':'users(id)'}, 
			'CREATE TABLE IF NOT EXISTS posts (\n\tid INTEGER PRIMARY KEY AUTOINCREMENT,\n\tuser_id INTEGER NOT NULL,\n\ttitle TEXT NOT NULL,\n\tcontent TEXT NOT NULL,\n\tcreated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n\tFOREIGN KEY (user_id) REFERENCES users(id)\n)'
		],[
			'comments', 
			{'id':'INTEGER PRIMARY KEY AUTOINCREMENT', 'post_id':'INTEGER NOT NULL', 'user_id':'INTEGER NOT NULL', 'text':'TEXT NOT NULL', 'created_at':'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'}, 
			{'post_id':'posts(id)','user_id':'users(id)'}, 
			'CREATE TABLE IF NOT EXISTS comments (\n\tid INTEGER PRIMARY KEY AUTOINCREMENT,\n\tpost_id INTEGER NOT NULL,\n\tuser_id INTEGER NOT NULL,\n\ttext TEXT NOT NULL,\n\tcreated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n\tFOREIGN KEY (post_id) REFERENCES posts(id),\n\tFOREIGN KEY (user_id) REFERENCES users(id)\n)'
		]
	]
)
def test_positive_createPage(sqliteorigin, page_name: str, scheme: dict[str, str], dependecies: dict[str, str], sql_command: str):
	sqliteorigin.mountOrigin('scr/tests/test.db')
	sqliteorigin.connectToDB()

	assert sqliteorigin.createPage(page_name, scheme, dependecies) == sql_command

	sqliteorigin.closeActiveDB()

@pytest.mark.parametrize("page_name", ['users', 'posts', 'comments'])
def test_positive_reloadPages(sqliteorigin, page_name: str):
	sqliteorigin.mountOrigin('scr/tests/test.db')
	sqliteorigin.connectToDB()

	assert page_name == sqliteorigin.pages[page_name].page_name

	sqliteorigin.closeActiveDB()