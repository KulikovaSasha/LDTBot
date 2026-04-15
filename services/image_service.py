"""
Image processing service.

Generates an image with text overlay.
Automatically adjusts font size and spacing so the text fits the image.
"""

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "CactusClassicalSerif-Regular.ttf"


def split_long_word(draw, word, font, max_width):
    """
    Splits a very long word into smaller parts if it does not fit the image width.

    Args:
        draw: Pillow drawing object.
        word: One long word.
        font: Loaded font.
        max_width: Maximum allowed text width.

    Returns:
        list[str]: Parts of the word.
    """
    parts = []
    current = ""

    for char in word:
        test = current + char
        bbox = draw.textbbox((0, 0), test.upper(), font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width - 40:
            current = test
        else:
            if current:
                parts.append(current.upper())
            current = char

    if current:
        parts.append(current.upper())

    return parts


def split_text(draw, text, font, max_width):
    """
    Splits text into multiple lines so it fits the image width.
    Also handles very long words without spaces.

    Args:
        draw: Pillow drawing object.
        text: User text.
        font: Loaded font.
        max_width: Maximum allowed text width.

    Returns:
        list[str]: List of text lines.
    """
    words = text.split()
    lines = []
    current = ""

    for word in words:
        word_bbox = draw.textbbox((0, 0), word.upper(), font=font)
        word_width = word_bbox[2] - word_bbox[0]

        if word_width > max_width - 40:
            if current:
                lines.append(current.upper())
                current = ""

            parts = split_long_word(draw, word, font, max_width)
            lines.extend(parts)
            continue

        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test.upper(), font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width - 40:
            current = test
        else:
            if current:
                lines.append(current.upper())
            current = word

    if current:
        lines.append(current.upper())

    return lines


def measure_lines(draw, lines, font):
    """
    Measures text block dimensions.

    Args:
        draw: Pillow drawing object.
        lines: List of text lines.
        font: Loaded font.

    Returns:
        tuple:
            max_width (int): width of the widest line
            line_heights (list[int]): heights of each line
            total_height (int): total height of all lines including spacing
    """
    line_heights = []
    max_width = 0
    line_spacing = 12

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        left, top, right, bottom = bbox
        width = right - left
        height = bottom - top

        max_width = max(max_width, width)
        line_heights.append(height)

    total_height = sum(line_heights)
    if len(line_heights) > 1:
        total_height += line_spacing * (len(line_heights) - 1)

    return max_width, line_heights, total_height


def get_fitting_font(draw, text, image_width, image_height, initial_font_size):
    """
    Finds the largest possible font size that fits the image.

    The function starts from the user-selected font size and gradually reduces it
    only if the text does not fit.

    Returns:
        tuple:
            font,
            lines,
            line_heights,
            total_height,
            used_font_size
    """
    font_size = max(12, initial_font_size)

    while font_size >= 12:
        font = ImageFont.truetype(FONT_PATH, font_size)

        lines = split_text(draw, text, font, image_width)
        max_width, line_heights, total_height = measure_lines(draw, lines, font)

        if max_width <= image_width - 20 and total_height <= image_height * 0.35:
            return font, lines, line_heights, total_height, font_size

        font_size -= 2

    # Fallback
    font_size = 12
    font = ImageFont.truetype(FONT_PATH, font_size)
    lines = split_text(draw, text, font, image_width)
    max_width, line_heights, total_height = measure_lines(draw, lines, font)

    return font, lines, line_heights, total_height, font_size


def generate_image(state: dict, user_id: int) -> str:
    """
    Generates an edited image with text overlay.

    Args:
        state: User state dictionary.
        user_id: Telegram chat ID.

    Returns:
        str: Path to the generated image.
    """
    image = Image.open(state["photo"])
    draw = ImageDraw.Draw(image)

    font, lines, line_heights, total_height, used_font_size = get_fitting_font(
        draw=draw,
        text=state["text"],
        image_width=image.width,
        image_height=image.height,
        initial_font_size=state["font_size"]
    )

    # Layout settings
    line_spacing = 12
    pad_x = 8
    pad_y = 8
    block_margin = 12

    # Determine starting Y for the whole text block
    if state["position"] == "top":
        current_y = block_margin
    else:
        current_y = image.height - total_height - block_margin

    for line, _line_height in zip(lines, line_heights):
        # Exact bbox for line
        bbox = draw.textbbox((0, 0), line, font=font)
        left, top, right, bottom = bbox

        text_width = right - left
        text_height = bottom - top

        # Position of the text block
        box_x = (image.width - text_width) / 2
        box_y = current_y

        # Background rectangle coordinates
        rect_x1 = box_x - pad_x
        rect_y1 = box_y - pad_y
        rect_x2 = box_x + text_width + pad_x
        rect_y2 = box_y + text_height + pad_y

        # Corrected text coordinates taking bbox offsets into account
        text_x = box_x - left
        text_y = box_y - top

        if state["color"] == 0:
            # White background + black text
            draw.rectangle((rect_x1, rect_y1, rect_x2, rect_y2), fill=(255, 255, 255))
            draw.text((text_x, text_y), line, font=font, fill=(0, 0, 0))
        else:
            # Black background + white text
            draw.rectangle((rect_x1, rect_y1, rect_x2, rect_y2), fill=(0, 0, 0))
            draw.text((text_x, text_y), line, font=font, fill=(255, 255, 255))

        # Move to next line
        current_y += text_height + line_spacing

    result_path = f"generated/result_{user_id}.jpg"
    image.save(result_path)

    # Save the actual font size used after fitting
    state["font_size"] = used_font_size

    return result_path