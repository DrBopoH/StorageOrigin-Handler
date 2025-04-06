import pytest

from scr.tests.conftest import EXISTS_FILEPATHS
from scr.StorageOrigin import NoteOrigin


@pytest.mark.parametrize("filePath, text", [
	[EXISTS_FILEPATHS[1], ''], 
	[EXISTS_FILEPATHS[-1], '{"vova":"promax",}']
])
def test_positive_getText(filePath: str, text: str):
	with NoteOrigin(filePath) as noteorigin:
		assert noteorigin.get() == text


@pytest.mark.parametrize("filePath, newText, text", [
	[EXISTS_FILEPATHS[1], 'hello', 'hello'],
	[EXISTS_FILEPATHS[1], ' ', 'hello '],
	[EXISTS_FILEPATHS[1], 'world!', 'hello world!'],
])
def test_positive_addText(filePath: str, newText: str, text: str):
	noteorigin = NoteOrigin(filePath)

	with noteorigin: noteorigin.add(newText)

	with noteorigin:
		assert noteorigin.get() == text


@pytest.mark.parametrize("filePath, text", [
	[EXISTS_FILEPATHS[1], 'abracadabra!'],
	[EXISTS_FILEPATHS[1], '']
])
def test_positive_replaceText(filePath: str, text: str):
	noteorigin = NoteOrigin(filePath)

	with noteorigin: noteorigin.replace(text)

	with noteorigin:
		assert noteorigin.get() == text