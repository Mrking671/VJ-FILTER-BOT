# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Clone Code Credit : YT - @Tech_VJ / TG - @VJ_Bots / GitHub - @VJBots

from info import API_ID, API_HASH, CLONE_MODE, LOG_CHANNEL
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from database.users_chats_db import db
import re
from Script import script

@Client.on_message(filters.command('clone'))
async def clone_menu(client, message):
    if not CLONE_MODE:
        return

    techvj = await client.ask(message.chat.id, "<b>1) sᴇɴᴅ <code>/newbot</code> ᴛᴏ @BotFather\n2) ɢɪᴠᴇ ᴀ ɴᴀᴍᴇ ꜰᴏʀ ʏᴏᴜʀ ʙᴏᴛ.\n3) ɢɪᴠᴇ ᴀ ᴜɴɪǫᴜᴇ ᴜsᴇʀɴᴀᴍᴇ.\n4) ᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴀ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ ʏᴏᴜʀ ʙᴏᴛ ᴛᴏᴋᴇɴ.\n5) ꜰᴏʀᴡᴀʀᴅ ᴛʜᴀᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴍᴇ.\n\n/cancel - ᴄᴀɴᴄᴇʟ ᴛʜɪs ᴘʀᴏᴄᴇss.</b>")
    
    if techvj.text == '/cancel':
        await techvj.delete()
        return await message.reply('<b>ᴄᴀɴᴄᴇʟᴇᴅ ᴛʜɪs ᴘʀᴏᴄᴇss 🚫</b>')
    
    if techvj.forward_from and techvj.forward_from.id == 93372553:
        try:
            bot_token = re.findall(r"\b(\d+:[A-Za-z0-9_-]+)\b", techvj.text)[0]
        except:
            return await message.reply('<b>sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ 😕</b>')
    else:
        return await message.reply('<b>ɴᴏᴛ ꜰᴏʀᴡᴀʀᴅᴇᴅ ꜰʀᴏᴍ @BotFather 😑</b>')
    
    user_id = message.from_user.id
    msg = await message.reply_text("**👨‍💻 ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ ɪ ᴀᴍ ᴄʀᴇᴀᴛɪɴɢ ʏᴏᴜʀ ʙᴏᴛ ❣️**")
    
    try:
        vj = Client(
            f"{bot_token}", API_ID, API_HASH,
            bot_token=bot_token,
            plugins={"root": "CloneTechVJ"}
        )
        await vj.start()
        bot = await vj.get_me()
        await db.add_clone_bot(user_id, bot.id, bot_token)
        await msg.edit_text(f"<b>sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴏɴᴇᴅ ʏᴏᴜʀ ʙᴏᴛ: @{bot.username}.\n\nʏᴏᴜ ᴄᴀɴ ᴄᴜsᴛᴏᴍɪsᴇ ʏᴏᴜʀ ᴄʟᴏɴᴇ ʙᴏᴛ ʙʏ /settings ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʏᴏᴜʀ ᴄʟᴏɴᴇ ʙᴏᴛ</b>")
    except BaseException as e:
        await msg.edit_text(f"⚠️ <b>Bot Error:</b>\n\n<code>{e}</code>\n\n**Kindly forward this message to @KingVJ01 to get assistance.**")

@Client.on_message(filters.command('listclones'))
async def list_clones(client, message):
    user_id = message.from_user.id
    clones = await db.get_clones(user_id)
    
    if not clones:
        return await message.reply("**ɴᴏ ᴄʟᴏɴᴇ ʙᴏᴛs ғᴏᴜɴᴅ**")
    
    clone_list = "\n".join([f"- @{bot['bot_id']}" for bot in clones])
    await message.reply(f"**Your cloned bots:**\n{clone_list}")

@Client.on_message(filters.command('deleteclone'))
async def delete_clone_menu(client, message):
    user_id = message.from_user.id
    clones = await db.get_clones(user_id)
    
    if not clones:
        return await message.reply("**ɴᴏ ᴄʟᴏɴᴇ ʙᴏᴛs ғᴏᴜɴᴅ**")
    
    if len(message.command) < 2:
        clone_list = "\n".join([f"- @{bot['bot_id']}" for bot in clones])
        return await message.reply(f"**Specify which clone to delete:**\n{clone_list}")
    
    bot_id = message.command[1]
    await db.delete_clone(user_id, bot_id)
    await message.reply(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴄʟᴏɴᴇ ʙᴏᴛ: {bot_id}**")

async def restart_bots():
    bots_cursor = await db.get_all_bots()
    bots = await bots_cursor.to_list(None)
    for bot in bots:
        bot_token = bot['bot_token']
        try:
            vj = Client(
                f"{bot_token}", API_ID, API_HASH,
                bot_token=bot_token,
                plugins={"root": "CloneTechVJ"},
            )
            await vj.start()
        except Exception as e:
            print(f"Error while restarting bot with token {bot_token}: {e}")

# Database functions to handle multiple clones per user
async def add_clone_bot(user_id, bot_id, bot_token):
    await collection.update_one(
        {'user_id': user_id},
        {'$push': {'clones': {'bot_id': bot_id, 'bot_token': bot_token}}},
        upsert=True
    )

async def get_clones(user_id):
    user_data = await collection.find_one({'user_id': user_id})
    return user_data['clones'] if user_data and 'clones' in user_data else []

async def delete_clone(user_id, bot_id):
    await collection.update_one(
        {'user_id': user_id},
        {'$pull': {'clones': {'bot_id': bot_id}}}
    )
