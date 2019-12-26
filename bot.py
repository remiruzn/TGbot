import telebot
import cv2
from findcontours import carCnt


# socks5 = '5.182.26.39:3129'
# socks51 = '51.158.186.141:1080'
#
# telebot.apihelper.proxy = {'https': 'socks5h://'+socks5}


telegram_bot = telebot.TeleBot('804614310:AAEg7B7wq9G67m0CK6R5ouubgBGzdREpbpw')

@telegram_bot.message_handler(commands=['start'])

def start_message(message):
    telegram_bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

@telegram_bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        telegram_bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'пока':
        telegram_bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'лавки':
        telegram_bot.send_sticker(message.chat.id, 'CAADAgADDAADwDZPE-LPI__Cd5-8FgQ')

@telegram_bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:

        file_info = telegram_bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = telegram_bot.download_file(file_info.file_path)
        src = file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        telegram_bot.reply_to(message, "Фото получил, обрабатываю...")

        print(src)

        carCnt(src)


        photo = open('CNTS.jpg', 'rb')
        telegram_bot.send_photo(message.chat.id, photo)

    except Exception as e:
        telegram_bot.reply_to(message, e)

@telegram_bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)




telegram_bot.polling()