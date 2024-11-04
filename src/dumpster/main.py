from datetime import datetime, timezone
from os import PathLike
from pathlib import Path
from sqlite3 import Connection, Cursor, Row, connect


def _make_datetime() -> datetime:
    return datetime.now(tz=timezone.utc)


def _get_db_name(database_connection: Connection) -> str:
    cursor: Cursor = database_connection.execute(
        "SELECT name FROM pragma_database_list;"
    )
    db_name: str = cursor.fetchone()[0]

    return db_name


# create a database connection
def database_connection(connection_string: str) -> Connection:
    connection = connect(connection_string)
    connection.row_factory = Row
    return connection


# store the database dump
def dump_database(connection_string: str, storage_location: str | PathLike) -> Path:
    file_timestamp: str = _make_datetime().strftime("%m-%d-%Y_%H:%M:%S")
    db_connection = database_connection(connection_string)
    db_name = _get_db_name(db_connection)
    stored_file: Path = Path(storage_location) / f"{db_name}_{file_timestamp}_dump.sql"
    with open(stored_file, "w") as f:
        for line in db_connection.iterdump():
            f.write(f"{line}\n")
    db_connection.close()
    return stored_file


# check if there are exisiting dumps
def dumps_exist(storage_location: str | PathLike) -> bool:
    for path in Path(storage_location).iterdir():
        if path.is_file():
            if any(word in path.name for word in ["dump"]):
                return True
    return False


# diff dumps

# return diff

##########
#  LATER
##########
# on demand dump

# git hook for branch dump(s)

# cloud storage for dumps
