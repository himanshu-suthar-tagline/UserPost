#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    # Can be generated like this: openssl rand -hex 32
    secret_key: str = secrets.token_hex(16)
    # Configuration for JWT.
    access_token_expire_minutes: int = 30
    jwt_algorithm: str = "HS512"

    # Disable OpenAPI and interactive documentation by default.
    openapi_routes: bool = True
