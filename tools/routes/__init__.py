from tools.routes.agents import AgentsRoutes
from tools.routes.auth import AuthRoutes
from tools.routes.connectors import (
    GmailConnectorRoutes,
    GoogleDriveConnectorRoutes,
    LeadspottingConnectorRoutes,
    SharepointConnectorRoutes,
)
from tools.routes.conversation import ConversationRoutes
from tools.routes.files import FilesRoutes
from tools.routes.folders import FoldersRoutes
from tools.routes.integration import IntegrationRoutes
from tools.routes.manual_loader import ManualLoaderRoutes
from tools.routes.online_call import OnlineCallServerEvents, OnlineCallSocketEvents
from tools.routes.org import OrgRoutes
from tools.routes.product import ProductRoutes
from tools.routes.project_source import ProjectSourceRoutes
from tools.routes.tags import TagIngestRoutes, TagQueryRoutes
from tools.routes.temp_files import TempFilesRoutes
from tools.routes.users import UserRoutes

__all__ = [
    "AgentsRoutes",
    "AuthRoutes",
    "ConversationRoutes",
    "FilesRoutes",
    "FoldersRoutes",
    "GmailConnectorRoutes",
    "GoogleDriveConnectorRoutes",
    "IntegrationRoutes",
    "LeadspottingConnectorRoutes",
    "ManualLoaderRoutes",
    "OnlineCallServerEvents",
    "OnlineCallSocketEvents",
    "OrgRoutes",
    "ProductRoutes",
    "ProjectSourceRoutes",
    "SharepointConnectorRoutes",
    "TagIngestRoutes",
    "TagQueryRoutes",
    "TempFilesRoutes",
    "UserRoutes",
]
