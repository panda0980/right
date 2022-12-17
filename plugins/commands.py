import traceback
import asyncio
from io import BytesIO
from pyrogram import enums
from pyrogram import filters,Client
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
from pyrogram.errors import PeerIdInvalid, ChannelInvalid
from plugins.send_to_users import broadcast
from plugins.database import Database
from plugins.text import welcome_text, ad_text
import config
from io import BytesIO


DATA_URL = config.DATA_URL
DATA_NAME = config.DATA_NAME

db = Database(DATA_URL, DATA_NAME)

AUTH_USERS = config.AUTH_USERS



  
 
@Client.on_message(filters.command("start"))
async def startprivate(Client, message):
    # return
    chat_type = message.chat.type
    chat_id = message.from_user.id
    name = message.from_user.first_name or message.from_user.username
    group_id =message.chat.id
    title= message.chat.title
    bot= await Client.get_me()
    user = message.from_user.mention
    
    keyboard= [
    [InlineKeyboardButton("Private chat", url=f"t.me/{bot.username}?start")]
    ]
    
    
    if chat_type == enums.ChatType.PRIVATE:
        if not await db.is_user_exist(chat_id):
            data = await Client.get_me()
            BOT_USERNAME = data.username
            await db.add_user(chat_id, name)
            
            
       
        await message.reply_text(welcome_text.format(user))


    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        groups = await db.is_group_exist(group_id)
        
        if groups == False:
            await db.add_chat(group_id,title)
        
        await message.reply_text(
            text ="Please use this bot in private mode",
            reply_markup = InlineKeyboardMarkup(keyboard)
            )
            

    



        
@Client.on_message(filters.private & filters.command("send"))
async def broadcast_handler_open(Client, message):
    reply = message.reply_to_message
    user = message.from_user.id
    
    if user not in AUTH_USERS:
        await message.delete()
        await message.reply_text("you are not a authorised person to use this command")
        
        
    else:
        if not reply:
            await message.reply_text("Please reply to message to broadcast")
        else:
            await broadcast(db, message)
            

@Client.on_message(filters.private & filters.command("stats"))
async def sts(Client, message):
    if message.from_user.id not in AUTH_USERS:
        await message.delete()
        return
    await message.reply_text(
        text=f"**Total Users in bot server** :{await db.total_users_count()}\n\n**Total groups in bot server** :{await db.total_chat_count()}",
        quote=True,
    )
        



    

@Client.on_message(filters.command("advertise"))
async def welcome(Client, message):
    user= message.from_user.mention
    bot = await Client.get_users("me")
    chat_type = message.chat.type

    keyboard1=[
        [InlineKeyboardButton("Pay", url=f"t.me/{bot.username}?start")]
        ]

    keyboard2=[
        [InlineKeyboardButton("Private chat", url=f"t.me/{bot.username}?start")]
    ]
    
    
    if chat_type == enums.ChatType.PRIVATE:
        await message.reply_text(
            text = ad_text.format(user),
            reply_markup = InlineKeyboardMarkup(keyboard1)
        )

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await message.reply_text(
            text = "This command only to be used in private",
            reply_markup = InlineKeyboardMarkup(keyboard2)
        )
        
def get_file_id(msg):
    if msg.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            "sticker"
        ):
            obj = getattr(msg, message_type)
            if obj:
                setattr(obj, "message_type", message_type)
                return obj


@Client.on_message(filters.command("id"))
async def showid(client, message):
    chat_type = message.chat.type
    
    if chat_type == enums.ChatType.PRIVATE:
        
        user_id = message.chat.id
        first = message.from_user.first_name
        last = message.from_user.last_name or ""
        username = message.from_user.username
        dc_id = message.from_user.dc_id or ""
        await message.reply_text(
            f"<b>➲ First Name:</b> {first}\n<b>➲ Last Name:</b> {last}\n<b>➲ Username:</b> @{username}\n<b>➲ Telegram ID:</b> <code>{user_id}</code>\n<b>➲ Data Centre:</b> <code>{dc_id}</code>",
            quote=True
        )

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        _id = ""
        _id += (
            "<b>➲ Chat ID</b>: "
            f"<code>{message.chat.id}</code>\n"
        )
        if message.reply_to_message:
            _id += (
                "<b>➲ User ID</b>: "
                f"<code>{message.from_user.id if message.from_user else 'Anonymous'}</code>\n"
                "<b>➲ Replied User ID</b>: "
                f"<code>{message.reply_to_message.from_user.id if message.reply_to_message.from_user else 'Anonymous'}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
        else:
            _id += (
                "<b>➲ User ID</b>: "
                f"<code>{message.from_user.id if message.from_user else 'Anonymous'}</code>\n"
            )
            file_info = get_file_id(message)
        if file_info:
            _id += (
                f"<b>{file_info.message_type}</b>: "
                f"<code>{file_info.file_id}</code>\n"
            )
        await message.reply_text(
            _id,
            quote=True
            )  
    
    
       
@Client.on_message(filters.command("send_group") & filters.private)
async def broadcast(bot, message):
    user_id = message.from_user.id
    if user_id in AUTH_USERS:
        text = message.reply_to_message
        groups = await db.get_all_chats()
        if not message.reply_to_message:
            await message.reply_text("please reply to a message")
            
        else:
            failed = 0
            sent = 0
            msg = await message.reply_text("sending broadcast...")
            async for chat in groups:
                if sent % 25 == 0:
                    await asyncio.sleep(1)
                try:
                    await text.copy(chat_id =chat["id"] )
                    sent += 1
                except (PeerIdInvalid, ChannelInvalid):
                    failed += 1
                    LOGGER .warning("Can't send broadcast to \"%s\" with id %s",
                                   chat["title"], chat["id"])
            await msg.edit_text(
                "Broadcast complete!\n"
                f"{sent} groups succeed, {failed} groups failed to receive the message"
            )



    else:
        message.reply_text("you are not a authorised person to use this command")

    







@Client.on_message(filters.command("chatlist") & filters.private)
async def chatlist(self, message):
        """ Send file of chat's I'm in """
        chatfile = "List of chats.\n"
        chat_lists = await db.get_all_chats()
        async for chat in chat_lists:
            chatfile += "{} - ({})\n".format(chat["title"],
                                             chat["id"])

        with BytesIO(str.encode(chatfile)) as output:
            output.name = "chatlist.txt"
            await message.reply_document(
                document=output,
                caption="Here is the list of chats in my database.",
            )
