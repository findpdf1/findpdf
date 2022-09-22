import os
import asyncio
#from info import FORCE_SUB
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

FORCE_SUB = os.environ.get("FORCE_SUB", "-1001368430615")



async def ForceSub(bot: Client, event: Message):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=(int(FORCE_SUB) if FORCE_SUB.startswith("-100") else FORCE_SUB))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Unable to do Force Subscribe to {FORCE_SUB}\n\nError: {err}\n\nContact @vipinpkd")
        return 200
    try:
        user = await bot.get_chat_member(chat_id=(int(FORCE_SUB) if FORCE_SUB.startswith("-100") else FORCE_SUB), user_id=event.from_user.id)
        if user.status == "banned":
            await bot.send_message(
                chat_id=event.from_user.id,
                text="Sorry Sir, You are Banned to use me. Contact my [master](https://t.me/vipinpkd).",
                parse_mode="markdown",
                disable_web_page_preview=True,
                reply_to_message_id=event.message_id
            )
            return 400
        else:
            return 200
    except UserNotParticipant:
        await bot.send_message(
            chat_id=event.from_user.id,
            text="**Please Join My PDF Channel to use this Bot!**\n\n__Due to Overload, Only Channel Subscribers can use the Bot!__",
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("Join 📚PDF Channel", url=invite_link.invite_link)
                ]]                
            ),
            parse_mode="markdown",
            reply_to_message_id=event.message_id
        )
        return 400
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}\n\nContact @vipinpkd")
        return 200


@Client.on_message(filtes.private & filters.incoming & filters.text)
async def forcesub(client, message):
    FSub = await ForceSub(client, message)
    if FSub == 400:
        return

  