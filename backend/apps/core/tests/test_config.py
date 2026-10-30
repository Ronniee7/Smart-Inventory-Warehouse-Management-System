"""Tests for Django configuration loading."""
from django.conf import settings


def test_settings_module_loads():
    assert settings.configured
    assert settings.DEBUG is False or settings.DEBUG is True


def test_installed_apps_include_core():
    assert "apps.core" in settings.INSTALLED_APPS


def test_rest_framework_defaults():
    assert "DEFAULT_PERMISSION_CLASSES" in settings.REST_FRAMEWORK
    assert settings.REST_FRAMEWORK["PAGE_SIZE"] == 25
