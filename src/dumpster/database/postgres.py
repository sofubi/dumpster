from typing import Any, Generator

from psycopg.connection import Connection
from psycopg.cursor import Cursor
from psycopg.rows import namedtuple_row
from psycopg.abc import Query


class PostgresConnection:
    # TODO: Consider how the password should be handled
    def __init__(
        self,
        host: str,
        dbname: str,
        user: str | None = None,
        password: str | None = None,
        port: str | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname

    def _build_conninfo(self, **kwargs) -> str:
        host = f"host={self.host}"
        dbname = f"dbname={self.dbname}"

        if self.port:
            port = f"port={self.port}"
        else:
            port = ""

        if self.user:
            user = f"user={self.user}"
        else:
            user = ""

        if self.password:
            password = f"password={self.password}"
        else:
            password = ""

        extra_args = ""
        if kwargs:
            for key, val in kwargs.items():
                extra_args += f"{key}={val} "

        return f"{host} {dbname} {port} {user} {password} {extra_args}"

    def open_connection(self, extra_args: dict[str, Any] | None = None) -> Connection:
        if extra_args:
            conninfo = self._build_conninfo(**extra_args)
        else:
            conninfo = self._build_conninfo()

        try:
            return Connection.connect(conninfo, row_factory=namedtuple_row)
        except Exception:
            raise

    def cursor(self) -> Generator[Cursor]:
        with self.open_connection() as conn:
            cursor = conn.cursor(row_factory=namedtuple_row)
            yield cursor
            cursor.close()

    def execute(self, query: Query, params: dict[str, Any] | None = None) -> Cursor:
        try:
            return self.open_connection().execute(query, params)
        except Exception:
            raise
