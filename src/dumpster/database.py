import logging
import sys
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from shutil import which
from subprocess import STDOUT, Popen
from typing import NamedTuple, NoReturn

from dumpster.storage import storage_dir
from dumpster.main import dumpster_obj

console = dumpster_obj.console

# TODO: Better logging config / not DEBUG by default
logger = logging.getLogger(__name__)
logging.basicConfig(filename="dump.log", encoding="utf-8", level=logging.DEBUG)


class DumpCommand(NamedTuple):
    root: str
    outfile_flag: str
    extras: list[str] | None = None


# TODO: Look at useful dump command defaults for each
command_map: dict[str, DumpCommand] = {
    "postgresql": DumpCommand(root="pg_dump", outfile_flag="-f"),
    "mysql": DumpCommand(root="mysqldump", outfile_flag="-r"),
    "sqlite3": DumpCommand(root="sqlite3", outfile_flag="-f"),
    "mariadb": DumpCommand(root="mariadb-dump", outfile_flag="-r"),
}


class DBMS(str, Enum):
    POSTGRES = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite3"
    MARIADB = "mariadb"


class Dump:
    def __init__(self, dbms: DBMS, db_path: str) -> None:
        self.db_type: str = dbms.value
        self.db_path: Path = Path(db_path)
        self.storage_dir: Path = storage_dir()
        self.created: bool = False
        self.command: DumpCommand = command_map[self.db_type]

    def _dtnow_aware(self) -> str:
        dtnow = datetime.now(timezone.utc)
        return dtnow.strftime("YYYY-MM-DD")

    def _filename(self) -> str:
        return f"{self.db_path.name}-dump-{self._dtnow_aware()}"

    def create(self) -> NoReturn:
        dump_path = self.storage_dir / f"{self._filename()}.sql"
        command_path = which(self.command.root)
        if command_path:
            command_path = Path(command_path)
        # TODO: fix handling here
        else:
            raise Exception
        try:
            # TODO: Make sure that logs don't pile up
            # TODO: Offer logging opt out (probably should be opt in)
            output_capture = storage_dir() / f"{self._filename()}.log"
            with open(output_capture, "w") as log:
                Popen(
                    [
                        self.command.root,
                        self.db_path,
                        self.command.outfile_flag,
                        dump_path,
                    ],
                    stdout=log,
                    stderr=STDOUT,
                )
            # TODO: Need better printing / config setup for rich
            console.print("SUCCESS")
            sys.exit(0)
        except Exception:
            # TODO: Handle for ValueError, SubprocessError
            raise
