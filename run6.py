# Есть у телеги ограничение на получения количества чатов = 180
# Так как чатов может быть много, то нужный чат надо закрепить на первой вкладке, иначе он может не попасть в список
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import MessageMediaPoll
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.messages import SendVoteRequest
from telethon.tl import types

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

# target_chat_id = 1772781939  # https://web.telegram.org/a/#-1001772781939 'Олег торгует'
# target_chat_id = 1734066007  # https://web.telegram.org/a/#-1001734066007 'БКС Мир инвестиций'
target_chat_id = 1322987562  # https://web.telegram.org/a/#-1001322987562 'Atusoi'

for i, chat in enumerate(chats):
    try:
        # print(i+1, chat.id, '~', chat.title, '~', chat.username)
        if chat.id == target_chat_id:
            groups.append(chat)
            break
    except:
        continue

try:
    target_group = groups[0]
    print(target_group)
except Exception:
    print(target_chat_id, ' надо закрепить на главной закладке Телеграм')
# print(target_group)

# print("Group ID:", target_group.id)
# print("Title:", target_group.title)
# print("Username:", target_group.username)

messages = client.get_messages(target_group, limit=1)


last_message = client.get_messages(target_group, limit=1)[0]


if isinstance(last_message.media, MessageMediaPoll):
    poll = last_message.media.poll
    print("ГОЛОСОВАНИЕ")
    print(poll.question)

    options = []
    for answer in poll.answers:
        print(answer.text)

        if answer.text == 'Не знаю':  # 'Не согласен' 'Согласен' 'Не знаю'
            options = [answer.option]  # Создание списка options с одним элементом
            break

    if len(options) > 0:
        # Отправка голоса
        client(SendVoteRequest(target_group.id, last_message.id, options=options))
else:
    print("Сообщение")
    last_message = messages[0].message
    print(last_message)

