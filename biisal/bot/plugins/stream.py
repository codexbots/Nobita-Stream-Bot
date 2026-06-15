#(c) Adarsh-Goel
#(c) @biisal
#(c) TechifyBots
import os
import asyncio
import requests
import string
import random
from asyncio import TimeoutError
from biisal.bot import StreamBot
from biisal.utils.database import Database
from biisal.utils.human_readable import humanbytes
from biisal.vars import Var
from urllib.parse import quote_plus
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from biisal.utils.file_properties import get_name, get_hash, get_media_file_size
from biisal.utils.channel_check import is_user_allowed
db = Database(Var.DATABASE_URL, Var.name)

def generate_random_alphanumeric(): 
    """Generate a random 8-letter alphanumeric string.""" 
    characters = string.ascii_letters + string.digits 
    random_chars = ''.join(random.choice(characters) for _ in range(8)) 
    return random_chars 

def get_shortlink(url): 
    rget = requests.get(f"https://{Var.SHORTLINK_URL}/api?api={Var.SHORTLINK_API}&url={url}&alias={generate_random_alphanumeric()}") 
    rjson = rget.json() 
    if rjson["status"] == "success" or rget.status_code == 200: 
        return rjson["shortenedUrl"] 
    else: 
        return url

MY_PASS = os.environ.get("MY_PASS", None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")


async def self_cleanup(*messages, delay):
    await asyncio.sleep(delay)
    for msg in messages:
        try:
            await msg.delete()
        except Exception:
            pass

msg_text ="""
<b>ʏᴏᴜʀ ʟɪɴᴋ ɪs ɢᴇɴᴇʀᴀᴛᴇᴅ...⚡</b>

<b>📧 ꜰɪʟᴇ ɴᴀᴍᴇ :- </b> <i>{}</i>

<b>📦 ꜰɪʟᴇ sɪᴢᴇ :- </b> <i>{}</i>

<b>⚠️ ᴛʜɪꜱ ʟɪɴᴋ ᴡɪʟʟ ᴇxᴘɪʀᴇ ᴀꜰᴛᴇʀ 𝟼 ʜᴏᴜʀꜱ</b>

<b>❇️ ʙʏ : @TechifyBots</b>"""

@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio | filters.photo) , group=4)
async def private_receive_handler(c: Client, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.NEW_USER_LOG,
            f"#𝐍𝐞𝐰𝐔𝐬𝐞𝐫\n\n**᚛› 𝐍𝐚𝐦𝐞 - [{m.from_user.first_name}](tg://user?id={m.from_user.id})**"
        )
    if not await is_user_allowed(c, m):
        return
    ban_chk = await db.is_banned(int(m.from_user.id))
    if ban_chk == True:
        return await m.reply(Var.BAN_ALERT)

    try:
        log_msg = await m.copy(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        stream = stream_link
        download = online_link
        if Var.SHORTLINK:
            try:
                stream = get_shortlink(stream_link)
                download = get_shortlink(online_link)
            except Exception as e:
                print(f"Shortlink error, using direct links: {e}")

        a = await log_msg.reply_text(
            text=f"ʀᴇǫᴜᴇꜱᴛᴇᴅ ʙʏ : [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nUꜱᴇʀ ɪᴅ : {m.from_user.id}\nStream ʟɪɴᴋ : {stream_link}",
            disable_web_page_preview=True, quote=True
        )
        k = await m.reply_text(
            text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m))),
            quote=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ꜱᴛʀᴇᴀᴍ •", url=stream),
                 InlineKeyboardButton("• ᴅᴏᴡɴʟᴏᴀᴅ •", url=download)],
                [InlineKeyboardButton('🧿 ᴡᴀᴛᴄʜ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ 🖥', web_app=WebAppInfo(url=stream))]
            ])
        )

        await m.delete()

        asyncio.create_task(self_cleanup(log_msg, a, k, 21600))

    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True)

@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.photo)  & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Var.BAN_CHNL:
        print("chat trying to get straming link is found in BAN_CHNL,so im not going to give stram link")
        return
    ban_chk = await db.is_banned(int(broadcast.chat.id))
    if (int(broadcast.chat.id) in Var.BANNED_CHANNELS) or (ban_chk == True):
        await bot.leave_chat(broadcast.chat.id)
        return
    try:  # This is the outer try block
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        stream = stream_link
        download = online_link
        if Var.SHORTLINK:
            try:
                stream = get_shortlink(stream_link)
                download = get_shortlink(online_link)
            except Exception as e:
                print(f"Shortlink error, using direct links: {e}")

        await log_msg.reply_text(
            text=f"**Channel Name:** `{broadcast.chat.title}`\n**CHANNEL ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {stream_link}",
            quote=True
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ꜱᴛʀᴇᴀᴍ 🔺", url=stream),
                 InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ 🔻", url=download)]
            ])
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                            text=f"GOT FLOODWAIT OF {str(w.x)}s FROM {broadcast.chat.title}\n\n**CHANNEL ID:** `{str(broadcast.chat.id)}`",
                            disable_web_page_preview=True)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ERROR_TRACKEBACK:** `{e}`", disable_web_page_preview=True)
        print(f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\nEʀʀᴏʀ:  **Give me edit permission in updates and bin Channel!{e}**")
