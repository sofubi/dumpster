import pytest

from dumpster.database.postgres import PostgresConnection


@pytest.fixture
def pg_connection():
    connection = PostgresConnection(
        "localhost",
        "test_db",
    )

    return connection


def test_build_conninfo(pg_connection):
    conninfo = pg_connection._build_conninfo()

    assert conninfo == "host=localhost dbname=test_db"
