from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from googleapiclient.errors import HttpError

from src.Core import auto_log, AutomationError
from .files import Files


class GoogleSheets:
    def __init__(self, service_account_file: str = None):
        self.service_account_file = (
            service_account_file or "config/secrets/client_secret.json"
        )
        self.service = None
        self._initialize_service()

    @auto_log
    def _initialize_service(self) -> None:
        try:
            if not Files.file_exists(self.service_account_file):
                raise AutomationError(
                    f"Google Sheets service account file not found: {self.service_account_file}"
                )

            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ]

            credentials = Credentials.from_service_account_file(
                self.service_account_file, scopes=scopes
            )

            self.service = discovery.build("sheets", "v4", credentials=credentials)
        except Exception as e:
            raise AutomationError(
                "Failed to initialize Google Sheets service", str(e)
            ) from e

    @auto_log
    def get_sheet_values(
        self, spreadsheet_id: str, sheet_name: str, range_name: str = None
    ) -> List[List[Any]]:
        try:
            if range_name:
                full_range = f"{sheet_name}!{range_name}"
            else:
                full_range = sheet_name

            result = (
                self.service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=spreadsheet_id,
                    range=full_range,
                    valueRenderOption="UNFORMATTED_VALUE",
                    dateTimeRenderOption="FORMATTED_STRING",
                )
                .execute()
            )

            values = result.get("values", [])
            return values
        except HttpError as e:
            raise AutomationError("Failed to get sheet values", str(e)) from e
        except Exception as e:
            raise AutomationError("Failed to get sheet values", str(e)) from e

    @auto_log
    def get_sheet_values_as_dataframe(
        self, spreadsheet_id: str, sheet_name: str
    ) -> pd.DataFrame:
        try:
            values = self.get_sheet_values(spreadsheet_id, sheet_name)

            if values:
                df = pd.DataFrame(values)
                date_columns = []

                def convert_to_date(val):
                    if isinstance(val, (int, float)):
                        try:
                            return (
                                datetime(1899, 12, 30) + timedelta(days=val)
                            ).strftime("%b %d, %Y")
                        except Exception:
                            return val
                    return val

                for col in date_columns:
                    if col in df.iloc[0].values:
                        col_index = df.iloc[0].values.tolist().index(col)
                        df.iloc[1:, col_index] = df.iloc[1:, col_index].apply(
                            convert_to_date
                        )

                return df
            else:
                return pd.DataFrame()
        except Exception as e:
            raise AutomationError(
                "Failed to get sheet values as DataFrame", str(e)
            ) from e

    @auto_log
    def get_sheet_all_information(
        self, spreadsheet_id: str, sheet_name: str
    ) -> Dict[str, Any]:
        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=spreadsheet_id,
                    range=sheet_name,
                    valueRenderOption="UNFORMATTED_VALUE",
                )
                .execute()
            )
            return result
        except Exception as e:
            raise AutomationError("Failed to get sheet all information", str(e)) from e

    @auto_log
    def insert_row(
        self, spreadsheet_id: str, sheet_name: str, row_data: List[Any]
    ) -> Dict[str, Any]:
        try:
            result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=sheet_name,
                    valueInputOption="RAW",
                    insertDataOption="INSERT_ROWS",
                    body={"values": [row_data]},
                )
                .execute()
            )
            return result
        except Exception as e:
            raise AutomationError("Failed to insert row", str(e)) from e

    @auto_log
    def update_sheet_range(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        data_list: List[List[Any]],
        range_update: str = None,
    ) -> Dict[str, Any]:
        try:
            if range_update is None:
                full_sheet_info = self.get_sheet_all_information(
                    spreadsheet_id, sheet_name
                )
                range_update = full_sheet_info.get("range", sheet_name)

            result = (
                self.service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    range=range_update,
                    valueInputOption="RAW",
                    body={"values": data_list},
                )
                .execute()
            )
            return result
        except Exception as e:
            raise AutomationError("Failed to update sheet range", str(e)) from e

    @auto_log
    def get_column_index(self, sheet_data: List[List[Any]], column_name: str) -> int:
        try:
            if not sheet_data or not sheet_data[0]:
                return -1

            for i, header in enumerate(sheet_data[0]):
                if header == column_name:
                    return i
            return -1
        except Exception as e:
            raise AutomationError("Failed to get column index", str(e)) from e

    @auto_log
    def update_test_result(
        self,
        spreadsheet_id: str,
        checklist: str,
        auto_testcase: str,
        sub_auto_testcases: str,
        auto_status: str,
        sheet_name: str = "Checklist",
    ) -> List[List[Any]]:
        try:
            values = self.get_sheet_values(spreadsheet_id, sheet_name)

            if not values:
                return []

            today = datetime.now()
            to_date = today.strftime("%m/%d/%Y %H:%M:%S")

            for i in range(2, len(values)):
                if len(values[i]) >= 12:
                    if values[i][2] == checklist and values[i][11] == auto_testcase:
                        range_update = f"{sheet_name}!M{i + 1}:O{i + 1}"
                        data_update = [[sub_auto_testcases, auto_status, to_date]]
                        self.update_sheet_values(
                            spreadsheet_id,
                            sheet_name,
                            data_update,
                            range_update.split("!")[1],
                        )
                        break

            return values
        except Exception as e:
            raise AutomationError("Failed to update test result", str(e)) from e

    @auto_log
    def update_sheet_values(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        values: List[List[Any]],
        range_name: str = None,
        value_input_option: str = "RAW",
    ) -> Dict[str, Any]:
        try:
            if range_name:
                full_range = f"{sheet_name}!{range_name}"
            else:
                full_range = sheet_name

            body = {"values": values}

            result = (
                self.service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    range=full_range,
                    valueInputOption=value_input_option,
                    body=body,
                )
                .execute()
            )

            return result
        except HttpError as e:
            raise AutomationError("Failed to update sheet", str(e)) from e
        except Exception as e:
            raise AutomationError("Failed to update sheet", str(e)) from e

    @auto_log
    def append_values(
        self, spreadsheet_id: str, sheet_name: str, values: List[List[Any]]
    ) -> Dict[str, Any]:
        try:
            body = {"values": values}

            result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=sheet_name,
                    valueInputOption="RAW",
                    body=body,
                )
                .execute()
            )

            return result
        except HttpError as e:
            raise AutomationError("Failed to append to sheet", str(e)) from e
        except Exception as e:
            raise AutomationError("Failed to append to sheet", str(e)) from e

    @auto_log
    def clear_sheet(
        self, spreadsheet_id: str, sheet_name: str, range_name: str = None
    ) -> Dict[str, Any]:
        try:
            if range_name:
                full_range = f"{sheet_name}!{range_name}"
            else:
                full_range = sheet_name

            result = (
                self.service.spreadsheets()
                .values()
                .clear(spreadsheetId=spreadsheet_id, range=full_range)
                .execute()
            )

            return result
        except HttpError as e:
            raise AutomationError("Failed to clear sheet", str(e)) from e
        except Exception as e:
            raise AutomationError("Failed to clear sheet", str(e)) from e

    @auto_log
    def get_sheet_info(self, spreadsheet_id: str) -> Dict[str, Any]:
        try:
            result = (
                self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            )

            return result
        except HttpError as e:
            raise AutomationError("Failed to get spreadsheet info", str(e)) from e
        except Exception as e:
            raise AutomationError("Failed to get spreadsheet info", str(e)) from e

    @auto_log
    def create_sheet(self, spreadsheet_id: str, sheet_name: str) -> Dict[str, Any]:
        try:
            request_body = {
                "requests": [{"addSheet": {"properties": {"title": sheet_name}}}]
            }

            result = (
                self.service.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
                .execute()
            )

            return result
        except HttpError as e:
            raise AutomationError(
                f"Failed to create sheet '{sheet_name}'", str(e)
            ) from e
        except Exception as e:
            raise AutomationError(
                f"Failed to create sheet '{sheet_name}'", str(e)
            ) from e

    @auto_log
    def delete_sheet(self, spreadsheet_id: str, sheet_id: int) -> Dict[str, Any]:
        try:
            request_body = {"requests": [{"deleteSheet": {"sheetId": sheet_id}}]}

            result = (
                self.service.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
                .execute()
            )

            return result
        except HttpError as e:
            raise AutomationError(
                f"Failed to delete sheet ID {sheet_id}", str(e)
            ) from e
        except Exception as e:
            raise AutomationError(
                f"Failed to delete sheet ID {sheet_id}", str(e)
            ) from e

    @auto_log
    def batch_update(
        self, spreadsheet_id: str, requests: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        try:
            request_body = {"requests": requests}

            result = (
                self.service.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
                .execute()
            )

            return result
        except HttpError as e:
            raise AutomationError("Failed to perform batch update", str(e)) from e
        except Exception as e:
            raise AutomationError("Failed to perform batch update", str(e)) from e

    @auto_log
    def find_cell(
        self, spreadsheet_id: str, sheet_name: str, search_value: Any
    ) -> Optional[Dict[str, int]]:
        try:
            values = self.get_sheet_values(spreadsheet_id, sheet_name)

            for row_index, row in enumerate(values):
                for col_index, cell_value in enumerate(row):
                    if str(cell_value) == str(search_value):
                        result = {"row": row_index + 1, "column": col_index + 1}
                        return result

            return None
        except Exception as e:
            raise AutomationError("Failed to find cell", str(e)) from e

    @auto_log
    def get_row_data(
        self, spreadsheet_id: str, sheet_name: str, row_number: int
    ) -> List[Any]:
        try:
            range_name = f"{row_number}:{row_number}"
            values = self.get_sheet_values(spreadsheet_id, sheet_name, range_name)

            if values:
                return values[0]
            else:
                return []
        except Exception as e:
            raise AutomationError(f"Failed to get row {row_number} data", str(e)) from e

    @auto_log
    def update_cell(
        self, spreadsheet_id: str, sheet_name: str, row: int, column: int, value: Any
    ) -> Dict[str, Any]:
        try:
            # Convert column number to letter (1=A, 2=B, etc.)
            column_letter = chr(64 + column)
            range_name = f"{column_letter}{row}"

            values = [[value]]
            return self.update_sheet_values(
                spreadsheet_id, sheet_name, values, range_name
            )
        except Exception as e:
            raise AutomationError(
                f"Failed to update cell {row},{column}", str(e)
            ) from e

    @auto_log
    def log_test_result(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        test_name: str,
        status: str,
        timestamp: str = None,
    ) -> None:
        try:
            if not timestamp:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            row_data = [[test_name, status, timestamp]]
            self.append_values(spreadsheet_id, sheet_name, row_data)
        except Exception as e:
            raise AutomationError("Failed to log test result", str(e)) from e
