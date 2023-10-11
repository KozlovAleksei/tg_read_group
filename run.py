import logging
import telegram
from telegram.ext import Updater, MessageHandler, Filters

# Конфигурация логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Ваш токен доступа к боту
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Функция, вызываемая при получении нового сообщения
def process_message(update, context):
    message = update.message
    chat_id = message.chat_id
    text = message.text

    # Записываем сообщение в файл
    filename = f'C:\\{chat_id}.txt'
    with open(filename, 'w') as file:
        file.write(text)

    # Отправляем подтверждение о получении сообщения
    context.bot.send_message(chat_id=chat_id, text='Сообщение получено и записано в файл.')

def main():
    # Создаем объект бота
    bot = telegram.Bot(token=TOKEN)
    updater = Updater(bot=bot, use_context=True)

    # Определяем обработчик сообщений
    message_handler = MessageHandler(Filters.text, process_message)
    updater.dispatcher.add_handler(message_handler)

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
