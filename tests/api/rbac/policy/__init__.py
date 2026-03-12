from tests.api.rbac.policy.auth import ACCESS_POLICY_AUTH
from tests.api.rbac.policy.org import ACCESS_POLICY_ORG
from tests.api.rbac.policy.users import ACCESS_POLICY_USERS

ACCESS_POLICY = [
    *ACCESS_POLICY_AUTH,
    *ACCESS_POLICY_ORG,
    *ACCESS_POLICY_USERS,
]

__all__ = [
    "ACCESS_POLICY",
    "ACCESS_POLICY_AUTH",
    "ACCESS_POLICY_ORG",
    "ACCESS_POLICY_USERS",
]
