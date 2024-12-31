from typing import Generator
from sqlalchemy import URL, Engine, Table, create_engine, text
from testcontainers.postgres import PostgresContainer
import pytest

from dumpster.database.connection import ConnectionArgs
from dumpster.database.postgres import PostgresqlConnection


def seed_postgres(engine: Engine) -> None:
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
def postgres_container() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer("postgres:16", driver=None) as postgres:
        yield postgres


@pytest.fixture(scope="session")
def postgres_seeded_engine(postgres_container: PostgresContainer) -> ConnectionArgs:
    conn_args = build_conn_args(postgres_container)
    url = URL.create(
        "postgresql+psycopg",
        username=conn_args.username,
        password=conn_args.password,
        host=conn_args.host,
        port=conn_args.port,
        database=conn_args.database,
    )
    engine: Engine = create_engine(url)
    seed_postgres(engine)
    return conn_args


def build_conn_args(container: PostgresContainer) -> ConnectionArgs:
    return ConnectionArgs(
        username=container.username,
        password=container.password,
        database=container.dbname,
        port=int(container.get_exposed_port(5432)),
        host="localhost",
    )


def test_get_engine(postgres_container: PostgresContainer):
    conn_args = build_conn_args(postgres_container)
    conn_class = PostgresqlConnection(conn_args)
    engine = conn_class._get_engine()
    assert isinstance(engine, Engine)


def test_fetch_schemas(postgres_seeded_engine: ConnectionArgs):
    conn_class = PostgresqlConnection(postgres_seeded_engine)
    schemas = conn_class._fetch_schemas()
    assert sorted(schemas) == sorted(
        ["information_schema", "public", "test_schema_a", "test_schema_b"]
    )


def test_table_list(postgres_seeded_engine: ConnectionArgs):
    conn_class = PostgresqlConnection(postgres_seeded_engine)
    tables = conn_class.table_list("public")
    assert sorted(tables) == sorted(["test_public"])


def test_table_from_meta(postgres_seeded_engine: ConnectionArgs):
    conn_class = PostgresqlConnection(postgres_seeded_engine)
    table = conn_class.table_from_meta("public", "test_public")
    assert isinstance(table, Table)
    assert table.name == "test_public"
