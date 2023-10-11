import time
from telethon.sync import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

def read_text_from_file(TextFileName):
    for _ in range(3):
        try:
            with open(TextFileName, "r") as file:
                text = file.read()
                return text
        except FileNotFoundError:
            time.sleep(0.01)
    return ''

api_id = int(read_text_from_file('C:\\py386\secret\\001\\api_id.txt'))
api_hash = read_text_from_file('C:\\py386\secret\\001\\api_hash.txt')

# channel = 'Atusoi'
# username = '@x5y5z5'

channel_username = 'OlegTrade'
# channel_username = 'OlegTradeSupport'

# Функция для чтения сообщений и записи в файл
def read_messages(channel_username):
    with TelegramClient('session_name', api_id, api_hash) as client:
        # Попробуйте получить сущность, используя различные типы данных
        entity = None
        if entity is None:
            entity = client.get_entity(channel_username)  # Попытка использовать введенное имя напрямую
        if entity is None:
            entity = client.get_entity(PeerChat(channel_username))  # Получение сущности, используя PeerChat
        if entity is None:
            entity = client.get_entity(PeerChannel(channel_username))  # Получение сущности, используя PeerChannel
        if entity is None:
            entity = client.get_entity(PeerUser(channel_username))  # Получение сущности, используя PeerUser

        if entity is not None:
            messages = client.get_messages(entity, limit=1)  # Читаем 1 последних сообщений


            # Записываем сообщения в файл
            with open(f'C:\\{channel_username}.txt', 'w') as file:
                for message in messages:
                    file.write(f'{message.sender_id}: {message.text}\n')
                    print(message.text)
        else:
            print("Сущность не найдена")

# Пример использования функции
read_messages(channel_username)