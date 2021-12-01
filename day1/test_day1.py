import pytest
from day1 import count_increases, load_integers_from_file


@pytest.fixture
def good_file(tmpdir):
    """
    Create a valid file of good integers and return the filename
    """
    f = tmpdir.join("good.txt")
    f.write("1\n2\n3\n4\n5\n")
    return str(f)


@pytest.fixture
def alpha_file(tmpdir):
    """
    Create a file of good integers with an alpha-numeric in there somewhere
    return the filename
    """
    f = tmpdir.join("good.txt")
    f.write("1\n2\n3\ncat\n4\n5\n")
    return str(f)


@pytest.mark.parametrize(
    "input_list,expected_result",
    [
        ([1, 2, 3], 2),
        ([], 0),
        ([1], 0),
        ([100, 99, 100, 101, 98, 100], 3),
        ([1001, 1002, 1003, 1004, 1005, 1005, 1005, 1006], 5),
    ],
)
def test_count_increases(input_list, expected_result):
    actual_result = count_increases(input_list)
    assert actual_result == expected_result


def test_load_integers_from_file(good_file):
    # Positive testing for now
    result = load_integers_from_file(good_file)
    assert [1, 2, 3, 4, 5] == result


def test_load_integers_from_file_bad_file(alpha_file):
    # should throw an error..
    with pytest.raises(ValueError):
        load_integers_from_file(alpha_file)


def test_load_integers_from_file_missing_file():
    # should throw an error..
    with pytest.raises(FileNotFoundError):
        load_integers_from_file("/imaginary/filename")
