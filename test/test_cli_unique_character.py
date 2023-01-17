from argparse import Namespace
from unittest.mock import mock_open, patch

import pytest

from unique_character import main, read_file, run_parser, validate_file


@patch('unique_character.cli_unique_character.run_parser', return_value=Namespace(filename=None, word=None))
def test_main_empty(mock_run_parser):
    with pytest.raises(ValueError):
        assert ValueError('Please select --string or --file') == main()
    mock_run_parser.assert_called_once()


@patch('unique_character.cli_unique_character.run_parser', return_value=Namespace(filename='path/to/open', word=None))
@patch('unique_character.cli_unique_character.validate_file', return_value='path/to/open')
@patch('unique_character.cli_unique_character.read_file', return_value='data43')
def test_main_file(mock_run_parser, mock_validate_file, mock_read_file):
    assert main() == 4
    mock_read_file.assert_called_once()
    mock_validate_file.assert_called_once()
    mock_run_parser.assert_called_once()


@patch('unique_character.cli_unique_character.run_parser', return_value=Namespace(filename=None, word='string'))
def test_main_string(mock_run_parser):
    assert main() == 6
    mock_run_parser.assert_called_once()


@pytest.mark.parametrize('param, expected_result',
                         [(['--string', 'string'], Namespace(filename=None, word='string')),
                          (['--file', 't.txt'], Namespace(filename='t.txt', word=None)),
                          ])
def test_run_parser(param, expected_result):
    assert run_parser(param) == expected_result


def test_read_file():
    with patch("builtins.open", mock_open(read_data="data")):
        assert read_file('path/to/open') == 'data'


@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_validate_file_error(mock_file):
    mock_file.assert_not_called()
    with pytest.raises(FileNotFoundError) as exc:
        validate_file('path/to/open')
    assert "File not found" in str(exc.value)


@patch('os.path.isfile')
@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_validate_file(mock_isfile, mock_file):
    assert validate_file('path/to/open') == "path/to/open"
    mock_file.assert_called_with("path/to/open")
    mock_isfile.assert_not_called()
