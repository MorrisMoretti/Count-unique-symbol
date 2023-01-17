import pytest

from unique_character import ValueException, count_letter


@pytest.mark.parametrize("word, expected_result", [('aaabbcc123', 3),
                                                   ('abc123!@#', 9),
                                                   ('aaabbbc', 1),
                                                   ('abbbccc', 1)])
def test_count(word, expected_result):
    assert count_letter(word) == expected_result


def test_check_decorator():
    assert hasattr(count_letter, '__wrapped__')


@pytest.mark.parametrize('test_type', [777, 3.14, (2 - 3j), (7, 7, 7), True, None])
def test_data_type(test_type):
    with pytest.raises(ValueException) as exc:
        count_letter(test_type)
    assert "Please pass only str" in str(exc.value)
