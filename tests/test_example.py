# Test Example Module
import pytest

from jinacld_tools.example import add


@pytest.mark.parametrize("a, b, result", [(1, 1, 2), (2, 2, 4)])
def test_add(a: int, b: int, result: int) -> None:
    assert add(a, b) == result
