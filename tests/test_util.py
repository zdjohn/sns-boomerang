from sns_boomerang.settings import util
import pytest


@pytest.mark.parametrize("test_input,expected", [
    ("correct-naming", True),
    ("bad-naming-", False),
    ('', False),
])
def test_letters_and_numbers_only(test_input, expected):
    isvalid = util.letters_and_numbers_only(test_input)
    assert isvalid == expected


def test_hash():
    value = util.compute_hash('a', 'b')
    assert value == '187ef4436122d1cc2f40dc2b92f0eba0'
