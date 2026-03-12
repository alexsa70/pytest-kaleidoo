from __future__ import annotations

from schema.rbac import AccessRule


# Add rules here as you onboard user-management endpoints.
# Example:
# AccessRule(
#     name="Users: list",
#     method="GET",
#     path="/api/users",
#     allowed_roles=["super_admin", "admin", "user"],
#     denied_roles=[],
#     expected_allowed_status=200,
# )
ACCESS_POLICY_USERS: list[AccessRule] = []
