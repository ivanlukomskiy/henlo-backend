from django.contrib import admin

from .models import Translation


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('original', 'translation', 'added', 'updated', 'starred', 'deleted')
    fields = ('uuid', 'original', 'translation', 'added', 'updated', 'starred', 'deleted')
    ordering = ('-added',)
