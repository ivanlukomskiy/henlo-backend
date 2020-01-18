import uuid as uuid

from django.db import models


class Translation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    original = models.CharField(max_length=500)
    translation = models.CharField(max_length=500)
    added = models.DateTimeField()
    updated = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)