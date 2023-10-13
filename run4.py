from telethon.sync import TelegramClient
from telethon.tl.functions import messages
import csv

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

import time

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
phone = read_text_from_file('C:\\py386\secret\\001\\phone.txt')

client = TelegramClient('session_name', api_id, api_hash)
client.connect()

client = TelegramClient(phone, api_id, api_hash)
# print(client)

client.start()

chats = []
last_date = None
size_chats = 200
groups=[]

offset_id = 0  # начальное смещение (0, чтобы получить первые 200 чатов/групп)
while True:
    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=offset_id,
        offset_peer=InputPeerEmpty(),
        limit=size_chats,
        hash=0
    ))
    chats.extend(result.chats)
    if len(result.chats) < size_chats:
        break  # если получено меньше, чем запрошенное количество, значит все чаты/группы загружены
    else:
        last_chat = result.chats[-1]
        offset_id = last_chat.id  # обновление смещения для следующей пагинации

# print(chats)

'''
Объект `Chat` в Telegram API обычно содержит следующие поля:

- `id`: Уникальный идентификатор чата.
- `title`: Название группы или канала.
- `username`: Юзернейм канала или супергруппы, если он установлен.
- `creator`: Вы, если вы являетесь создателем группы или супергруппы.
- `created`: Время создания группы или супергруппы.
- `participants_count`: Количество участников в группе или супергруппы.
- `admins_count`: Количество администраторов в группе или супергруппы.
- `kicked_count`: Количество пользователей, исключенных из группы или супергруппы.
- `left`: Если вы покинули группу или супергруппы.
- `migrated_to`: Переведен ли данный объект в супергруппу, если это обычная группа.
- `about`: Описание супергруппы или информация о профиле канала.
- `slowmode_seconds`: Интервал между сообщениями в супергруппе.
- `slowmode_next_send_date`: Когда в следующий раз можно будет отправить сообщение, если это супергруппа с включенным ограничением по времени.
- `restriction_reason`: Причина ограничения группы или супергруппы, если применимо.

Примечание: Некоторые из этих полей могут быть не доступны или иметь значение `None` в зависимости от настроек группы или супергруппы, прав доступа пользователя и т.д.
'''

# if chat.title == 'Atusoi':
# if chat.title == '#-1001322987562': # https://web.telegram.org/a/#-1001322987562
# print(chat.id, '~', chat.title, '~', chat.username, '~', chat.creator, '~', chat.created, '~',
#       chat.participants_count, '~', chat.admins_count, '~', chat.kicked_count, '~', chat.left, '~',
#       chat.migrated_to, '~', chat.about, '~', chat.slowmode_seconds, '~', chat.slowmode_next_send_date,
#       '~', chat.restriction_reason)

# target_chat_id = 1772781939  # https://web.telegram.org/a/#-1001772781939 'Олег торгует'
# target_chat_id = 1734066007  # https://web.telegram.org/a/#-1001734066007 'БКС Мир инвестиций'
target_chat_id = 1322987562  # https://web.telegram.org/a/#-1001322987562 'Atusoi'

for i, chat in enumerate(chats):
    try:
        print(i+1, chat.id, '~', chat.title, '~', chat.username)
        if chat.id == target_chat_id:
            groups.append(chat)
            # break
    except:
        continue

target_group = groups[0]
print(target_group)

print("Group ID:", target_group.id)
print("Title:", target_group.title)
print("Username:", target_group.username)

# здесь надо получить последнее сообщение из чата и вывести сообщение в окно терминала
print('Узнаём последнее сообщение...')
messages = client.get_messages(target_group, limit=1)
last_message = messages[0].message
print(last_message)
