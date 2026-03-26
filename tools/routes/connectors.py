from enum import Enum


class GmailConnectorRoutes(str, Enum):
    """Gmail Connector service routes."""

    GET_SCAN_TASKS = "/api/gmail_connector/get_scan_tasks"

    def __str__(self) -> str:
        return self.value


class GoogleDriveConnectorRoutes(str, Enum):
    """Google Drive Connector service routes."""

    GET_SCAN_TASKS = "/api/google_drive_connector/get_scan_tasks"

    def __str__(self) -> str:
        return self.value


class SharepointConnectorRoutes(str, Enum):
    """SharePoint Connector service routes."""

    GET_SCAN_TASKS = "/api/sharepoint_connector/get_scan_tasks"

    def __str__(self) -> str:
        return self.value


class LeadspottingConnectorRoutes(str, Enum):
    """Leadspotting Connector service routes."""

    GET_SCAN_TASKS = "/api/leadspotting_connector/get_scan_tasks"

    def __str__(self) -> str:
        return self.value
