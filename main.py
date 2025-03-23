# https://replit.com/@vmgoryachkin/IntelligentShoddyCgibin#main.py
# https://desktop.telegram.org/

import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont
from settings import TG_TOKEN

# инициализация бота
bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я - генератор мемов. Для начала отправь картинку - основу мема.')


# обработчик сообщений с фотографиями
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('photo.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, f"{message.from_user.first_name}, отличное фото! Теперь давай добавим текст")
    bot.register_next_step_handler(message, set_photo_text)


# обработчик текста для мема
def set_photo_text(message):
    try:
        image = Image.open('photo.jpg')
        draw = ImageDraw.Draw(image)
        # загрузка шрифта, поддерживающего кириллицу
        h = 60
        font = ImageFont.truetype('ARIAL.TTF', h)  # убеждаемся, что файл находится в рабочем каталоге
        text = message.text
        bbox = draw.textbbox((0, 0), text.upper(), font=font)
        text_width = bbox[2] - bbox[0]

        ans = []
        text_2 = text.split()

        i = 1
        go = True
        text = text_2[0]
        while go:

            if i < len(text_2):
                if (text_2[i][0]).isalpha():
                    prov = text + text_2[i]
                    bbox = draw.textbbox((0, 0), prov.upper(), font=font)
                    text_width = bbox[2] - bbox[0]
                    if text_width + 60 < image.width:
                        text = text + " " + text_2[i]
                        i += 1
                    else:
                        text = text.upper()
                        ans.append(text)
                        text = text_2[i]
                        i += 1
                else:
                    text = text + " " + text_2[i]
                    i += 1


            else:
                text = text.upper()
                ans.append(text)
                go = False
        n = len(ans)

        for i in ans:
            bbox = draw.textbbox((0, 0), i, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            b = (h+20) * n
            x = (image.width - text_width) / 2
            y = image.height - b
            n -= 1
            draw.rectangle((x - 10, y, x + text_width + 10, y + h*1.1 ), fill=(255, 255, 255, 255))
            draw.text((x, y), i, font=font, fill=(0, 0, 0))
            image.save('result.jpg')

        bot.send_photo(message.chat.id, open('result.jpg', 'rb'))

    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка, попробуй снова')
        print(e)


bot.polling(none_stop=True)