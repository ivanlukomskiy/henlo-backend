from django.contrib import admin
from .models import Translation


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'original', 'translation', 'added', 'updated', 'deleted')
    fields=('uuid', 'original', 'translation', 'added', 'updated', 'deleted')
