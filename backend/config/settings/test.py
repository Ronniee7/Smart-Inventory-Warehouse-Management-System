"""Test settings for StockPilot."""
from .base import *  # noqa: F401,F403

DEBUG = False

# Tests must not depend on production secrets.
SECRET_KEY = "test-secret-key-not-for-production"

# Use a fast password hasher in tests.
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

ALLOWED_HOSTS = ["*"]

# Keep the database from base (PostgreSQL via DATABASE_URL / default).
# Tests requiring Postgres need a running instance; see development-setup.md.
