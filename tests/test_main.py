from os import PathLike
from pathlib import Path
from sqlite3 import Connection

from branch_memory.main import database_connection, dump_database, dumps_exist


def test_database_connection(database_path):
    connection = database_connection(database_path)
    assert isinstance(connection, Connection)


def test_dump_database(seeded_db, storage_dir):
    database = dump_database(seeded_db, storage_dir)
    assert isinstance(database, PathLike)
    assert Path(database).exists()
    assert Path(database).is_file()


def test_dumps_exist(storage_dir, populated_storage_dir):
    assert dumps_exist(storage_dir) is False
    assert dumps_exist(populated_storage_dir) is True


def test_previous_dump():
    pass
