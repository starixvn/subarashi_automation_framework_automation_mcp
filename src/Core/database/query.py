from typing import List, Dict, Any, Optional
from pathlib import Path
from src.Core import auto_log, AutomationError
from .connection import Connection


class Query:
    def __init__(self, connection: Connection):
        self.connection = connection

    @auto_log
    def execute_select(
        self, sql: str, params: Optional[tuple[Any, ...]] = None
    ) -> List[Dict[str, Any]]:
        if not self.connection.is_connected:
            raise AutomationError("Not connected to database")
        cursor = self.connection.cursor
        if not cursor:
            raise AutomationError("Cursor is None")
        try:
            cursor.execute(sql, params or ())
            if not cursor.description:
                return []
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise AutomationError("Failed to execute SELECT query", str(e)) from e

    @auto_log
    def execute_insert(self, sql: str, params: Optional[tuple[Any, ...]] = None) -> int:
        if not self.connection.is_connected:
            raise AutomationError("Not connected to database")
        cursor = self.connection.cursor
        if not cursor:
            raise AutomationError("Cursor is None")
        try:
            cursor.execute(sql, params or ())
            rows_affected: int = cursor.rowcount
            return rows_affected
        except Exception as e:
            raise AutomationError("Failed to execute INSERT query", str(e)) from e

    @auto_log
    def execute_update(self, sql: str, params: Optional[tuple[Any, ...]] = None) -> int:
        if not self.connection.is_connected:
            raise AutomationError("Not connected to database")
        cursor = self.connection.cursor
        if not cursor:
            raise AutomationError("Cursor is None")
        try:
            cursor.execute(sql, params or ())
            rows_affected: int = cursor.rowcount
            return rows_affected
        except Exception as e:
            raise AutomationError("Failed to execute UPDATE query", str(e)) from e

    @auto_log
    def execute_delete(self, sql: str, params: Optional[tuple[Any, ...]] = None) -> int:
        if not self.connection.is_connected:
            raise AutomationError("Not connected to database")
        cursor = self.connection.cursor
        if not cursor:
            raise AutomationError("Cursor is None")
        try:
            cursor.execute(sql, params or ())
            rows_affected: int = cursor.rowcount
            return rows_affected
        except Exception as e:
            raise AutomationError("Failed to execute DELETE query", str(e)) from e

    @auto_log
    def query(self, sql: str, query_type: str = "select") -> Any:
        if not self.connection.is_connected:
            raise AutomationError("Not connected to database")
        cursor = self.connection.cursor
        conn = self.connection.connection
        if not cursor or not conn:
            raise AutomationError("Cursor or Connection is None")
        try:
            cursor.execute(sql)
            if query_type.lower() == "select":
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise AutomationError(
                f"Failed to execute {query_type} query", str(e)
            ) from e

    @auto_log
    def query_and_get_all(self, sql: str) -> List[Dict[str, Any]]:
        if not self.connection.is_connected:
            raise AutomationError("Not connected to database")
        cursor = self.connection.cursor
        if not cursor:
            raise AutomationError("Cursor is None")
        try:
            cursor.execute(sql)
            if not cursor.description:
                return []
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                row_dict = {}
                for i, value in enumerate(row):
                    row_dict[columns[i]] = str(value) if value is not None else None
                results.append(row_dict)
            return results
        except Exception as e:
            raise AutomationError("Failed to get all query results", str(e)) from e

    @auto_log
    def get_value_in_column(self, sql: str, column_name: str) -> List[str]:
        if not self.connection.is_connected:
            raise AutomationError("Not connected to database")
        cursor = self.connection.cursor
        if not cursor:
            raise AutomationError("Cursor is None")
        try:
            cursor.execute(sql)
            values: List[str] = []
            for row in cursor.fetchall():
                value = getattr(row, column_name, None)
                if value is not None:
                    values.append(str(value))
                else:
                    values.append("")
            return values
        except Exception as e:
            raise AutomationError(
                f"Failed to get values from column {column_name}", str(e)
            ) from e

    @auto_log
    def insert_data_to_table(self, table_name: str, params: Dict[str, Any]) -> None:
        if not params:
            raise AutomationError("Parameters cannot be empty")
        try:
            columns = []
            values = []
            for key, value in params.items():
                columns.append(key)
                if value is None or str(value).lower() == "null":
                    values.append("NULL")
                elif "today" in str(value).lower():
                    date_value = str(value).lower().replace("today", "GETDATE()")
                    values.append(date_value)
                elif "first_day_of_month" in str(value).lower():
                    values.append("DATEADD(MM,DATEDIFF(MM, 0, GETDATE()),0)")
                elif "last_day_of_month" in str(value).lower():
                    values.append("DATEADD(MM,DATEDIFF(MM, -1, GETDATE()),-1)")
                else:
                    values.append(f"'{str(value)}'")

            column_names = ", ".join(columns)
            value_list = ", ".join(values)
            sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({value_list})"

            cursor = self.connection.cursor
            conn = self.connection.connection
            if not cursor or not conn:
                raise AutomationError("Cursor or Connection is None")
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn_rollback = self.connection.connection
            if conn_rollback:
                conn_rollback.rollback()
            raise AutomationError(
                f"Failed to insert data into {table_name}", str(e)
            ) from e

    @auto_log
    def insert_data_from_file(
        self, sql_file: str, replacements: List[List[str]], iterations: int = 1
    ) -> List[Any]:
        if iterations > 10:
            iterations = 10
        try:
            file_path = Path(sql_file)
            if not file_path.exists():
                raise AutomationError(f"SQL file not found: {sql_file}")

            with open(file_path, "r", encoding="utf-8") as f:
                sql_content = f.read()

            for replacement in replacements[1:]:
                if len(replacement) >= 2:
                    sql_content = sql_content.replace(replacement[0], replacement[1])

            results = []
            for _ in range(iterations):
                try:
                    cursor = self.connection.cursor
                    conn = self.connection.connection
                    if not cursor or not conn:
                        raise AutomationError("Cursor or Connection is None")
                    cursor.execute(sql_content)
                    data = cursor.fetchall()
                    conn.commit()

                    for row in data:
                        result = [row[0], row[1]] if len(row) >= 2 else list(row)
                        results.append(result)
                        if len(row) > 0 and row[0] > 0:
                            break
                except Exception:
                    conn_rollback = self.connection.connection
                    if conn_rollback:
                        conn_rollback.rollback()

            return results
        except Exception as e:
            raise AutomationError(
                f"Failed to insert data from file {sql_file}", str(e)
            ) from e

    @auto_log
    def execute_stored_procedure(
        self, procedure_name: str, params: Optional[tuple[Any, ...]] = None
    ) -> List[Dict[str, Any]]:
        if not self.connection.is_connected:
            raise AutomationError("Not connected to database")
        cursor = self.connection.cursor
        if not cursor:
            raise AutomationError("Cursor is None")
        try:
            if params:
                cursor.execute(
                    f"EXEC {procedure_name} {','.join(['?' for _ in params])}", params
                )
            else:
                cursor.execute(f"EXEC {procedure_name}")

            if cursor.description:
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            else:
                return []
        except Exception as e:
            raise AutomationError(
                f"Failed to execute stored procedure '{procedure_name}'", str(e)
            ) from e

    @auto_log
    def execute_batch(self, queries: List[Dict[str, Any]]) -> List[int]:
        if not self.connection.is_connected:
            raise AutomationError("Not connected to database")
        cursor = self.connection.cursor
        if not cursor:
            raise AutomationError("Cursor is None")
        results = []
        try:
            for query_info in queries:
                sql = query_info.get("sql")
                params = query_info.get("params")

                if not sql:
                    raise AutomationError("SQL query is required in batch")

                cursor.execute(sql, params or ())
                results.append(cursor.rowcount)

            return results
        except Exception as e:
            raise AutomationError("Failed to execute batch queries", str(e)) from e

    @auto_log
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        try:
            sql = """
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = ?
                ORDER BY ORDINAL_POSITION
            """
            return self.execute_select(sql, (table_name,))
        except Exception as e:
            raise AutomationError(
                f"Failed to get table info for '{table_name}'", str(e)
            ) from e

    @auto_log
    def count_records(self, table_name: str, where_clause: Optional[str] = None) -> int:
        try:
            sql = f"SELECT COUNT(*) as count FROM {table_name}"
            if where_clause:
                sql += f" WHERE {where_clause}"

            result = self.execute_select(sql)
            return result[0]["count"] if result else 0
        except Exception as e:
            raise AutomationError(
                f"Failed to count records in '{table_name}'", str(e)
            ) from e

    @auto_log
    def execute_scalar(self, sql: str, params: Optional[tuple[Any, ...]] = None) -> Any:
        if not self.connection.is_connected:
            raise AutomationError("Not connected to database")
        cursor = self.connection.cursor
        if not cursor:
            raise AutomationError("Cursor is None")
        try:
            cursor.execute(sql, params or ())
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            raise AutomationError("Failed to execute scalar query", str(e)) from e
