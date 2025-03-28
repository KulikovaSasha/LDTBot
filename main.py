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
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}! Я умею добавляте текст на фото. Если хочешь попробовать, отправь картинку')


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
    bot.reply_to(message, f"{message.from_user.first_name}, отличное фото! Давай решим, где будет находиться надпись",
                 reply_markup=markup)
    position = 0
    k = 16
    color = 0
    @bot.callback_query_handler(func=lambda callback: True)
    def callback_message(callback):
        global position
        global k
        global color
        if callback.data == 'top':
            bot.send_message(message.chat.id, f"Хорошо! Теперь отправь мне текст")
            position = 'top'
            k = 16
            color = 0
            bot.register_next_step_handler(message, set_photo_text, position, k, color)

        elif callback.data == 'bottom':
            bot.send_message(message.chat.id, f"Хорошо! Теперь отправь мне текст")
            position = 'bottom'
            k = 16
            color = 0
            bot.register_next_step_handler(message, set_photo_text, position, k,color)

            #оцениваем результат
        elif callback.data == 'yes':
            bot.send_message(message.chat.id, f"Отлично! Буду рад увидеться снова!")
            #изменяем надпись
        elif callback.data == 'no':
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn5 = types.InlineKeyboardButton('Уменьшить шрифт', callback_data='correct_1')
            btn6 = types.InlineKeyboardButton('Увеличить шрифт', callback_data='correct_2')
            if color == 0:
                btn7 = types.InlineKeyboardButton('Изменить цвет шрифта', callback_data='correct_3_1')
            else:
                btn7 = types.InlineKeyboardButton('Сменить цвет шрифта', callback_data='correct_3_2')
            if position == 'top':
                btn8 = types.InlineKeyboardButton('Сделать надпись внизу', callback_data='correct_4')
            else:
                btn8 = types.InlineKeyboardButton('Сделать надпись вверху', callback_data='correct_5')
            markup.row(btn5, btn6)
            markup.row(btn7, btn8)
            bot.send_message(message.chat.id, f"Что бы ты хотел исправить?",
                             reply_markup=markup)
        elif callback.data == 'correct_1':
            k *= 1.5
            bot.send_message(message.chat.id, f"Хорошо, введи, пожалуйста, текст заново")
            bot.register_next_step_handler(message, set_photo_text, position, k, color)
        elif callback.data == 'correct_2':
            k /= 1.5
            bot.send_message(message.chat.id, f"Хорошо, введи, пожалуйста, текст заново")
            bot.register_next_step_handler(message, set_photo_text, position, k, color)
        elif callback.data == 'correct_3_1':
            color = 1
            bot.send_message(message.chat.id, f"Хорошо, введи, пожалуйста, текст заново")
            bot.register_next_step_handler(message, set_photo_text, position, k, color)
        elif callback.data == 'correct_3_2':
            color = 0
            bot.send_message(message.chat.id, f"Хорошо, введи, пожалуйста, текст заново")
            bot.register_next_step_handler(message, set_photo_text, position, k, color)
        elif callback.data == 'correct_4':
            position = 'bottom'
            bot.send_message(message.chat.id, f"Хорошо, введи, пожалуйста, текст заново")
            bot.register_next_step_handler(message, set_photo_text, position, k, color)
        elif callback.data == 'correct_5':
            position = 'top'
            bot.send_message(message.chat.id, f"Хорошо, введи, пожалуйста, текст заново")
            bot.register_next_step_handler(message, set_photo_text, position, k, color)

# обработчик текста
def set_photo_text(message, position, k, color):
    try:
        image = Image.open('photo.jpg')
        draw = ImageDraw.Draw(image)
            # загрузка шрифта, поддерживающего кириллицу
        h = image.height/k
        font = ImageFont.truetype('CactusClassicalSerif-Regular.ttf',
                                          h)  # убеждаемся, что файл находится в рабочем каталоге

            # накладываем текст на фото
        text = message.text
        text_3 = text
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
            b = (h + 20) * n
            x = (image.width - text_width) / 2
            if position == 'bottom':
                y = image.height - b
                n -= 1
            elif position == 'top':
                y = 20 + b
                n += 1
            if color == 0:
                draw.rectangle((x - 8, y, x + text_width + 10, y + h * 1.2), fill=(255, 255, 255, 255))
                draw.text((x, y), i, font=font, fill=(0, 0, 0))
            else:
                draw.rectangle((x - 8, y, x + text_width + 10, y + h * 1.2), fill=(0, 0, 0, 0))
                draw.text((x, y), i, font=font, fill=(255, 255, 255))
            image.save('result.jpg')


        bot.send_photo(message.chat.id, open('result.jpg', 'rb'))
        bot.send_message(message.chat.id, f"Готово!")
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn3 = types.InlineKeyboardButton('Да, оставляем так', callback_data='yes')
        btn4 = types.InlineKeyboardButton('Нет, хочу переделать', callback_data='no')
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, тебе нравится?",
                                 reply_markup=markup)

    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка, попробуй снова')
        print(e)

bot.polling(non_stop=True)  # запуск бота