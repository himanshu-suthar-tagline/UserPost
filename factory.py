#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from fastapi import FastAPI

from config import Settings
from routers.api import router

logger = logging.getLogger(__name__)
API_PREFIX = "/api"


def create_fastapi(settings: Settings):
    kwargs = {}

    app = FastAPI(title="User Post", dependencies=[], **kwargs)

    app.include_router(router, prefix=API_PREFIX)

    return app
