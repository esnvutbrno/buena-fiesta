import hashlib
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.utils.encoding import filepath_to_uri
from django.utils.timezone import now

from apps.utils.models import BaseModel


class NamespacedFilesStorage(FileSystemStorage):
    storages = []

    def __init__(self, namespace: str):
        self.namespace = namespace.strip("/")
        super().__init__(location=settings.MEDIA_ROOT / namespace)
        self.storages.append(self)

    @property
    def url_name_suffix(self):
        return f"serve-{self.namespace}"

    def url(self, name):
        return reverse(
            f"files:{self.url_name_suffix}", kwargs=dict(name=filepath_to_uri(name))
        )

    def serve_url(self, name):
        return urljoin(settings.MEDIA_URL, f"{self.namespace}/{filepath_to_uri(name)}")

    @staticmethod
    def upload_to(instance: BaseModel, filename: str) -> str:
        try:
            # for BaseTimestampedModel
            modified = instance.modified.isoformat()
        except AttributeError:
            modified = now().isoformat()

        return hashlib.sha256(f"{instance.pk}-{modified}".encode()).hexdigest()
