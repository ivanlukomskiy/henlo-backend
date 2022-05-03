import os
import re

from django.core.management import BaseCommand
from django.utils import timezone
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

from henlo_app.models import Translation

TOKEN = os.getenv('telegram_token')

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

class Command(BaseCommand):
    help = 'Fetch drafts from telegram bot and save them to the database'

    def start(self, update: Update, context: CallbackContext):
        try:
            text = update.message.text.strip()
            is_russian = has_cyrillic(text)
            Translation.objects.create(
                original=text if not is_russian else '',
                translation=text if is_russian else '',
                added=timezone.now(),
            )
            context.bot.send_message(chat_id=update.effective_chat.id, text="Draft saved")
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to save draft")

    def handle(self, *args, **options):
        updater = Updater(token=TOKEN)
        dispatcher = updater.dispatcher
        start_handler = MessageHandler(Filters.text, self.start)
        dispatcher.add_handler(start_handler)
        updater.start_polling()
