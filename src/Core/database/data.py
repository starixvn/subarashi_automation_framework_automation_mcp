from typing import Dict, List, Any, Optional, TYPE_CHECKING
from src.Core import auto_log, AutomationError

if TYPE_CHECKING:
    from .query import Query


class Data:
    def __init__(self, query: "Query") -> None:
        self.query = query

    @auto_log
    def insert_record(
        self, table: str, data: Dict[str, Any], schema: str = "dbo"
    ) -> int:
        if not data:
            raise AutomationError("Data dictionary cannot be empty")
        try:
            columns = list(data.keys())
            values = list(data.values())
            placeholders = ",".join("?" * len(values))
            sql = f"INSERT INTO {schema}.{table} ({','.join(columns)}) VALUES ({placeholders})"
            affected_rows: int = self.query.execute_insert(sql, tuple(values))
            return affected_rows
        except Exception as e:
            raise AutomationError(
                f"Failed to insert record into {table}", str(e)
            ) from e

    @auto_log
    def insert_records(
        self, table: str, records: List[Dict[str, Any]], schema: str = "dbo"
    ) -> int:
        if not records:
            raise AutomationError("Records list cannot be empty")
        try:
            total_affected = 0
            for record in records:
                affected = self.insert_record(table, record, schema)
                total_affected += affected
            return total_affected
        except Exception as e:
            raise AutomationError(
                f"Failed to insert records into {table}", str(e)
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

            cursor = self.query.connection.cursor
            conn = self.query.connection.connection
            if not cursor or not conn:
                raise AutomationError("Cursor or Connection is None")
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn_rollback = self.query.connection.connection
            if conn_rollback:
                conn_rollback.rollback()
            raise AutomationError(
                f"Failed to insert data into {table_name}", str(e)
            ) from e

    @auto_log
    def update_record(
        self,
        table: str,
        data: Dict[str, Any],
        where_clause: str,
        where_params: Optional[tuple[Any, ...]] = None,
        schema: str = "dbo",
    ) -> int:
        if not data:
            raise AutomationError("Data dictionary cannot be empty")
        try:
            set_clauses = [f"{key} = ?" for key in data.keys()]
            values = list(data.values())
            sql = f"UPDATE {schema}.{table} SET {','.join(set_clauses)} WHERE {where_clause}"
            if where_params:
                values.extend(where_params)
            affected_rows: int = self.query.execute_update(sql, tuple(values))
            return affected_rows
        except Exception as e:
            raise AutomationError(f"Failed to update records in {table}", str(e)) from e

    @auto_log
    def delete_records(
        self,
        table: str,
        where_clause: str,
        where_params: Optional[tuple[Any, ...]] = None,
        schema: str = "dbo",
    ) -> int:
        try:
            sql = f"DELETE FROM {schema}.{table} WHERE {where_clause}"
            affected_rows: int = self.query.execute_delete(sql, where_params)
            return affected_rows
        except Exception as e:
            raise AutomationError(
                f"Failed to delete records from {table}", str(e)
            ) from e

    @auto_log
    def get_records(
        self,
        table: str,
        columns: str = "*",
        where_clause: str = "1=1",
        where_params: Optional[tuple[Any, ...]] = None,
        schema: str = "dbo",
    ) -> List[Dict[str, Any]]:
        try:
            sql = f"SELECT {columns} FROM {schema}.{table} WHERE {where_clause}"
            records: List[Dict[str, Any]] = self.query.execute_select(sql, where_params)
            return records
        except Exception as e:
            raise AutomationError(f"Failed to get records from {table}", str(e)) from e

    @auto_log
    def get_record_count(
        self,
        table: str,
        where_clause: str = "1=1",
        where_params: Optional[tuple[Any, ...]] = None,
        schema: str = "dbo",
    ) -> int:
        try:
            sql = f"SELECT COUNT(*) as count FROM {schema}.{table} WHERE {where_clause}"
            result = self.query.execute_select(sql, where_params)
            return result[0]["count"] if result else 0
        except Exception as e:
            raise AutomationError(
                f"Failed to get record count from {table}", str(e)
            ) from e

    @auto_log
    def truncate_table(self, table: str, schema: str = "dbo") -> None:
        try:
            sql = f"TRUNCATE TABLE {schema}.{table}"
            cursor = self.query.connection.cursor
            if not cursor:
                raise AutomationError("Cursor is None")
            cursor.execute(sql)
        except Exception as e:
            raise AutomationError(f"Failed to truncate table {table}", str(e)) from e

    @auto_log
    def backup_table(
        self,
        source_table: str,
        backup_table: str,
        where_clause: str = "1=1",
        where_params: Optional[tuple[Any, ...]] = None,
        schema: str = "dbo",
    ) -> int:
        try:
            sql = f"""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{backup_table}' AND xtype='U')
                    SELECT * INTO {schema}.{backup_table} FROM {schema}.{source_table} WHERE 1=0;
                    
                INSERT INTO {schema}.{backup_table}
                SELECT * FROM {schema}.{source_table}
                WHERE {where_clause}
            """
            affected_rows: int = self.query.execute_insert(sql, where_params)
            return affected_rows
        except Exception as e:
            raise AutomationError(
                f"Failed to backup {source_table} to {backup_table}", str(e)
            ) from e

    @auto_log
    def table_exists(self, table_name: str, schema: str = "dbo") -> bool:
        try:
            sql = "SELECT COUNT(*) as count FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?"
            result = self.query.execute_select(sql, (schema, table_name))
            return result[0]["count"] > 0 if result else False
        except Exception as e:
            raise AutomationError(
                f"Failed to check if table {table_name} exists", str(e)
            ) from e

    @auto_log
    def get_table_columns(self, table_name: str, schema: str = "dbo") -> List[str]:
        try:
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ? ORDER BY ORDINAL_POSITION"
            results = self.query.execute_select(sql, (schema, table_name))
            return [row["COLUMN_NAME"] for row in results]
        except Exception as e:
            raise AutomationError(
                f"Failed to get columns for table {table_name}", str(e)
            ) from e

    @auto_log
    def bulk_insert(
        self,
        table: str,
        data_list: List[Dict[str, Any]],
        schema: str = "dbo",
        batch_size: int = 1000,
    ) -> int:
        if not data_list:
            raise AutomationError("Data list cannot be empty")
        try:
            total_affected = 0
            for i in range(0, len(data_list), batch_size):
                batch = data_list[i : i + batch_size]
                affected = self.insert_records(table, batch, schema)
                total_affected += affected
            return total_affected
        except Exception as e:
            raise AutomationError(f"Failed to bulk insert into {table}", str(e)) from e
