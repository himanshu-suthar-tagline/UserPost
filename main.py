#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uvicorn

from dependencies import get_settings
from factory import create_fastapi

settings = get_settings()

app = create_fastapi(settings)
