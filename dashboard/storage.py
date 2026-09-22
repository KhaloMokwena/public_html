import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class PrivateStorage(FileSystemStorage):
    """
    For files that must never be public (candidate CVs).
    They live outside MEDIA_ROOT, have no URL, and are only handed out by a staff-only view in /manage/.
    """

    @property
    def base_location(self):
        return getattr(settings, 'PRIVATE_MEDIA_ROOT', settings.BASE_DIR / 'private_uploads')

    @property
    def location(self):
        return os.path.abspath(self.base_location)

    @property
    def base_url(self):
        return None


def get_private_storage():
    return PrivateStorage()
