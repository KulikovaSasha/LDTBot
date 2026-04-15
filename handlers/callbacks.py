"""
Callback handlers.

Processes button clicks from inline keyboards.
"""

from services.state_service import get_user_state
from services.image_service import generate_image
from keyboards.inline import get_edit_keyboard, get_result_keyboard


def register_callback_handlers(bot, set_text_handler):
    """
    Registers callback query handlers.

    Args:
        bot: TeleBot instance.
        set_text_handler: Function that handles user text input.
    """

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        """
        Main callback router.
        """
        user_id = call.message.chat.id
        state = get_user_state(user_id)

        if not state:
            return

        if call.data in ["top", "bottom"]:
            state["position"] = call.data
            bot.send_message(user_id, "Now send me the text")
            bot.register_next_step_handler(call.message, set_text_handler)

        elif call.data == "yes":
            bot.send_message(user_id, "Great! Glad to help 😊")

        elif call.data == "no":
            bot.send_message(user_id, "What would you like to change?", reply_markup=get_edit_keyboard())


        elif call.data == "font_up":

            state["font_size"] = min(state["font_size"] + 4, 120)

            send_updated_image(bot, user_id, state)


        elif call.data == "font_down":

            state["font_size"] = max(state["font_size"] - 4, 12)

            send_updated_image(bot, user_id, state)

        elif call.data == "color":
            state["color"] = 1 - state["color"]
            send_updated_image(bot, user_id, state)

        elif call.data == "switch_position":
            state["position"] = "bottom" if state["position"] == "top" else "top"
            send_updated_image(bot, user_id, state)

        elif call.data == "change_text":
            bot.send_message(user_id, "Send me the new text")
            bot.register_next_step_handler(call.message, set_text_handler)


def send_updated_image(bot, user_id, state):
    """
    Regenerates and sends updated image after editing.

    Args:
        bot: TeleBot instance.
        user_id: Telegram chat ID.
        state: User state dictionary.
    """
    result_path = generate_image(state, user_id)

    with open(result_path, "rb") as photo:
        bot.send_photo(user_id, photo)

    bot.send_message(user_id, "Updated!")
    bot.send_message(user_id, "Do you like the result?", reply_markup=get_result_keyboard())