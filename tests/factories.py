import factory
from django.contrib.auth.models import User
from django.utils import timezone

from henlo_app.models import Translation


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%s' % n)


class TranslationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Translation

    uuid = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
    original = 'cat'
    translation = 'кот'
    starred = False
    deleted = False
    added = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)
