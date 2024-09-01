import pytest
from src.main import add_numbers

def test_add_numbers():
    # Test cases
    assert add_numbers(1, 2) == 3