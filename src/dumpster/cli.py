from cyclopts import App
from rich.console import Console

from dumpster.database.connection import ConnectionArgs, ConnectionQuery
from dumpster.database.postgres import PostgresqlConnection


console = Console()
app = App(
    name="dumpster",
    help="Keep track of local database state without worry.",
    help_format="md",
    console=console,
)


@app.command
def dump(
    *,
    database_type: str,
    database_name: str,
    host: str = "127.0.0.1",
    port: int | None = None,
    username: str | None = None,
    password: str | None = None,
    query: ConnectionQuery | None = None,
):
    """Create a json formatted database dump

    Parameters
    ----------
    database_type: str
        Name of the DBMS being used. Ex. 'postgres'
    database_name: str
        Name of the database. Ex. 'my_database'
    host: str
        Host IP of the database. Ex. 'localhost'
    port: str
        Port number used to connect. Ex. 5432
    username: str
        Username used to access the database. Ex. 'my_username'
    password: str
        Password of user used to access database, requires username. Ex. 'my_p@ssword'
    query: ConnectionQuery
        A query string to pass at the end of the constructed connection string. Ex. {'param': 'val'}
    """

    if database_name is None or database_type is None:
        raise Exception

    if password is not None and username is None:
        raise Exception

    connection_query = ConnectionArgs(
        database=database_name,
        host=host,
        port=port,
        username=username,
        password=password,
        query=query,
    )

    # handle which connection class

    db = PostgresqlConnection(connection_query, auto_inspect=True)

    print(db.tables)


if __name__ == "__main__":
    try:
        app()
    except Exception:
        console.print_exception()
