from enum import Enum


class ManualLoaderRoutes(str, Enum):
    """Manual Loader service routes."""

    UPLOAD_MANUAL_FILE = "/api/manual_loader/upload_manual_file"
    DELETE_MANUAL_FILES = "/api/manual_loader/delete_manual_files"

    def __str__(self) -> str:
        return self.value
