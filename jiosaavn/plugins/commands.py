import logging
import asyncio
import random
from jiosaavn.bot import Bot
from jiosaavn.plugins.text import TEXT
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

#################### COMMAND ##########
@Bot.on_callback_query(filters.regex('^home$'))
@Bot.on_message(filters.command('start') & filters.private & filters.incoming)
async def start(c, m):
    last_name = f' {m.from_user.last_name}' if m.from_user.last_name else ''
    mention = f"[{m.from_user.first_name}{last_name}](tg://user?id={m.from_user.id})" if m.from_user.first_name else f"[User](tg://user?id={m.from_user.id})"
### Send reaction to command
    random_emoji = random.choice(TEXT.EMOJI_LIST)
    await c.send_reaction(
        chat_id=m.chat.id,
        message_id=m.id,
        emoji=random_emoji,
        big=True  # Set big animation for the reaction
    )
    await asyncio.sleep(0.5)
    msg = m.message if getattr(m, "data", None) else await m.reply("**Processing....⌛**", quote=True)
    try:
        buttons = [[
            InlineKeyboardButton('Owner 🧑', url='https://t.me/Ns_AnoNymous'),
            InlineKeyboardButton('About 📕', callback_data='about')
        ], [
            InlineKeyboardButton('Help 💡', callback_data='help'),
            InlineKeyboardButton('Settings ⚙', callback_data='settings')
        ], [
            InlineKeyboardButton('Open Source Repository 🌐', url='https://github.com/Ns-AnoNymouS/jiosaavn')
        ], [
            InlineKeyboardButton('Close ❌', callback_data='close')
           ]
        ]  
        logger.debug(f"User mention: {mention}")  
        await msg.edit(
            text=TEXT.START_MSG.format(mention=mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except KeyError as e:
        logger.error(f"Error in start command: {e}")
        await msg.edit(text="An error occurred while processing your request.")


@Bot.on_callback_query(filters.regex('^help$'))
@Bot.on_message(filters.command('help') & filters.private & filters.incoming)
async def help_handler(client: Bot, message: Message | CallbackQuery):
    try:
        buttons = [[
            InlineKeyboardButton('About 📕', callback_data='about'),
            InlineKeyboardButton('Settings ⚙', callback_data='settings')
        ], [
            InlineKeyboardButton('Home 🏕', callback_data='home'),
            InlineKeyboardButton('Close ❌', callback_data='close')
        ]]
        if isinstance(message, Message):
            await message.reply_text(
                text=TEXT.HELP_MSG,
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True
            )
        else:
            await message.message.edit(
                text=TEXT.HELP_MSG,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    except Exception as e:
        logger.error(f"Error in help_handler command: {e}")
        if isinstance(message, Message):
            await message.reply("An error occurred while processing your request.")
        else:
            await message.message.edit("An error occurred while processing your request.")

@Bot.on_callback_query(filters.regex('^about$'))
@Bot.on_message(filters.command('about') & filters.private & filters.incoming)
async def about(client: Bot, message: Message | CallbackQuery):
    try:
        me = await client.get_me()
        buttons = [[
            InlineKeyboardButton('Help 💡', callback_data='help'),
            InlineKeyboardButton('Settings ⚙', callback_data='settings')
        ], [
            InlineKeyboardButton('Home 🏕', callback_data='home'),
            InlineKeyboardButton('Close ❌', callback_data='close')
        ]]
        if isinstance(message, Message):
            await message.reply_text(
                text=TEXT.ABOUT_MSG.format(me=me),  # Updated to pass `me` directly
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=True,
                quote=True
            )
        else:
            await message.message.edit(
                text=TEXT.ABOUT_MSG.format(me=me),
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=True
            )
    except Exception as e:
        logger.error(f"Error in about command: {e}")
        if isinstance(message, Message):
            await message.reply("An error occurred while processing your request.")
        else:
            await message.message.edit("An error occurred while processing your request.")
            
@Bot.on_callback_query(filters.regex('^close$'))
async def close_cb(client: Bot, callback: CallbackQuery):
    try:
        await callback.answer()
        await callback.message.delete()
        await callback.message.reply_to_message.delete()
    except Exception as e:
        logger.error(f"Error in close_cb command: {e}")
        await callback.message.edit("An error occurred while closing the message.")
        
