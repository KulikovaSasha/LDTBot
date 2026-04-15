"""
Service for storing user state.

Keeps temporary data for each user while they interact with the bot.
"""

user_states = {}


def create_user_state(user_id: int, photo_path: str) -> None:
    """
    Creates initial state for a user.

    Args:
        user_id: Telegram chat ID.
        photo_path: Path to the uploaded photo.
    """
    user_states[user_id] = {
        "photo": photo_path,
        "position": "top",
        "font_size": 40,
        "color": 0,
        "text": ""
    }


def get_user_state(user_id: int):
    """
    Returns the user's current state.
    """
    return user_states.get(user_id)