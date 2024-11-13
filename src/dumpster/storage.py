from pathlib import Path


def storage_dir() -> Path:
    # TODO: consider configurations (CLI flag, config file)
    # TODO: check for storage config here
    configured_path = None
    if configured_path:
        storage_path = Path(configured_path)
    else:
        storage_path = Path().cwd() / ".dumpster"

    if storage_path.is_dir:
        return storage_path

    storage_path.mkdir()
    return storage_path
