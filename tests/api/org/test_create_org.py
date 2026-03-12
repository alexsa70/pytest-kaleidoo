import base64
from http import HTTPStatus

import allure
import pytest

from clients.operations_client import APIClient
from config import APISettings as Settings
from schema.organizations import (
    CreateOrgRequestSchema,
    CreateOrgResponseSchema,
    CreateOrgValidationErrorSchema,
    PermissionsSchema,
    FilesAccessPermissionsSchema,
    CachePermissionsSchema,
)
from tools.assertions.base import assert_status_code
from tools.fakers import fake_org_name, fake_domain, fake_email, fake_username, fake_first_name, fake_last_name

VALID_COLORS = [
    "blue", "mint", "green", "yellow", "orange", "red",
    "lightGrey", "grey", "black", "electricBlue", "royalPurple", "pink",
]

# Minimal 1x1 PNG
PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8"
    "z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg=="
)

# Minimal GIF (invalid logo format)
GIF_BYTES = b"GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;"


def base_org_payload(settings: Settings) -> CreateOrgRequestSchema:
    return CreateOrgRequestSchema(
        org_name=fake_org_name(),
        domain=fake_domain(),
        admin_email=fake_email(),
        user_name=fake_username(),
        first_name=fake_first_name(),
        last_name=fake_last_name(),
        role_id=settings.org_role_id or "507f1f77bcf86cd799439022",
    )


