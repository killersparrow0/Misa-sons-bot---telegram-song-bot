# Β© MisaBots

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
from config import Config

bot = Client(
    'MeenutyBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------
@bot.on_message(filters.command(['start']))
def start(client, message):
    MeenutyBot = f'π Hello @{message.from_user.username}\n\nI am meenuty bot (https://telegra.ph/file/04828a131605f87a0cc7b.gif)\n I\'m Meenuty, I can download songs from YouTube. Type /s song name:'
    message.reply_text(
        text=MeenutyBot, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('SUPPORT π¬', url='https://t.me/movies_songs_tj'),
                    InlineKeyboardButton('ADD ME π€', url='https://t.me/meenuty_bot?startgroup=true')
                ]
            ]
        )
    )

@bot.on_message(filters.command(['s']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('π Searching the π§song...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('Found nothing. Try changing the spelling a littleπ')
            return
    except Exception as e:
        m.edit(
            "βοΈ Found Nothing. Sorry.\n\nTry another keywork or maybe spell it properly. ( Β΄β’οΈ΅β’` ) "
        )
        print(str(e))
        return
    m.edit("β³processingβ’β’β’β’")
    m.edit("βοΈProcessingβ’β’")
    m.edit("β¬οΈβ«οΈβ«οΈβ«οΈβ«οΈβ«οΈβ«οΈβ«οΈβ«οΈ")
    m.edit("β¬οΈβ¬οΈβ«οΈβ«οΈβ«οΈβ«οΈβ«οΈβ«οΈβ«οΈ")
    m.edit("β¬οΈβ¬οΈβ¬οΈβ«οΈβ«οΈβ«οΈβ«οΈβ«οΈβ«οΈ")
    m.edit("β¬οΈβ¬οΈβ¬οΈβ¬οΈβ«οΈβ«οΈβ«οΈβ«οΈβ«οΈ")
    m.edit("β¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ«οΈβ«οΈβ«οΈβ«οΈ")
    m.edit("β¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ«οΈβ«οΈβ«οΈ")
    m.edit("β¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ«οΈβ«οΈ")
    m.edit("β¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ«οΈ")
    m.edit("DREAM BIG β¨")
    m.edit("β’β’π΅DOWNLOADINGπ΅β’β’")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'π§ ππ’π­π₯π : [{title[:35]}]({link})\nβ³ ππ?π«ππ­π’π¨π§ : `{duration}`\nπ¬ ππ¨π?π«ππ : [Youtube](https://www.youtube.com/channel/UC8zUxxo11sqJZTkVyqj3OwQ)\nπβπ¨ ππ’ππ°π¬ : `{views}`\n\nπ ππ² : @misasong'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
         m.edit('β ERROR REPORT NOW @movies_songs_tj or @misasong')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
