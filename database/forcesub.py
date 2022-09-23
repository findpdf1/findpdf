#https://github.com/M299792458/chatSizeBot
import os
import time
from pyrogram.enums.parse_mode import ParseMode
#from bot import LOGGER
#from config import Config
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

class Config:
    FORCE_SUBSCRIBE_CHANNEL = os.environ.get('FORCE_SUBSCRIBE_CHANNEL','Pdfmalayalam') # force subscribe channel link.
    CHANNEL_OR_CONTACT = os.environ.get('CHANNEL_OR_CONTACT', "vipinpkd") # give your public channel or contact username

    JOIN_CHANNEL_STR = os.environ.get('JOIN_CHANNEL_STR',
        "Hi {}\n\n" + \
        "First Subscribe my Channel from Button, Try Again.\n" + \
        "Due to Overload, Only Channel Subscribers Can Use This Bot.")
    YOU_ARE_BANNED_STR = os.environ.get('YOU_ARE_BANNED_STR',
        "You are Banned to use me.\n\nfor further queries : {}")
    JOIN_BUTTON_STR = os.environ.get('JOIN_BUTTON_STR', "Join Our 📚PDF Channel")
 #-----------------------------#
 
tg_link_regex = "(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$"

    
def ForceSub(event: Message):
    """
    Custom Pyrogram Based Telegram Bot's Force Subscribe Function by @viharasenindu.
    If User is not Joined Force Sub Channel Bot to Send a Message & ask him to Join First.
    
    :param bot: Pass Client.
    :param event: Pass Message.
    :return: It will return 200 if Successfully Got User in Force Sub Channel and 400 if Found that User Not Participant in Force Sub Channel or User is Kicked from Force Sub Channel it will return 400. Also it returns 200 if Unable to Find Channel.
    """
    if Config.FORCE_SUBSCRIBE_CHANNEL is not None:
        try:
            invite_link = event._client.create_chat_invite_link(
                chat_id=(
                    int(Config.FORCE_SUBSCRIBE_CHANNEL) if Config.FORCE_SUBSCRIBE_CHANNEL.startswith("-100") else Config.FORCE_SUBSCRIBE_CHANNEL
                ),
                member_limit = 1
            )
        except FloodWait as e:
            time.sleep(e.value)
            fix_ = ForceSub(event)
            return fix_
        except Exception as err:
            #LOGGER.error(f"Error: {err}\nDo not forget to make admin your bot in forcesub channel.\nDestek / Support: {Config.CHANNEL_OR_CONTACT}") # debug
            return 200
        try:
            user = event._client.get_chat_member(chat_id=(int(Config.FORCE_SUBSCRIBE_CHANNEL) if Config.FORCE_SUBSCRIBE_CHANNEL.startswith("-100") else Config.FORCE_SUBSCRIBE_CHANNEL), user_id=event.from_user.id)
            if user.status == "kicked":
                event.reply_text(
                    text=Config.YOU_ARE_BANNED_STR.format(Config.CHANNEL_OR_CONTACT),
                    parse_mode = ParseMode.HTML,
                    disable_notification=True,
                    disable_web_page_preview=True,
                    reply_to_message_id = event.id
                )
                return 400
            else:
                return 200
        except UserNotParticipant:
            event.reply_text(
                text=Config.JOIN_CHANNEL_STR.format(event.from_user.mention),
                parse_mode = ParseMode.HTML,
                disable_notification=True,
                reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"{Config.JOIN_BUTTON_STR}", url=invite_link.invite_link)
                    ]
                ]
                ),
                disable_web_page_preview=True,
                reply_to_message_id = event.id
            )
            return 400
        except FloodWait as e:
            time.sleep(e.value)
            fix_ = ForceSub(event)
            return fix_
        except Exception as err:
            #LOGGER.error(f"Error: {err}\nDo not forget to make admin your bot in forcesub channel.\nDestek / Support: {Config.CHANNEL_OR_CONTACT}") # debug
            return 200
    else:
        return 200
        
        
@Client.on_message((filters.forwarded | ((filters.regex(tg_link_regex)) & filters.text)) & filters.private & filters.incoming)
def handler(client, message: Message):
    if ForceSub(message) == 400:
    return