from orbidi.settings.base import *  # noqa: F401,F403


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": ":memory:",
    }
}
