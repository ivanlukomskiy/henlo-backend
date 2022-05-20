import json

import pytest
import pytz
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import APIRequestFactory

from henlo_app.models import Translation
from henlo_app.serializers import TranslationSerializer
from henlo_app.views import sync_view
from tests.factories import TranslationFactory

pytestmark = pytest.mark.django_db

tz = pytz.FixedOffset(180)


def test_sync_empty():
    api_factory = APIRequestFactory()
    request = api_factory.post('/sync/', data=[], format='json')
    response = sync_view(request)
    assert response.status_code == 200
    translations = json.loads(response.content)
    assert translations == []


def call_sync(data):
    api_factory = APIRequestFactory()
    request = api_factory.post('/sync/', data=data, format='json')
    response = sync_view(request)
    assert response.status_code == 200
    return json.loads(response.content)


def sync_and_get(translation, hour=0):
    with freeze_time(timezone.datetime(2021, 1, 2, hour=hour, tzinfo=tz)):
        translations = call_sync([translation])
        assert len(translations) == 1
        return translations[0]


def test_sync_new():
    with freeze_time(timezone.datetime(2021, 1, 2, hour=0, tzinfo=tz)):
        test_translation = TranslationSerializer(TranslationFactory()).data

    translation = sync_and_get(test_translation, hour=1)
    assert translation == test_translation


def test_update():
    with freeze_time(timezone.datetime(2021, 1, 1, hour=0, tzinfo=tz)):
        t = TranslationFactory()  # ok, FakeDatetime(2020, 12, 31, 21, 0, tzinfo=datetime.timezone.utc)
        t.save()

    # update all fields, make sure all changes applied
    test_translation = TranslationSerializer(Translation.objects.last()).data
    test_translation['added'] = int(timezone.datetime(2021, 1, 1, hour=1, tzinfo=tz).timestamp() * 1000)
    test_translation['updated'] = int(timezone.datetime(2021, 1, 1, hour=2, tzinfo=tz).timestamp() * 1000)
    test_translation['starred'] = True
    test_translation['deleted'] = True
    test_translation['original'] = 'dog'
    test_translation['translation'] = 'пёс'

    translation = sync_and_get(test_translation, hour=3)
    assert test_translation == translation

    # update a single field, make sure its saved
    test_translation['starred'] = False
    test_translation['updated'] = int(timezone.datetime(2021, 1, 1, hour=3, tzinfo=tz).timestamp() * 1000)

    translation = sync_and_get(test_translation, hour=4)
    assert test_translation == translation

    # older update should be ignored
    test_translation['starred'] = True
    test_translation['updated'] = int(timezone.datetime(2021, 1, 1, hour=1, tzinfo=tz).timestamp() * 1000)

    translation = sync_and_get(test_translation, hour=5)
    assert translation['starred'] is False

    # updates with the same timestamp should be ignored
    test_translation['starred'] = True
    test_translation['updated'] = translation['updated']

    translation = sync_and_get(test_translation, hour=6)
    assert translation['starred'] is False


def test_no_update_time():
    with freeze_time(timezone.datetime(2021, 1, 2, hour=0, tzinfo=tz)):
        translation = TranslationSerializer(TranslationFactory()).data

    del translation['updated']
    translation = sync_and_get(translation, hour=1)
    assert translation['updated'] / 1000 == timezone.datetime(2021, 1, 2, hour=1, tzinfo=tz).timestamp()
