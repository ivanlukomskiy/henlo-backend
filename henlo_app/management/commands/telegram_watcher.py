import os
import re

from django.core.management import BaseCommand
from django.utils import timezone
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

from henlo_app.models import Translation

TOKEN_FILE = os.getenv('TELEGRAM_TOKEN_FILE')
token = None
with open(TOKEN_FILE, 'r') as file:
    token = file.read().replace('\n', '')


class Command(BaseCommand):
    help = 'Fetch drafts from telegram bot and save them to the database'

    def start(self, update: Update, context: CallbackContext):
        try:
            text = update.message.text.strip()
            Translation.objects.create(
                original=text,
                translation='',
                added=timezone.now(),
            )
            context.bot.send_message(chat_id=update.effective_chat.id, text="Draft saved")
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to save draft")

    def handle(self, *args, **options):
        updater = Updater(token=token)
        dispatcher = updater.dispatcher
        start_handler = MessageHandler(Filters.text, self.start)
        dispatcher.add_handler(start_handler)
        updater.start_polling()
