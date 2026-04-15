"""
Command handlers for the Telegram bot.

Handles basic commands such as /start and /help.
"""


def register_commands(bot):
    """
    Registers command handlers for the bot.

    Args:
        bot (telebot.TeleBot): The bot instance.
    """

    @bot.message_handler(commands=["start"])
    def start(message):
        """
        Sends a welcome message when the user starts the bot.
        """
        bot.send_message(
            message.chat.id,
            "👋 Send me a photo, and I will add text to it!"
        )

    @bot.message_handler(commands=["help"])
    def help_command(message):
        """
        Sends help instructions to the user.
        """
        bot.send_message(
            message.chat.id,
            "📷 Send a photo to start editing.\n"
            "You will be able to add and customize text."
        )