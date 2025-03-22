import pytest, os

#def test_positive_createOrigin(sqliteorigin):
#	assert sqliteorigin.createOrigin('scr/tests/test.db')

def test_positive_createPage(sqliteorigin):
	assert sqliteorigin.createOrigin('scr/tests/test.db')
	assert sqliteorigin.connectToDB()
	assert sqliteorigin.createPage("users")

