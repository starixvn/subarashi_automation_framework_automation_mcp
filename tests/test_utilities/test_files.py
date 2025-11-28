"""Unit tests for src/Core/utilities/files.py"""

import json
from pathlib import Path

import pandas as pd
import pytest

from src.Core.exceptions import AutomationError
from src.Core.utilities.files import Files


class TestReadWriteText:
    """Test text file operations."""

    def test_read_text_success(self, temp_test_file: Path) -> None:
        """Test read text file."""
        content = Files.read_text(str(temp_test_file))
        assert content == "Test content"

    def test_write_text_success(self, tmp_path: Path) -> None:
        """Test write text file."""
        file_path = tmp_path / "output.txt"
        Files.write_text(str(file_path), "Test output")

        assert file_path.exists()
        assert file_path.read_text() == "Test output"

    def test_read_text_file_not_found(self) -> None:
        """Test read text raises error when file not found."""
        with pytest.raises(AutomationError):
            Files.read_text("/nonexistent/file.txt")


class TestReadWriteJSON:
    """Test JSON file operations."""

    def test_read_json_success(self, temp_json_file: Path) -> None:
        """Test read JSON file."""
        data = Files.read_json(str(temp_json_file))
        assert data["key"] == "value"
        assert data["number"] == 123

    def test_write_json_success(self, tmp_path: Path) -> None:
        """Test write JSON file."""
        file_path = tmp_path / "output.json"
        data = {"test": "data", "num": 456}

        Files.write_json(str(file_path), data)

        assert file_path.exists()
        written_data = json.loads(file_path.read_text())
        assert written_data == data

    def test_append_json_data_new_file(self, tmp_path: Path) -> None:
        """Test append JSON data to new file."""
        file_path = tmp_path / "new.json"
        Files.append_json_data(str(file_path), {"key1": "value1"})

        assert file_path.exists()

    def test_append_json_data_existing_file(self, temp_json_file: Path) -> None:
        """Test append JSON data to existing file."""
        Files.append_json_data(str(temp_json_file), {"new_key": "new_value"})

        data = json.loads(temp_json_file.read_text())
        assert "new_key" in data

    def test_json_key_exists_true(self, temp_json_file: Path) -> None:
        """Test json_key_exists returns True when key exists."""
        result = Files.json_key_exists(str(temp_json_file), "key")
        assert result is True

    def test_json_key_exists_false(self, temp_json_file: Path) -> None:
        """Test json_key_exists returns False when key not exists."""
        result = Files.json_key_exists(str(temp_json_file), "nonexistent")
        assert result is False


class TestReadWriteExcel:
    """Test Excel file operations."""

    def test_read_excel_success(self, temp_excel_file: Path) -> None:
        """Test read Excel file."""
        df = Files.read_excel(str(temp_excel_file))
        assert isinstance(df, pd.DataFrame)
        # temp_excel_file has 3 rows of data
        assert len(df) >= 3

    def test_write_excel_success(self, tmp_path: Path) -> None:
        """Test write Excel file."""
        file_path = tmp_path / "output.xlsx"
        df = pd.DataFrame({"X": [1, 2], "Y": [3, 4]})

        Files.write_excel(str(file_path), df)

        assert file_path.exists()

    def test_read_cell_success(self) -> None:
        """Test read cell from DataFrame."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

        value = Files.read_cell(df, 0, 0)

        assert value == "1"

    def test_get_sheet_last_row(self) -> None:
        """Test get last row of sheet."""
        df = pd.DataFrame({"A": [1, 2, 3]})

        last_row = Files.get_sheet_last_row(df)

        assert last_row == 3

    def test_get_sheet_last_column(self) -> None:
        """Test get last column of sheet."""
        df = pd.DataFrame({"A": [1], "B": [2], "C": [3]})

        last_col = Files.get_sheet_last_column(df)

        assert last_col == 3


class TestFileOperations:
    """Test file system operations."""

    def test_file_exists_true(self, temp_test_file: Path) -> None:
        """Test file_exists returns True when file exists."""
        result = Files.file_exists(str(temp_test_file))
        assert result is True

    def test_file_exists_false(self) -> None:
        """Test file_exists returns False when file not exists."""
        result = Files.file_exists("/nonexistent/file.txt")
        assert result is False

    def test_delete_file_success(self, temp_test_file: Path) -> None:
        """Test delete file."""
        Files.delete_file(str(temp_test_file))
        assert not temp_test_file.exists()

    def test_get_file_size_success(self, temp_test_file: Path) -> None:
        """Test get file size."""
        size = Files.get_file_size(str(temp_test_file))
        assert size > 0

    def test_get_file_size_not_exists(self) -> None:
        """Test get file size returns 0 when not exists."""
        size = Files.get_file_size("/nonexistent.txt")
        assert size == 0


class TestDirectoryOperations:
    """Test directory operations."""

    def test_create_directory_success(self, tmp_path: Path) -> None:
        """Test create directory."""
        dir_path = tmp_path / "new_dir" / "sub_dir"

        Files.create_directory(str(dir_path))

        assert dir_path.exists()

    def test_create_directory_empty_path(self) -> None:
        """Test create directory with empty path."""
        Files.create_directory("")

    def test_list_files_success(self, tmp_path: Path) -> None:
        """Test list files in directory."""
        (tmp_path / "file1.txt").write_text("test")
        (tmp_path / "file2.txt").write_text("test")

        files = Files.list_files(str(tmp_path), ".txt")

        assert len(files) == 2

    def test_list_files_not_exists(self) -> None:
        """Test list files returns empty when dir not exists."""
        files = Files.list_files("/nonexistent")
        assert files == []
