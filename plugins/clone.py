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
    if CLONE_MODE == False:
        return 
    techvj = await client.ask(message.chat.id, "<b>1) sᴇɴᴅ <code>/newbot</code> ᴛᴏ @BotFather\n2) ɢɪᴠᴇ ᴀ ɴᴀᴍᴇ ꜰᴏʀ ʏᴏᴜʀ ʙᴏᴛ.\n3) ɢɪᴠᴇ ᴀ ᴜsᴇʀɴᴀᴍᴇ ᴜɴɪǫᴜᴇ.\n4) ᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴀ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ ʏᴏᴜʀ ʙᴏᴛ ᴛᴏᴋᴇɴ.\n5) ꜰᴏʀᴡᴀʀᴅ ᴛʜᴀᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴍᴇ.\n\n/cancel - ᴄᴀɴᴄᴇʟ ᴛʜɪs ᴘʀᴏᴄᴇss.</b>")
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
    msg = await message.reply_text("👨‍💻 ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ ɪ ᴀᴍ ᴄʀᴇᴀᴛɪɴɢ ʏᴏᴜʀ ʙᴏᴛ ❣️")
    
    # Send a request to log channel for approval
    log_msg = await client.send_message(
        LOG_CHANNEL,
        f"**New Clone Request**\n\nUser: {message.from_user.mention} ({message.from_user.id})\nBot Token: <code>{bot_token}</code>\n\nApprove this request?",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Approve", callback_data=f"approve_clone:{user_id}:{bot_token}"),
                InlineKeyboardButton("Reject", callback_data=f"reject_clone:{user_id}:{bot_token}")]
            ]
        )
    )
    await msg.edit_text(f"<b>Request sent for approval. Please wait for approval in the log channel.</b>")

@Client.on_callback_query(filters.regex(r"approve_clone:(\d+):(.+)"))
async def approve_clone(client, callback_query):
    user_id, bot_token = callback_query.data.split(":")[1], callback_query.data.split(":")[2]
    msg = await callback_query.message.reply_text(f"<b>Approving clone for user {user_id}...</b>")
    try:
        vj = Client(
            f"{bot_token}", API_ID, API_HASH,
            bot_token=bot_token,
            plugins={"root": "CloneTechVJ"}
        )
        await vj.start()
        bot = await vj.get_me()
        await db.add_clone_bot(bot.id, user_id, bot_token)
        await msg.edit_text(f"<b>sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴏɴᴇᴅ ʏᴏᴜʀ ʙᴏᴛ: @{bot.username}.</b>")
        await client.send_message(user_id, f"<b>Your bot @{bot.username} has been approved and is now active.</b>")
    except BaseException as e:
        await msg.edit_text(f"⚠️ <b>Bot Error:</b>\n\n<code>{e}</code>\n\nKindly forward this message to @KingVJ01 to get assistance.")
    await callback_query.message.delete()

@Client.on_callback_query(filters.regex(r"reject_clone:(\d+):(.+)"))
async def reject_clone(client, callback_query):
    user_id, bot_token = callback_query.data.split(":")[1], callback_query.data.split(":")[2]
    await client.send_message(user_id, "<b>Your bot cloning request has been rejected.</b>")
    await callback_query.message.delete()

@Client.on_message(filters.command('deleteclone'))
async def delete_clone_menu(client, message):
    clones = await db.get_clones(message.from_user.id)
    if clones:
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"Delete {clone['bot_id']}", callback_data=f"delete_clone:{clone['bot_id']}")] for clone in clones]
        )
        await message.reply("Select the bot you want to delete:", reply_markup=reply_markup)
    else:
        await message.reply("ɴᴏ ᴄʟᴏɴᴇ ʙᴏᴛs ғᴏᴜɴᴅ")

@Client.on_callback_query(filters.regex(r"delete_clone:(\d+)"))
async def confirm_delete_clone(client, callback_query):
    bot_id = int(callback_query.data.split(":")[1])
    await db.delete_clone_by_id(callback_query.from_user.id, bot_id)
    await callback_query.message.edit_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ʙᴏᴛ ᴡɪᴛʜ ID {bot_id}, ʏᴏᴜ ᴄᴀɴ ᴄʀᴇᴀᴛᴇ ᴀɢᴀɪɴ ʙʏ /clone")

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
