import pytest
from src.utils.has_money import has_money

def test_regex_matches():
    examples = [
        "$1",
        "$1,000",
        "$111,111.11",
        "$1,000,000.00",
        "1 dollar",
        "1,000 dollars",
        "1,000,000.00 dollars",
        "1 USD",
        "1,000 USD",
        "1,000,000.00 USD"
    ]

    for example in examples:
        assert has_money(example), f"Failed to match: {example}"

def test_regex_not_matches():
    non_examples = [
        "$1,00",
        "$1111,111.11",
        "1.000,00 dollars",
        "$1.000,00 USD",
        "one dollar",
        "1,000,000.000 USD"
    ]

    for non_example in non_examples:
        assert not has_money(non_example), f"Incorrectly matched: {non_example}"
