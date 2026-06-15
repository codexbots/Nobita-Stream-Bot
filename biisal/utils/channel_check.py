from biisal.vars import Var
from biisal.bot import StreamBot
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def is_user_allowed(client, message):
    if Var.UPDATES_CHANNEL == "None":
        return True
    try:
        user = await client.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
        if user.status == "kicked":
            await client.send_message(
                chat_id=message.chat.id,
                text="ꜱᴏʀʀʏ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜꜱᴇ ᴍᴇ ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ ꜰᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟꜱ.",
                disable_web_page_preview=True
            )
            return False
    except UserNotParticipant:
        await StreamBot.send_photo(
            chat_id=message.chat.id,
            photo="https://graph.org/file/a8095ab3c9202607e78ad.jpg",
            caption=f"{message.from_user.mention},\n\n<b><i>⚠️ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ.</i></b>\n\n<i>ᴅᴜᴇ ᴛᴏ sᴇʀᴠᴇʀ ᴏᴠᴇʀʟᴏᴀᴅ, ᴏɴʟʏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʙᴏᴛ 😊</i>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("ᴊᴏɪɴ ɴᴏᴡ 🚩", url=f"https://telegram.me/{Var.UPDATES_CHANNEL}")
                    ]
                ]
            ),
        )
        return False
    except Exception:
        await client.send_message(
            chat_id=message.chat.id,
            text="<b>ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. ᴄᴏɴᴛᴀᴄᴛ ᴍʏ <a href='https://telegram.me/CallOwnerBot'>ᴏᴡɴᴇʀ</a></b>",
            disable_web_page_preview=True
        )
        return False
    return True
