import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from src.Core import auto_log, AutomationError


class Files:
    @staticmethod
    @auto_log
    def read_text(file_path: str, encoding: str = "utf-8") -> str:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                content = file.read()
            return content
        except Exception as e:
            raise AutomationError(f"Failed to read file {file_path}", str(e))

    @staticmethod
    @auto_log
    def write_text(file_path: str, content: str, encoding: str = "utf-8") -> None:
        try:
            Files.create_directory(os.path.dirname(file_path))

            with open(file_path, "w", encoding=encoding) as file:
                file.write(content)
        except Exception as e:
            raise AutomationError(f"Failed to write file {file_path}", str(e))

    @staticmethod
    @auto_log
    def read_json(file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data
        except Exception as e:
            raise AutomationError(f"Failed to read JSON file {file_path}", str(e))

    @staticmethod
    @auto_log
    def write_json(file_path: str, data: Dict[str, Any], indent: int = 2) -> None:
        try:
            Files.create_directory(os.path.dirname(file_path))

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
        except Exception as e:
            raise AutomationError(f"Failed to write JSON file {file_path}", str(e))

    @staticmethod
    @auto_log
    def append_json_data(file_path: str, data: Dict[str, Any]) -> None:
        try:
            existing_data = {}
            if Files.file_exists(file_path):
                existing_data = Files.read_json(file_path)

            existing_data.update(data)
            Files.write_json(file_path, existing_data)
        except Exception as e:
            raise AutomationError(f"Failed to append JSON data to {file_path}", str(e))

    @staticmethod
    @auto_log
    def json_key_exists(file_path: str, key: str) -> bool:
        try:
            if not Files.file_exists(file_path):
                return False

            data = Files.read_json(file_path)
            return key in data
        except Exception as e:
            raise AutomationError(
                f"Failed to check JSON key in {file_path}", str(e)
            ) from e

    @staticmethod
    @auto_log
    def read_excel(
        file_path: str,
        sheet_name: Optional[Union[str, int]] = None,
        header: Optional[int] = None,
    ) -> pd.DataFrame:
        try:
            engine = "openpyxl" if file_path.endswith(".xlsx") else None

            if sheet_name is not None:
                df = pd.read_excel(
                    file_path, sheet_name=sheet_name, engine=engine, header=header
                )
            else:
                df = pd.read_excel(file_path, engine=engine, header=header)

            df = df.dropna(axis=1, how="all")
            return df
        except Exception as e:
            raise AutomationError(f"Failed to read Excel file {file_path}", str(e))

    @staticmethod
    @auto_log
    def write_excel(
        file_path: str, data: pd.DataFrame, sheet_name: str = "Sheet1"
    ) -> None:
        try:
            Files.create_directory(os.path.dirname(file_path))
            data.to_excel(file_path, sheet_name=sheet_name, index=False)
        except Exception as e:
            raise AutomationError(f"Failed to write Excel file {file_path}", str(e))

    @staticmethod
    @auto_log
    def read_cell(
        sheet: pd.DataFrame, row_index: int, column_index: int, start_row: int = 2
    ) -> Union[str, List[Any]]:
        try:
            if row_index == -1:
                return sheet.iloc[start_row:, column_index].tolist()
            elif column_index == -1:
                return sheet.iloc[row_index].tolist()
            else:
                value = sheet.iloc[row_index, column_index]
                if pd.isna(value):
                    return ""
                return str(value)
        except Exception as e:
            raise AutomationError("Failed to read cell from sheet", str(e)) from e

    @staticmethod
    @auto_log
    def get_sheet_last_row(sheet: pd.DataFrame) -> int:
        try:
            return len(sheet)
        except Exception as e:
            raise AutomationError("Failed to get last row", str(e)) from e

    @staticmethod
    @auto_log
    def get_sheet_last_column(sheet: pd.DataFrame) -> int:
        try:
            return len(sheet.iloc[-1]) if len(sheet) > 0 else 0
        except Exception as e:
            raise AutomationError("Failed to get last column", str(e)) from e

    @staticmethod
    @auto_log
    def remove_file(
        file_path: str, root_dir: str = None, subfolder: str = "Excel"
    ) -> None:
        try:
            if root_dir and subfolder:
                full_path = os.path.join(root_dir, subfolder, file_path)
            else:
                full_path = file_path

            if os.path.exists(full_path):
                os.remove(full_path)
        except Exception as e:
            raise AutomationError(f"Failed to remove file {file_path}", str(e)) from e

    @staticmethod
    @auto_log
    def create_directory(directory_path: str) -> None:
        if not directory_path:
            return

        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise AutomationError(
                f"Failed to create directory {directory_path}", str(e)
            )

    @staticmethod
    @auto_log
    def file_exists(file_path: str) -> bool:
        try:
            exists = os.path.exists(file_path)
            return exists
        except Exception:
            return False

    @staticmethod
    @auto_log
    def delete_file(file_path: str) -> None:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            raise AutomationError(f"Failed to delete file {file_path}", str(e))

    @staticmethod
    @auto_log
    def get_file_size(file_path: str) -> int:
        try:
            if not os.path.exists(file_path):
                return 0

            size = os.path.getsize(file_path)
            return size
        except Exception as e:
            raise AutomationError(f"Failed to get size of {file_path}", str(e))

    @staticmethod
    @auto_log
    def list_files(directory_path: str, extension: str = None) -> List[str]:
        try:
            if not os.path.exists(directory_path):
                return []

            files = []
            for file in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path):
                    if extension is None or file.endswith(extension):
                        files.append(file_path)

            return files
        except Exception as e:
            raise AutomationError(f"Failed to list files in {directory_path}", str(e))
