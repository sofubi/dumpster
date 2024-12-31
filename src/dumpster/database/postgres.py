from sqlalchemy import URL, Engine, MetaData, Table, create_engine, inspect
from dumpster.database.connection import ConnectionArgs, ConnectionPrefix, DbConnection


class PostgresqlConnection(DbConnection):
    def __init__(
        self, connection_args: ConnectionArgs, auto_inspect: bool = False
    ) -> None:
        super().__init__(connection_args)

        self.conn_prefix = ConnectionPrefix.POSTGRES
        self.engine = self._get_engine()

        self.meta = MetaData()

        self._schemas = []
        self._tables = {}

        if auto_inspect is True:
            self.map_schemas_tables()

    def _get_engine(self) -> Engine:
        url = URL.create(
            self.conn_prefix,
            username=self.connection_args.username,
            password=self.connection_args.password,
            host=self.connection_args.host,
            port=self.connection_args.port,
            database=self.connection_args.database,
            query=self.connection_args.query,
        )
        return create_engine(url)

    def _fetch_schemas(self) -> list[str]:
        try:
            inspector = inspect(self.engine)
            return inspector.get_schema_names()

        except Exception:
            raise

    def _refresh_schemas(self) -> None:
        updated_schemas = self._fetch_schemas()
        if len(set(updated_schemas) - set(self._schemas)) > 0:
            self._schemas = updated_schemas

    def table_list(self, schema: str) -> list[str]:
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names(schema)

        except Exception:
            raise

    def map_schemas_tables(self) -> dict[str, list[str]]:
        self._refresh_schemas()

        mapping: dict[str, list] = {}
        for schema in self._schemas:
            mapping[schema] = self.table_list(schema)

        return mapping

    def table_from_meta(self, schema: str, table: str) -> Table:
        return Table(table, self.meta, schema=schema, autoload_with=self.engine)

    def load_schema_tables(self, schemas: list | None = None) -> dict[str, list[Table]]:
        if schemas is None:
            self._refresh_schemas()
            schemas = self._schemas

        mapping: dict[str, list[Table]] = {}
        for schema in schemas:
            schema_entry = mapping[schema] = []
            for table in self._tables[schema]:
                schema_entry.append(self.table_from_meta(schema, table))

        return mapping
