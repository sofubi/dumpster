from sqlite3 import Row, connect

import pytest

ROOT_SEED = """
    CREATE TABLE test(a, b, c);
    INSERT INTO test (a, b, c) VALUES('testing', 'testing', 'testing');
    INSERT INTO test (a, b, c) VALUES('HELP', 'HELP', 'HELP');
    CREATE TABLE testing(x, y, z);
    INSERT INTO testing (x, y, z) VALUES('here', 'here', 'here');
    INSERT INTO testing (x, y, z) VALUES('there', 'there', 'there');
"""

VALUE_UPDATE = """
    UPDATE 
        test 
    SET 
        b = 'tested',
        c = NULL
    WHERE
        a = 'testing';
"""

RECORD_DELETE = """
    DELETE FROM
        test
    WHERE
        a = 'HELP';
"""


def make_db_connection(db_path):
    connection = connect(db_path)
    connection.row_factory = Row
    return connection


def db_transaction(db_connection, sql_statement):
    with db_connection:
        db_connection.executescript(sql_statement)


@pytest.fixture
def storage_dir(tmp_path_factory, request):
    return tmp_path_factory.mktemp("storage")


@pytest.fixture
def database_path(storage_dir):
    db_path = storage_dir / "test_database.sqlite3"
    db_path.touch()

    return db_path


@pytest.fixture
def populated_storage_dir(database_path, storage_dir):
    populated_path = storage_dir / "populated"
    populated_path.mkdir()
    db_connection = make_db_connection(database_path)

    for statement in [ROOT_SEED, VALUE_UPDATE, RECORD_DELETE]:
        db_transaction(db_connection, statement)
        dump_database(str(database_path), populated_path)

    db_connection.close()

    return populated_path


@pytest.fixture
def seeded_db(database_path):
    db_connection = make_db_connection(database_path)
    db_transaction(db_connection, ROOT_SEED)
    db_connection.close()
    return database_path
