from __future__ import annotations
import os
from typing import Literal


DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:qwerty@localhost:5432/proxy"
)
