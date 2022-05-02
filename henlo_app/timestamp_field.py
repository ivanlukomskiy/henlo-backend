from datetime import datetime

from django.utils.timezone import make_aware
from rest_framework import serializers


class TimestampField(serializers.DateTimeField):
    def to_representation(self, value):
        return int(value.timestamp() * 1000)

    def to_internal_value(self, value):
        res = make_aware(datetime.fromtimestamp(float('%s' % value) / 1000))
        return res
