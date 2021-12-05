import pytest

from day4 import BingoCard


@pytest.fixture
def simple_card_range():
    return list(range(1, 26))


def test_bingocard_setup(simple_card_range):
    """
    Check that the BingoCard class does what we want..
    """
    b = BingoCard(simple_card_range)
    board_description = str(b)
    # Check horizontals
    assert "{1, 2, 3, 4, 5}" in board_description
    assert "{6, 7, 8, 9, 10}" in board_description
    assert "{11, 12, 13, 14, 15}" in board_description
    assert "{16, 17, 18, 19, 20}" in board_description
    assert "{21, 22, 23, 24, 25}" in board_description
    # Check verticals
    assert "{1, 6, 11, 16, 21}" in board_description
    assert "{2, 7, 12, 17, 22}" in board_description
    assert "{3, 8, 13, 18, 23}" in board_description
    assert "{4, 9, 14, 19, 24}" in board_description
    assert "{5, 10, 15, 20, 25}" in board_description


@pytest.mark.parametrize(
    "numbers_called,expecting_bingo",
    [
        ([1, 2, 3, 4, 5], True),
        ([1, 2, 3, 4, 6], False),
        ([1, 2, 3, 4, 6, 7, 8, 9, 5], True),
        ([6, 7, 8, 9, 10], True),
        ([11, 12, 13, 14, 15], True),
        ([16, 17, 18, 19, 20], True),
        ([21, 22, 23, 24, 25], True),
    ],
)
def test_bingocard_bingo(numbers_called, expecting_bingo, simple_card_range):
    """
    Check that we get bingos when we should..
    """
    b = BingoCard(simple_card_range)
    actual_bingo = b.is_bingo(numbers_called)
    assert actual_bingo == expecting_bingo


@pytest.mark.parametrize(
    "numbers_called,expected_score",
    [(range(1, 6), sum(range(6, 26)) * 5), (range(1, 26), 0), (range(1, 25), 600)],
)
def test_bingocard_score(numbers_called, expected_score, simple_card_range):
    """
    Check that the score is as expected
    """
    b = BingoCard(simple_card_range)
    actual_score = b.score_card(numbers_called)
    assert actual_score == expected_score
