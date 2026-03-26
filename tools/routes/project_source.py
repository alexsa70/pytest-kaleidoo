from enum import Enum


class ProjectSourceRoutes(str, Enum):
    """Connectors - Project Source service routes."""

    CREATE_AUTH_URL = "/api/project_source/create_auth_url"
    CREATE_CONNECTOR = "/api/project_source/create_connector"
    CREATE_SCAN_TASKS = "/api/project_source/create_scan_tasks"
    LIST_BY_ORG = "/api/project_source/list_by_org"
    DELETE = "/api/project_source/delete"
    CONNECT_SYNC = "/api/project_source/connect_sync"
    DISCONNECT_SYNC = "/api/project_source/disconnect_sync"
    UPDATE_SYNC_HOUR = "/api/project_source/update_sync_hour"
    VALIDATE_SOURCE_PATH = "/api/project_source/validate_source_path"
    GET_SUPPORTED_FILE_TYPES = "/api/project_source/get_supported_file_types"

    def __str__(self) -> str:
        return self.value
