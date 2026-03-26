from enum import Enum


class TempFilesRoutes(str, Enum):
    """Temporary Files service routes."""

    GET_FILE = "/api/temporary_files/v1/get_file"
    CLEANUP = "/api/temporary_files/v1/cleanup"

    def __str__(self) -> str:
        return self.value
