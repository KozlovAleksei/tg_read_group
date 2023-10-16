'''
В телеграм-канале помимо обычного текста появляются кнопки, например кнопка "Смотреть идею".
Обычный текст прилагаемая программа выводит, а текст кнопки - нет.
Кнопки похожи на кнопки голосования, но ими не являются т.к. прилагаемый код их не видит.
Надо распознавать кнопки в сообщениях, которые не являются кнопками голосования, и если они там сделаны и выводить их текст.
'''

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import MessageMediaPoll
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.messages import SendVoteRequest
from telethon.tl import types
from datetime import datetime
import time
import mlb

api_id = int(mlb.read_text_from_file('C:\\py386\secret\\001\\api_id.txt'))
api_hash = mlb.read_text_from_file('C:\\py386\secret\\001\\api_hash.txt')
phone = mlb.read_text_from_file('C:\\py386\secret\\001\\phone.txt')
message_file = 'C:\\py386\\message.txt'

client = TelegramClient('session_name', api_id, api_hash)
client.connect()

client = TelegramClient(phone, api_id, api_hash)

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

target_chat_id = 1772781939  # https://web.telegram.org/a/#-1001772781939 'Олег торгует'
# target_chat_id = 1734066007  # https://web.telegram.org/a/#-1001734066007 'БКС Мир инвестиций'
# target_chat_id = 1322987562  # https://web.telegram.org/a/#-1001322987562 'Atusoi'

for i, chat in enumerate(chats):
    try:
        print(i+1, chat.id, '~', chat.title, '~', chat.username)
        if chat.id == target_chat_id:
            groups.append(chat)
            break
    except:
        continue

try:
    target_group = groups[0]
except Exception:
    print(target_chat_id, ' надо закрепить на главной закладке Телеграм')
    breakpoint()

# print(target_group)
print("Group ID:", target_group.id)
print("Title:", target_group.title)
print("Username:", target_group.username)

while True:
    time.sleep(2)
    messages = client.get_messages(target_group, limit=1)  # для сообщений

    last_message = client.get_messages(target_group, limit=1)[0]  # для голосования

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
        # print(messages[0])

        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S") + '\n'
        print(now)

        text_messages = messages[0].message
        print(text_messages)

        reply_markup = messages[0].reply_markup

        if reply_markup is not None and isinstance(reply_markup, types.ReplyInlineMarkup):
            for row in reply_markup.rows:
                for button in row.buttons:
                    if isinstance(button, types.KeyboardButtonCallback):
                        button_text = button.text
                        print("Найдена кнопка:", button_text)
                    elif isinstance(button, types.KeyboardButtonUrl):
                        button_text = button.text
                        print("Найдена кнопка со ссылкой:", button_text)







        # with open(message_file, 'w', encoding='cp1251', errors='ignore') as file:
        #     file.write(last_message)
        # breakpoint()
        # if last_message !="Занято":
        #     client(SendMessageRequest(target_chat_id, "Занято"))
    breakpoint()
