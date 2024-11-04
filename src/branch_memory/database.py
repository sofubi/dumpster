from typing import Any

from psycopg import connect as pgconnect
from psycopg import connection


class DBConnection:
    def __init__(self, db_type: str, connection_string: str):
        self.db_type: str = db_type
        self.connection_string: str = connection_string

    def connect(self) -> connection:
        return pgconnect()

    def dump(self) -> Any:
        raise NotImplementedError

    # def should_dump()
    # def dump_with_params()
