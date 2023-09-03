import pytest

# Test always passes
@pytest.mark.testenv
def test_true():
    assert True

# Test always fails
@pytest.mark.testenv
def test_false():
    assert False