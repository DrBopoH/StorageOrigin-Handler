import pytest, os




@pytest.mark.parametrize("filePath", [
		'scr/tests/test.json',
		'scr/tests/test.txt'
	])
def test_positive_mountOrigin(fileorigin, filePath: str):
	fileorigin.mountOrigin(filePath)

	exist: bool = os.path.exists(filePath)
	if exist: os.remove(filePath)

	assert exist

@pytest.mark.parametrize("filePath", ['', '.'])
def test_negative_mountOrigin(fileorigin, filePath: str):
	with pytest.raises(ValueError): fileorigin.mountOrigin(filePath)