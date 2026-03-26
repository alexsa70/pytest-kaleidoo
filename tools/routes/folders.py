from enum import Enum


class FoldersRoutes(str, Enum):
    """Folders service routes."""

    GET_ALL = "/api/folders/get_all"
    GET_FOLDERS = "/api/folders/get_folders"
    GET = "/api/folders/get"
    CREATE = "/api/folders/create"
    UPDATE = "/api/folders/update"
    DELETE = "/api/folders/delete"
    ASSOCIATE_FILES = "/api/folders/associate_files_to_folder"
    DISASSOCIATE_FILES = "/api/folders/disassociate_files_from_folder"
    GET_FILES_BY_FOLDERS = "/api/folders/get_files_by_folders"
    GET_FOLDERS_BY_FILES = "/api/folders/get_folders_by_files"
    ASSOCIATE_AGENTS = "/api/folders/associate_agents_to_folder"
    ASSOCIATE_AGENT_TO_FOLDERS = "/api/folders/associate_agent_to_folders"
    DISASSOCIATE_AGENTS = "/api/folders/disassociate_agents_from_folder"
    GET_AGENTS_BY_FOLDERS = "/api/folders/get_agents_by_folders"
    GET_FOLDERS_BY_AGENTS = "/api/folders/get_folders_by_agents"
    REMOVE_AUTO_SUBFOLDER = "/api/folders/remove_auto_subfolder"

    def __str__(self) -> str:
        return self.value
