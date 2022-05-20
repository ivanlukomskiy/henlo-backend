from django.utils import timezone
from rest_framework import serializers

from .timestamp_field import TimestampField
from .models import Translation


class TranslationSerializer(serializers.ModelSerializer):
    original = serializers.CharField(allow_blank=True, required=False, default='', max_length=500)
    translation = serializers.CharField(allow_blank=True, required=False, default='', max_length=500)
    added = TimestampField()
    updated = TimestampField(default=timezone.now)
    deleted = serializers.BooleanField(required=False, default=False)
    starred = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = Translation
        fields = ['uuid', 'original', 'translation', 'added', 'updated', 'starred', 'deleted']
        extra_kwargs = {
            'uuid': {'validators': []},
        }
