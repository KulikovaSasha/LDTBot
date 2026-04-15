"""
Photo handlers.

Receives photos from the user and saves them locally.
"""

import os

from services.state_service import create_user_state, get_user_state
from services.image_service import generate_image
from keyboards.inline import get_position_keyboard, get_result_keyboard


def register_photo_handlers(bot):
    """
    Registers photo handlers.

    Returns:
        function: set_text handler for next-step registration.
    """

    @bot.message_handler(content_types=["photo"])
    def handle_photo(message):
        """
        Handles uploaded photos.
        """
        user_id = message.chat.id

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        os.makedirs("generated", exist_ok=True)

        photo_path = f"generated/photo_{user_id}.jpg"
        with open(photo_path, "wb") as new_file:
            new_file.write(downloaded_file)

        create_user_state(user_id, photo_path)

        bot.send_message(
            user_id,
            "Where should I place the text?",
            reply_markup=get_position_keyboard()
        )

    def set_text(message):
        """
        Saves user text and generates the image.
        """
        user_id = message.chat.id
        state = get_user_state(user_id)

        if not state:
            return

        state["text"] = message.text
        result_path = generate_image(state, user_id)

        with open(result_path, "rb") as photo:
            bot.send_photo(user_id, photo)

        bot.send_message(user_id, "Done!")
        bot.send_message(user_id, "Do you like the result?", reply_markup=get_result_keyboard())

    return set_text