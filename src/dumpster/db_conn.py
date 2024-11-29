from enum import Enum
from functools import partial
from typing import Any, TypeAlias

from mysql.connector import connect as mysql_connect
from mysql.connector.abstracts import (
    MySQLConnectionAbstract as mysql_conn_class,
    MySQLCursorAbstract as mysql_cursor,
)
from mysql.connector.pooling import PooledMySQLConnection as pooled_mysql_conn_class
from psycopg import (
    connect as pgsql_connnect,
    Connection as pgsql_conn_class,
    Cursor as pgsql_cursor,
)
from pymssql import (
    connect as mssql_connect,
    Connection as mssql_conn_class,
    Cursor as mssql_cursor,
)


class DBMS(str, Enum):
    INNODB = partial(mysql_connect)
    MARIADB = partial(mysql_connect)
    MSSQL = partial(mssql_connect)
    MYSQL = partial(mysql_connect)
    POSTGRES = partial(pgsql_connnect)
    # SQLITE = "sqlite3"


MySQLConnection: TypeAlias = mysql_conn_class | pooled_mysql_conn_class

DBMSConnection: TypeAlias = MySQLConnection | pgsql_conn_class | mssql_conn_class

MaybeDBMSConnection: TypeAlias = (
    MySQLConnection | pgsql_conn_class | mssql_conn_class | None
)

DBMSCursor: TypeAlias = mysql_cursor | pgsql_cursor | mssql_cursor

MaybeDBMSCursor: TypeAlias = mysql_cursor | pgsql_cursor | mssql_cursor | None


class DbConnection:
    # TODO: Consider how the password should be handled
    def __init__(
        self,
        dbms: DBMS,
        host: str,
        port: str,
        user: str,
        password: str,
        database: str,
    ) -> None:
        self.conn_func = dbms.value
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        self._connection: MaybeDBMSConnection = None

    @property
    def connection(self) -> MaybeDBMSConnection:
        return self._connection

    def connect(self, **kwargs) -> DBMSConnection:
        if not self._connection:
            try:
                self._connection = self.conn_func(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    **kwargs,
                )
            except Exception:
                raise

        return self._connection

    def cursor(
        self,
        cur_kwargs: dict[Any, Any] | None = None,
        conn_kwargs: dict[Any, Any] | None = None,
    ) -> MaybeDBMSCursor:
        if not self._connection:
            if conn_kwargs:
                self.connect(**conn_kwargs)
            else:
                self.connect()

        if self._connection:
            if cur_kwargs:
                cursor = self._connection.cursor(**cur_kwargs)
            else:
                cursor = self._connection.cursor()

            return cursor

    def execute(self):
        pass

    def _insert(self):
        pass

    def select(self):
        pass
