# https://replit.com/@vmgoryachkin/IntelligentShoddyCgibin#main.py
# https://desktop.telegram.org/
from background import keep_alive #импорт функции для поддержки работоспособности
import pip
pip.main(['install', 'pytelegrambotapi'])
import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont

from settings import TG_TOKEN

# инициализация бота
bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Я умею добавляте текст на фото. Если хочешь попробовать, отправь картинку')

# обработчик сообщений с фотографиями
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('photo.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)

    # определяем, где будет текст
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Вверху', callback_data='top')
    btn2 = types.InlineKeyboardButton('Внизу', callback_data='bottom')
    markup.row(btn1, btn2)
    bot.reply_to(message, f"{message.from_user.first_name}, отличное фото! Давай решим, где будет находиться надпись", reply_markup=markup)

    @bot.callback_query_handler(func=lambda callback: True)

    def callback_message(callback):
        if callback.data == 'top':
            bot.send_message(message.chat.id, f"Хорошо! Теперь отправь мне текст")
            position = 'top'
            bot.register_next_step_handler(message, set_photo_text, position)

        elif callback.data == 'bottom':
            bot.send_message(message.chat.id, f"Хорошо! Теперь отправь мне текст")
            position = 'bottom'
            bot.register_next_step_handler(message, set_photo_text, position)


# обработчик текста
def set_photo_text(message,position):
    try:
        image = Image.open('photo.jpg')
        draw = ImageDraw.Draw(image)
        # загрузка шрифта, поддерживающего кириллицу

        h = 60
        font = ImageFont.truetype('CactusClassicalSerif-Regular.ttf', h)  # убеждаемся, что файл находится в рабочем каталоге

        #накладываем текст на фото
        text = message.text
        bbox = draw.textbbox((0, 0), text.upper(), font=font)
        #text_width = bbox[2] - bbox[0]

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
        if position == 'bottom':
            n = len(ans)
        elif position == 'top':
            n = 0

        for i in ans:
            bbox = draw.textbbox((0, 0), i, font=font)
            text_width = bbox[2] - bbox[0]
            #text_height = bbox[3] - bbox[1]
            b = (h+20) * n
            x = (image.width - text_width) / 2
            if position == 'bottom':
                y = image.height - b
                n -= 1
            elif position == 'top':
                y = 20 + b
                n += 1

            draw.rectangle((x - 8, y, x + text_width + 10, y + h*1.2), fill=(255, 255, 255, 255))
            draw.text((x, y), i, font=font, fill=(0, 0, 0))
            image.save('result.jpg')

        bot.send_photo(message.chat.id, open('result.jpg', 'rb'))

    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка, попробуй снова')
        print(e)



keep_alive()#запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0) #запуск бота