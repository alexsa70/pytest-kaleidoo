from enum import Enum


class TagIngestRoutes(str, Enum):
    """Tag ingest (write) service routes."""

    CREATE = "/api/tag_ingest/create"
    UPDATE = "/api/tag_ingest/update"
    DELETE = "/api/tag_ingest/delete"
    TAG_FILES = "/api/tag_ingest/tag_files"
    UNLINK_TAG_FILES = "/api/tag_ingest/unlink_tag_files"
    TAG_FOLDERS = "/api/tag_ingest/tag_folders"
    UNLINK_TAG_FOLDERS = "/api/tag_ingest/unlink_tag_folders"
    PROMOTE_TO_ALBUM = "/api/tag_ingest/promote_to_album"
    DEMOTE_TO_REGULAR = "/api/tag_ingest/demote_to_regular"

    def __str__(self) -> str:
        return self.value


class TagQueryRoutes(str, Enum):
    """Tag query (read) service routes."""

    GET = "/api/tag_query/get"
    GET_TAGS = "/api/tag_query/get_tags"
    GET_TAGS_BY_OBJECT_ID = "/api/tag_query/get_tags_by_object_id"
    GET_OBJECTS_BY_TAGS = "/api/tag_query/get_objects_by_tags"
    GET_OBJECTS_BY_TAG_NAME = "/api/tag_query/get_objects_by_tag_name"

    def __str__(self) -> str:
        return self.value
