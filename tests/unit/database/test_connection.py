from sqlalchemy import Engine, Table, create_engine, text
from testcontainers.postgres import PostgresContainer
import pytest

from dumpster.database.connection import (
    fetch_schemas,
    get_engine,
    table_from_meta,
    table_list,
)


# with PostgresContainer("postgres:16") as postgres:
#
#     engine = sqlalchemy.create_engine(postgres.get_connection_url())
#
#     with engine.begin() as connection:
#
#         result = connection.execute(sqlalchemy.text("select version()"))
#
#         version, = result.fetchone()


def seed_postgres(engine):
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA test_schema_a"))
        conn.execute(text("CREATE SCHEMA test_schema_b"))

        conn.execute(
            text(
                """
                CREATE TABLE public.test_public (
                    id   serial PRIMARY KEY,
                    name text,
                    age  integer
                );
                """
            )
        )
        conn.execute(
            text(
                """
                INSERT INTO public.test_public (name, age)
                VALUES
                    ('test teen', 18),
                    ('man test', 30),
                    ('baby test', 1);
                """
            )
        )

        conn.execute(
            text(
                """
                CREATE TABLE test_schema_a.test_a (
                    id   serial PRIMARY KEY,
                    name text,
                    age  integer
                );
                """
            )
        )
        conn.execute(
            text(
                """
                INSERT INTO public.test_public (name, age)
                VALUES
                    ('test lady', 50),
                    ('woman test', 30),
                    ('child test', 7);
                """
            )
        )

        conn.commit()


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def postgres_seeded_engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    seed_postgres(engine)
    yield engine


def test_get_engine(postgres_container):
    conn_string = postgres_container.get_connection_url()
    engine = get_engine("postgres", conn_string)
    assert isinstance(engine, Engine)


def test_fetch_schemas(postgres_seeded_engine):
    schemas = fetch_schemas(postgres_seeded_engine)
    assert sorted(schemas) == sorted(
        ["information_schema", "public", "test_schema_a", "test_schema_b"]
    )


def test_table_list(postgres_seeded_engine):
    tables = table_list(postgres_seeded_engine, "public")
    assert sorted(tables) == sorted(["test_public"])


def test_table_from_meta(postgres_seeded_engine):
    table = table_from_meta(postgres_seeded_engine, "public", "test_public")
    assert isinstance(table, Table)
    assert table.name == "test_public"
