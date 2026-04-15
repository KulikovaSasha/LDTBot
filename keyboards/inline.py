"""
Inline keyboards for bot interaction.
"""

from telebot import types


def get_position_keyboard():
    """
    Keyboard for selecting text position.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Top", callback_data="top"),
        types.InlineKeyboardButton("Bottom", callback_data="bottom")
    )
    return markup


def get_result_keyboard():
    """
    Keyboard shown after image generation.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Yes", callback_data="yes"),
        types.InlineKeyboardButton("No", callback_data="no")
    )
    return markup


def get_edit_keyboard():
    """
    Keyboard for editing the generated result.
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Decrease Font", callback_data="font_down"),
        types.InlineKeyboardButton("Increase Font", callback_data="font_up")
    )
    markup.add(
        types.InlineKeyboardButton("Change Color", callback_data="color"),
        types.InlineKeyboardButton("Switch Position", callback_data="switch_position")
    )
    markup.add(
        types.InlineKeyboardButton("Edit Text", callback_data="change_text")
    )
    return markup