@pytest.mark.api
@pytest.mark.org
@pytest.mark.integration
@allure.feature("Organizations")
@allure.story("Create Organization")
class TestCreateOrgPositive:

    @allure.title("Create Org: required fields only → 200 + org_id")
    async def test_create_org_required_fields(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        response = await api_client.create_org(payload, token=auth_token)
        assert_status_code(response.status_code, HTTPStatus.OK)
        body = CreateOrgResponseSchema.model_validate_json(response.text)
        assert body.message == "Organization created successfully"
        assert body.org_id

    @allure.title("Create Org: with org_description → 200")
    async def test_create_org_with_description(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.org_description = "Test organization description"
        response = await api_client.create_org(payload, token=auth_token)
        assert_status_code(response.status_code, HTTPStatus.OK)

    @allure.title("Create Org: color='{color}' → 200")
    @pytest.mark.parametrize("color", VALID_COLORS)
    async def test_create_org_valid_colors(
        self, api_client: APIClient, auth_token: str, settings: Settings, color: str,
    ) -> None:
        payload = base_org_payload(settings)
        payload.org_color = color
        response = await api_client.create_org(payload, token=auth_token)
        assert_status_code(response.status_code, HTTPStatus.OK)

    @allure.title("Create Org: default_language=english → 200")
    async def test_create_org_language_english(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.default_language = "english"
        response = await api_client.create_org(payload, token=auth_token)
        assert_status_code(response.status_code, HTTPStatus.OK)

    @allure.title("Create Org: default_language=hebrew → 200")
    async def test_create_org_language_hebrew(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.default_language = "hebrew"
        response = await api_client.create_org(payload, token=auth_token)
        assert_status_code(response.status_code, HTTPStatus.OK)

    @allure.title("Create Org: PNG logo upload → 200")
    async def test_create_org_with_png_logo(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        response = await api_client.create_org(
            payload, token=auth_token,
            logo=PNG_BYTES, logo_filename="logo.png", logo_content_type="image/png",
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

    @allure.title("Create Org: permissions.files_access.manual_public=true → 200")
    async def test_create_org_with_permissions_files_access(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.permissions = PermissionsSchema(
            files_access=FilesAccessPermissionsSchema(manual_public=True)
        )
        response = await api_client.create_org(payload, token=auth_token)
        assert_status_code(response.status_code, HTTPStatus.OK)

    @allure.title("Create Org: permissions.cache with valid ttl → 200")
    async def test_create_org_with_permissions_cache(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.permissions = PermissionsSchema(
            cache=CachePermissionsSchema(user_acl_ttl=2400, user_acl_refresh_gap_ttl=1200)
        )
        response = await api_client.create_org(payload, token=auth_token)
        assert_status_code(response.status_code, HTTPStatus.OK)


@pytest.mark.api
@pytest.mark.org
@pytest.mark.integration
@allure.feature("Organizations")
@allure.story("Create Organization – Validation")
class TestCreateOrgValidation:

    @allure.title("Create Org: duplicate org_name → 400")
    async def test_create_org_duplicate_name(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.org_name = "duplicate-org-test-fixed"
        await api_client.create_org(payload, token=auth_token)

        payload2 = base_org_payload(settings)
        payload2.org_name = "duplicate-org-test-fixed"
        response = await api_client.create_org(payload2, token=auth_token)

        assert response.status_code == HTTPStatus.BAD_REQUEST.value

    @allure.title("Create Org: org_description > 150 chars → 422")
    async def test_create_org_description_too_long(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.org_description = "x" * 151
        response = await api_client.create_org(payload, token=auth_token)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value
        body = CreateOrgValidationErrorSchema.model_validate_json(response.text)
        assert any("150" in e or "org_description" in e for e in body.validation_errors)

    @allure.title("Create Org: org_description exactly 150 chars → 200 (boundary)")
    async def test_create_org_description_boundary_150(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.org_description = "x" * 150
        response = await api_client.create_org(payload, token=auth_token)
        assert_status_code(response.status_code, HTTPStatus.OK)

    @allure.title("Create Org: invalid admin_email → 422")
    async def test_create_org_invalid_email(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.admin_email = "not-an-email"
        response = await api_client.create_org(payload, token=auth_token)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value

    @allure.title("Create Org: invalid org_color → 400/422")
    async def test_create_org_invalid_color(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.org_color = "neon_rainbow"
        response = await api_client.create_org(payload, token=auth_token)
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("Create Org: GIF logo → 400 invalid format")
    async def test_create_org_gif_logo_rejected(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        response = await api_client.create_org(
            payload, token=auth_token,
            logo=GIF_BYTES, logo_filename="logo.gif", logo_content_type="image/gif",
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST.value

    @allure.title("Create Org: cache user_acl_ttl < 900 → 422")
    async def test_create_org_cache_ttl_below_minimum(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.permissions = PermissionsSchema(
            cache=CachePermissionsSchema(user_acl_ttl=899)
        )
        response = await api_client.create_org(payload, token=auth_token)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value

    @allure.title("Create Org: refresh_gap >= ttl → 422")
    async def test_create_org_refresh_gap_exceeds_ttl(
        self, api_client: APIClient, auth_token: str, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        payload.permissions = PermissionsSchema(
            cache=CachePermissionsSchema(user_acl_ttl=1800, user_acl_refresh_gap_ttl=1800)
        )
        response = await api_client.create_org(payload, token=auth_token)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value

    @allure.title("Create Org: missing field '{field}'")
    @pytest.mark.parametrize("field", [
        "org_name", "domain", "admin_email",
        "user_name", "first_name", "last_name", "role_id",
    ])
    async def test_create_org_missing_required_field(
        self, api_client: APIClient, auth_token: str, settings: Settings, field: str,
    ) -> None:
        data = base_org_payload(settings).model_dump(exclude_none=True)
        del data[field]
        response = await api_client.post(
            "/api/org/create",
            data=data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )


@pytest.mark.api
@pytest.mark.org
@pytest.mark.integration
@allure.feature("Organizations")
@allure.story("Create Organization – Authorization")
class TestCreateOrgAuthorization:

    @allure.title("Create Org: no token → 401")
    async def test_create_org_no_token(
        self, api_client: APIClient, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        response = await api_client.post(
            "/api/org/create",
            data=payload.model_dump(exclude_none=True),
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED.value

    @allure.title("Create Org: invalid token → 401")
    async def test_create_org_invalid_token(
        self, api_client: APIClient, settings: Settings,
    ) -> None:
        payload = base_org_payload(settings)
        response = await api_client.create_org(payload, token="invalid.token.here")
        assert response.status_code == HTTPStatus.UNAUTHORIZED.value
