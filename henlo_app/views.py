import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import Translation
from .serializers import TranslationSerializer

logger = logging.getLogger(__name__)


@csrf_exempt
def sync_view(request):
    if request.method == 'GET':
        translations = Translation.objects.filter(deleted=False)
        serializer = TranslationSerializer(translations, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TranslationSerializer(data=data, many=True)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400, safe=False)

        sync(serializer.validated_data)

        serializer = TranslationSerializer(Translation.objects.all(), many=True)
        return JsonResponse(serializer.data, status=200, safe=False)


def sync(translations):
    server_translations = {str(translation.uuid): translation for translation in Translation.objects.all()}
    client_translations = {str(translation['uuid']): translation for translation in translations}

    translations_to_update = []
    translations_to_create = []

    # Update translations on server side
    for translation in client_translations.values():
        uuid = str(translation['uuid'])
        if uuid in server_translations:
            server_translation = server_translations[uuid]

            if server_translation.updated >= translation['updated']:
                print(f'{server_translation.updated} > {translation["updated"]}')
                continue

            server_translation.updated = translation['updated']
            server_translation.added = translation['added']
            server_translation.original = translation['original']
            server_translation.translation = translation['translation']
            server_translation.deleted = translation['deleted']
            server_translation.starred = translation['starred']
            translations_to_update.append(server_translation)

        else:
            new_translation = Translation(uuid=uuid, added=translation['added'],
                                          updated=translation['updated'], original=translation['original'],
                                          translation=translation['translation'], deleted=translation['deleted'],
                                          starred=translation['starred'])
            translations_to_create.append(new_translation)

    logger.info('Translations to update: %s; translations to create: %s',
                len(translations_to_update), len(translations_to_create))

    Translation.objects.bulk_update(translations_to_update,
                                    ['updated', 'original', 'translation', 'starred', 'deleted', 'added'])
    Translation.objects.bulk_create(translations_to_create)
