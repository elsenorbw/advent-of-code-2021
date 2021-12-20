import pytest

from day18 import SnailfishNumber


@pytest.mark.parametrize(
    "input_number",
    [
        ("[1,2]"),
        ("[[1,2],3]"),
        ("[9,[8,7]]"),
        ("[[1,9],[8,5]]"),
        ("[[[[1,2],[3,4]],[[5,6],[7,8]]],9]"),
        ("[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]"),
        ("[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"),
    ],
)
def test_snailfish_parse(input_number):
    """
    check that they all parse and get represented as themselves
    """
    actual = SnailfishNumber.parse(input_number)
    assert str(actual) == input_number


@pytest.mark.parametrize(
    "input_number,expected_result,expected_number",
    [
        ("[[[[[9,8],1],2],3],4]", True, "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", True, "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", True, "[[6,[5,[7,0]]],3]"),
        (
            "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
            True,
            "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
        ),
        ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", True, "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
        ("[[1,2],[3,4]]", False, "[[1,2],[3,4]]"),
    ],
)
def test_explode(input_number, expected_result, expected_number):
    """
    Check that the explode logic does what we would expect
    """
    numb = SnailfishNumber.parse(input_number)
    actual = numb.explode()
    assert actual == expected_result
    assert expected_number == str(numb)


@pytest.mark.parametrize(
    "input_number,expected_result,expected_number",
    [
        ("9", False, "9"),
        ("[9,9]", False, "[9,9]"),
        ("10", True, "[5,5]"),
        ("11", True, "[5,6]"),
        ("[16,14]", True, "[[8,8],14]"),
    ],
)
def test_split(input_number, expected_result, expected_number):
    """
    Check that the splitting logic is working as expected
    """
    numb = SnailfishNumber.parse(input_number)
    actual = numb.split()
    assert actual == expected_result
    assert expected_number == str(numb)


@pytest.mark.parametrize(
    "number1,number2,expected_number",
    [
        ("1", "2", "[1,2]"),
        ("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
        (
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
        ),
        (
            "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
            "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
        ),
        (
            "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
            "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
            "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]",
        ),
        (
            "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]",
            "[7,[5,[[3,8],[1,4]]]]",
            "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]",
        ),
        (
            "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]",
            "[[2,[2,2]],[8,[8,1]]]",
            "[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]",
        ),
        (
            "[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]",
            "[2,9]",
            "[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]",
        ),
        (
            "[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]",
            "[1,[[[9,3],9],[[9,0],[0,7]]]]",
            "[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]",
        ),
        (
            "[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]",
            "[[[5,[7,4]],7],1]",
            "[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]",
        ),
        (
            "[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]",
            "[[[[4,2],2],6],[8,7]]",
            "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
        ),
    ],
)
def test_addition(number1, number2, expected_number):
    """
    Confirm that the addition logic is doing what we expect
    """
    a = SnailfishNumber.parse(number1)
    b = SnailfishNumber.parse(number2)
    actual = SnailfishNumber.add(a, b)
    assert str(actual) == expected_number


@pytest.mark.parametrize(
    "number,expected",
    [
        ("[9,1]", 29),
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ],
)
def test_magnitude(number, expected):
    """
    Check that the magnitude calculation does what it should
    """
    numb = SnailfishNumber.parse(number)
    actual = numb.magnitude()
    assert actual == expected


@pytest.mark.parametrize(
    "number_list,expected",
    [
        (
            [
                "[1,1]",
                "[2,2]",
                "[3,3]",
                "[4,4]",
            ],
            "[[[[1,1],[2,2]],[3,3]],[4,4]]",
        ),
        (
            [
                "[1,1]",
                "[2,2]",
                "[3,3]",
                "[4,4]",
                "[5,5]",
            ],
            "[[[[3,0],[5,3]],[4,4]],[5,5]]",
        ),
        (
            [
                "[1,1]",
                "[2,2]",
                "[3,3]",
                "[4,4]",
                "[5,5]",
                "[6,6]",
            ],
            "[[[[5,0],[7,4]],[5,5]],[6,6]]",
        ),
        (
            [
                "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
                "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
                "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
                "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
                "[7,[5,[[3,8],[1,4]]]]",
                "[[2,[2,2]],[8,[8,1]]]",
                "[2,9]",
                "[1,[[[9,3],9],[[9,0],[0,7]]]]",
                "[[[5,[7,4]],7],1]",
                "[[[[4,2],2],6],[8,7]]",
            ],
            "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
        ),
    ],
)
def test_add_list(number_list, expected):
    """
    Check the logic for adding lists of numbers..
    """
    actual = SnailfishNumber.add_list(number_list)
    assert str(actual) == expected


def test_homework_exercise():
    """
    A single straight-through example from the problem statement
    """
    numbers_to_add = [
        "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
        "[[[5,[2,8]],4],[5,[[9,9],0]]]",
        "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
        "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
        "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
        "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
        "[[[[5,4],[7,7]],8],[[8,3],8]]",
        "[[9,3],[[9,9],[6,[4,9]]]]",
        "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
        "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]",
    ]
    expected_number = "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"
    expected_magnitude = 4140

    the_result = SnailfishNumber.add_list(numbers_to_add)
    assert str(the_result) == expected_number
    assert the_result.magnitude() == expected_magnitude
