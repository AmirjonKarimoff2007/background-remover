from loader import dp, Bot
from aiogram.types import ContentType, Message
from pathlib import Path

download_path = Path().joinpath("downloads","categories")
download_path.mkdir(parents=True, exist_ok=True)


@dp.message_handler(content_types=ContentType.ANY)
async def download_items(message: Message):
    if message.content_type=='document':
        await message.document.download(destination=download_path)
        await message.reply(f"Siz {message.content_type} yubordingiz")
    # rasm
    elif message.content_type=='photo':
        await message.photo[-1].download(destination=download_path)
        await message.reply(f"Siz {message.content_type} yubordingiz fileid=={message.photo[-1].file_id}")
    # musiqa
    elif message.content_type=='audio':
        await message.audio.download(destination=download_path)
        await message.reply(f"Siz {message.content_type} yubordingiz")
    # sticker
    elif message.content_type=='sticker':
        await message.sticker.download(destination=download_path)
        await message.reply(f"Siz  {message.content_type} yubordingiz")