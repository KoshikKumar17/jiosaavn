from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req
from .download import download

@Client.on_callback_query(filters.regex('^open\+'))
async def opensong(c, m):
    await m.answer()
    id = m.data.split('+')
    song_id = m.data.split('+')[1]
    album_id = None
    if len(id) == 3:
        album_id = m.data.split('+')[2]
    print(song_id)
    url = 'https://www.jiosaavn.com/api.php?'
    params = {
        '__call': 'song.getDetails',
        'cc': 'in',
        '_marker': '0%3F_marker%3D0',
        '_format': 'json',
        'pids': song_id
    }
    data = (await req(url, params))[song_id]
    album_url = data['album_url'].encode().decode() if 'album_url' in data else ''
    image_url = data['image'].encode().decode().replace("150x150", "500x500") if 'image' in data else ''
    song_url = data['perma_url'].encode().decode() if 'perma_url' in data else ''

    text = f"[\u2063]({image_url})"
    text += f"**🎧 Song:** [{data['song']}]({song_url})\n\n" if 'song' in data else ''
    text += f"**📚 Album:** [{data['album']}]({album_url})\n\n" if 'album' in data else ''
    text += f"**🥁 Music:** {data['music']}\n\n" if 'music' in data else ''
    text += f"**👨‍🎤 Singers:** {data['singers']}\n\n" if 'singers' in data else ''
    text += f"**📰 Language:** {data['language']}\n\n" if 'language' in data else ''
    text += f"**📆 Release Date:** __{data['release_date']}__\n\n" if 'release_date' in data else ''

    type = await c.db.get_type(m.from_user.id)
    type = 'all' if type == 'all' else 'song'
    back_cb = f'album+{album_id}' if album_id else f'nxt+{type}+1'
    buttons = [[
        InlineKeyboardButton('lyrics', callback_data='lyrics'),
        InlineKeyboardButton('Upload to TG 📤', callback_data=f'upload+{song_id}+song')
        ],[
        InlineKeyboardButton('🔙', callback_data=back_cb)
    ]]
    try:
        await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass


@Client.on_callback_query(filters.regex('^upload\+'))
async def upload_cb(c, m):
    await m.answer()
    await download(c, m, True)
