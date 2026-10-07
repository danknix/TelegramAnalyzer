from config import api_id, api_hash
from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel
from datetime import datetime, timedelta, timezone
 

client = TelegramClient('1', api_id, api_hash)

offsetw = datetime.now(timezone.utc) - timedelta(days=7)
offsetm = datetime.now(timezone.utc) - timedelta(days=30)


async def main():
    msg_week = 0
    msg_month = 0
    most_active_chat = []
    most_used_words = {}
    await client.start()
    print("Успешный вход!\n")
    for dialog in await client.get_dialogs():
        is_bot = getattr(dialog.entity, "bot", False)
        if dialog.is_group or dialog.is_channel or is_bot:
            continue
        print("Чат:", dialog.name)
        messages = await client.get_messages(dialog.id, offset_date=offsetw, reverse=True)
        msg_week += len(messages)
        messages = await client.get_messages(dialog.id, offset_date=offsetm, reverse=True)
        msg_month += len(messages)
        most_active_chat.append((len(messages), dialog.name))
        for message in messages:
            if message.text and message.out:
                words = message.text.split()
                for word in words:
                    if len(word) < 3:
                        continue
                    if word in most_used_words:
                        most_used_words[word] += 1
                    else:
                        most_used_words[word] = 1
    most_active_chat.sort(reverse=True)
    print("MOST ACTIVE CHATS:")
    for i in range(min(5, len(most_active_chat))):
        print(i + 1, most_active_chat[i][1], "with", most_active_chat[i][0], "messages")

    print("\nMOST USED WORDS:")
    sorted_words = sorted(most_used_words.items(), key=lambda x: x[1], reverse=True)
    for i in range(min(5, len(sorted_words))):
        print(i + 1, sorted_words[i][0], "used", sorted_words[i][1], "times")
with client:
    client.loop.run_until_complete(main())