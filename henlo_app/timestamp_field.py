import pytz
from django.utils import timezone
from rest_framework import serializers


class TimestampField(serializers.DateTimeField):
    def to_representation(self, value):
        return int(value.timestamp() * 1000)

    def to_internal_value(self, value):
        return timezone.datetime.fromtimestamp(value / 1000, tz=pytz.UTC)
