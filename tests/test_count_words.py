import pytest
from src.utils.count_words import count_words


def test_count_words():
    examples = {
        "This is a test.": 4,
        "Hello, world!": 2,
        "Keith Haring’s art might not be for everybody, but he is": 11,
        "The quick brown fox jumps over the lazy dog.": 9,
        "It's a beautiful day in the neighborhood.": 7,
        "One, two, three... Testing!": 4
    }

    for phrase, expected_count in examples.items():
        assert count_words(phrase) == expected_count, f"Failed on phrase: {phrase}"
