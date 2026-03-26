from enum import Enum


class FilesRoutes(str, Enum):
    """Files service routes."""

    GET_FILE_METADATA = "/api/files/get_file_metadata"
    GET_FILE_DETAILS = "/api/files/get_file_details"
    GET_FILES = "/api/files/get_files"
    GET_FILES_BY_IDS = "/api/files/get_files_by_ids"
    UPDATE_FILE_DETAILS = "/api/files/update_file_details"
    EDIT_FILES_PERMISSIONS = "/api/files/edit_files_permissions"
    GET_FILE_PERMISSIONS = "/api/files/get_file_permissions"

    def __str__(self) -> str:
        return self.value
