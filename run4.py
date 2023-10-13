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

result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=size_chats,
            hash = 0
        ))
chats.extend(result.chats)
# print(chats)

for chat in chats:
   try:
       # 'ProfitGateClub' 'Atusoi'
       if chat.title == 'Atusoi':
           groups.append(chat)
           break
   except:
       continue

target_group = groups[0]
# print(target_group)

print('Узнаём пользователей...')
all_participants = []
all_participants = client.get_participants(target_group)


# здесь надо получить последнее сообщение из чата и вывести сообщение в окно терминала
print('Узнаём последнее сообщение...')
messages = client.get_messages(target_group, limit=1)
last_message = messages[0].message
print(last_message)

print('Сохраняем данные в файл...')
with open("members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = ""
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = ""
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = ""
        name = (first_name + ' ' + last_name).strip()
        print(name)
        writer.writerow([username, name, target_group.title])
print('Парсинг участников группы успешно выполнен.')


print('Сохраняем данные в файл...')
with open("members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = ""
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = ""
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = ""
        name = (first_name + ' ' + last_name).strip()
        print(name)
        writer.writerow([username, name, target_group.title])
print('Парсинг участников группы успешно выполнен.')


