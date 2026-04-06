from __future__ import annotations

from typing import Optional

import pyotp
import pytest

from config import APISettings as Settings
from schema.auth import LoginRequestSchema


def _require_auth_credentials(settings: Settings) -> None:
    if settings.auth_credentials is None:
        pytest.skip("AUTH_CREDENTIALS not set in .env")

def _make_login_payload(
    settings: Settings, 
    *,
     otp_code: Optional[str] = None,
     auto_generate_otp: bool = False,     
     ) -> LoginRequestSchema:
    """
    Builder payload для /login.
    auto_generate_otp=True: если otp_secret есть, сгенерит TOTP и подставит otp_code.
    auto_generate_otp=False: otp_code будет либо задан явно, либо None (тогда otp_code не уйдёт в запрос).
    """
    _require_auth_credentials(settings)

    code = otp_code
    if code is None and auto_generate_otp and  settings.auth_credentials.otp_secret:
        code = pyotp.TOTP(settings.auth_credentials.otp_secret).now()

    return LoginRequestSchema(
        orgName=settings.org_name or "",
        identity=settings.auth_credentials.email,
        password=settings.auth_credentials.password,
        otp_code=code,
    )
    