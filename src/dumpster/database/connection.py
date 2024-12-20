from enum import Enum

from sqlalchemy import MetaData, Table, create_engine, inspect
from sqlalchemy.engine import Engine


class ConnectionPrefix(str, Enum):
    POSTGRES = "postgresql+psycopg://"


def get_engine(db_type: str, conn_string: str):
    conn_prefix = ConnectionPrefix[db_type.upper()]

    return create_engine(f"{conn_prefix}{conn_string}")


def fetch_schemas(engine: Engine) -> list[str]:
    try:
        inspector = inspect(engine)
        return inspector.get_schema_names()

    except Exception:
        raise


def table_list(engine: Engine, schema: str) -> list[str]:
    try:
        inspector = inspect(engine)
        return inspector.get_table_names(schema)

    except Exception:
        raise


def table_from_meta(engine: Engine, schema: str, table: str) -> Table:
    meta_obj = MetaData()
    return Table(table, meta_obj, schema=schema, autoload_with=engine)
