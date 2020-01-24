from rest_framework import serializers

from .timestamp_field import TimestampField
from .models import Translation


class TranslationSerializer(serializers.ModelSerializer):
    added = TimestampField()
    updated = TimestampField(required=False, default=None, allow_null=True)
    deleted = serializers.BooleanField(required=False, default=False)
    starred = serializers.BooleanField(required=False, default=False)
    class Meta:
        model = Translation
        fields = ['uuid', 'original', 'translation', 'added', 'updated', 'starred', 'deleted']
        extra_kwargs = {
            'uuid': {'validators': []},
        }
