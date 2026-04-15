"""
Main entry point of the bot.
"""

import telebot
from config import TG_TOKEN

from handlers.commands import register_commands
from handlers.photo import register_photo_handlers
from handlers.callbacks import register_callback_handlers

bot = telebot.TeleBot(TG_TOKEN)


def main():
    """
    Registers all handlers and starts polling.
    """
    register_commands(bot)
    set_text_handler = register_photo_handlers(bot)
    register_callback_handlers(bot, set_text_handler)

    print("Bot is running...")
    bot.infinity_polling()


if __name__ == "__main__":
    main()