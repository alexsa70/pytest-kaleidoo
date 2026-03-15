from enum import Enum


class OrgRoutes(str, Enum):
    """Organization routes."""

    ORG_GET = "/api/org/get"
    ORG_GET_MODELS = "/api/org/get_models"
    ORG_CREATE = "/api/org/create"
    ORG_UPDATE = "/api/org/update"
    ORG_UPDATE_CAPABILITIES = "/api/org/update_org_capabilities"
    ORG_UPDATE_SSO = "/api/org/update_org_sso"
    ORG_DELETE = "/api/org/delete"
    ORG_GET_ALL = "/api/org/get_all"
    ORG_CREATE_LICENSE = "/api/org/create_license"
    ORG_UPDATE_LICENSE = "/api/org/update_license"
    ORG_GET_LICENSE = "/api/org/get_license"
    ORG_SET_PRIORITY_TABLE = "/api/org/set_priority_table"
    ORG_BALANCE_PRIORITIES = "/api/org/balance_org_priorities"

    def __str__(self) -> str:
        return self.value
