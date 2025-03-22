from ..utils import utils

def test_add():
    assert utils.add(2, 3) == 5
    assert utils.add(-1, 1) == 0

def test_multiply():
    assert utils.multiply(3, 4) == 12
    assert utils.multiply(0, 5) == 0
