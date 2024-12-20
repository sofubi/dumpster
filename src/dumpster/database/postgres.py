from typing import Any
from urllib.parse import quote_plus, urlencode


def postgres_conn_string(
    host: str,
    dbname: str,
    user: str | None = None,
    password: str | None = None,
    port: str | None = None,
    query_args: dict[str, Any] | None = None,
) -> str:
    host = f"{host}"
    dbname = f"/{dbname}"

    if port:
        port = f":{port}"
    else:
        port = ""

    if user:
        if not password:
            host = f"@{host}"
        user = f"{user}"
    else:
        user = ""

    if password:
        escaped_password = quote_plus(password)
        password = f":{escaped_password}"

        host = f"@{host}"
    else:
        password = ""

    extra_args = ""
    if query_args:
        extra_args = urlencode(query_args)

    return f"{user}{password}{host}{port}{dbname}{extra_args}".strip()
