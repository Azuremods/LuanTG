from pyrogram import Client, filters
from plugins.help import module_list
import requests
import os

def get_pic(city):
    file_name = f"{city}.png"
    with open(file_name, "wb") as pic:
        response = requests.get(f"http://wttr.in/{city}_2&lang=ru.png", stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            pic.write(block)
        return file_name


@Client.on_message(filters.command("weather", prefixes='!') & filters.me)
async def weather(client, message):
    city = message.command[1]
    await message.edit("Check weather...")
    r = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=ru")
    await message.edit(f"🗺 You sity/village: {city}\n{r.text}")
    await client.send_photo(
        chat_id=message.chat.id,
        photo=get_pic(city),
        reply_to_message_id=message.id)
    os.remove(f"{city}.png")


module_list['Weather'] = f'!weather [город]'
