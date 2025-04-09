from typing import Type, Dict 
import pytest, json, os, re

from scr.tests.conftest import EXISTS_FILEPATHS, JSON_EXAMPLES
from scr.main import JsonOrigin



@pytest.mark.parametrize("filePath", [EXISTS_FILEPATHS[0]])
def test_positive_getJson(filePath: str):
	with JsonOrigin(filePath) as jsonorigin:
		assert jsonorigin.load() == JSON_EXAMPLES[-1]

@pytest.mark.parametrize("filePath, exception, exc_out", [
	[EXISTS_FILEPATHS[-1], json.decoder.JSONDecodeError, "Expecting property name enclosed in double quotes: line 1 column 18 (char 17)"],
	[EXISTS_FILEPATHS[1], ValueError, f": Error trying to get data with <{EXISTS_FILEPATHS[1]}>, JSON file is empty"]
])
def test_negative_getJson(filePath: str, exception: Type[Exception], exc_out: str):
	jsonorigin = JsonOrigin(filePath)

	exc_out = f"{jsonorigin.__repr__()}"+exc_out if filePath == EXISTS_FILEPATHS[1] else exc_out

	with pytest.raises(exception, match=re.escape(exc_out)):
		with jsonorigin:
			jsonorigin.load()


@pytest.mark.parametrize("data", JSON_EXAMPLES)
def test_positive_replaceJson(data: Dict):
	jsonorigin = JsonOrigin(EXISTS_FILEPATHS[0])

	with jsonorigin: jsonorigin.replace(data)

	with jsonorigin:
		assert jsonorigin.load() == data and not os.path.exists(f'{EXISTS_FILEPATHS[0]}.tmp')

#@pytest.mark.parametrize("data", JSON_EXAMPLES)
#def test_negative_replaceJson(data: Dict):
#	jsonorigin = JsonOrigin(EXISTS_FILEPATHS[0])

#	with pytest.raises(RuntimeError, match=f"{jsonorigin.__repr__()}: Error trying to save data in <{jsonorigin}>, error as: "):
#		with jsonorigin: 
#			jsonorigin.replaceJson(data)


@pytest.mark.parametrize("data", JSON_EXAMPLES)
def test_notsafe_replaceJson(data: Dict):
	jsonorigin = JsonOrigin(EXISTS_FILEPATHS[0])

	with jsonorigin: jsonorigin.replace(data, False)

	with jsonorigin:
		assert jsonorigin.load() == data and not os.path.exists(f'{EXISTS_FILEPATHS[0]}.tmp')