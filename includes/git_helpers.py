import os


class GitHelper:
    @staticmethod
    def _check_local_path(path: str) -> bool:
        # does path exist
        return os.path.isdir(path)

    @staticmethod
    def _create_local_path(path) -> None:
        # Create path
        from pathlib import Path

        return Path(path).mkdir(parents=True, exist_ok=True)
