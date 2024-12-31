from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence, TypeAlias

from sqlalchemy.util import immutabledict


class ConnectionPrefix(str, Enum):
    POSTGRES = "postgresql+psycopg"


ConnectionQuery: TypeAlias = Mapping[str, str | Sequence[str]]


@dataclass
class ConnectionArgs:
    host: str = "127.0.0.1"
    username: str | None = None
    password: str | None = None
    port: int | None = None
    database: str | None = None
    query: ConnectionQuery = field(default_factory=immutabledict[Any, Any])


class DbConnection:
    def __init__(self, connection_args: ConnectionArgs) -> None:
        self.connection_args = connection_args

        self._schemas = []
        self._tables = []

    @property
    def schemas(self) -> list[str]:
        return self._schemas

    @property
    def tables(self) -> list[str]:
        return self._tables
