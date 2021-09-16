import telebot

from settings import TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def send_message(message):
    bot.send_message(TELEGRAM_CHAT_ID, message)
    