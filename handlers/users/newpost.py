import logging
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS, CHANNELS
from keyboards.inline.manage_post import confirmation_keyboard, post_callback
from loader import dp, bot
from states.newpost import NewPost

@dp.message_handler(Command("yangi_post"))
async def create_post(message: Message):
    xabar = await message.answer("Chop etish uchun post yuboring.")

    await NewPost.NewMessage.set()

user_id = []
@dp.message_handler(state=NewPost.NewMessage,content_types=types.ContentTypes.ANY)
async def enter_message(message: Message, state: FSMContext):
    # await state.update_data(photo = message.photo,mention=message.from_user.get_mention())
    await state.update_data(photo = message.photo,text=message.html_text, mention=message.from_user.get_mention())
    await message.answer(f"Postni tekshirish uchun yuboraymi?",
                         reply_markup=confirmation_keyboard)
    id = message.from_user.id
    user_id.append(id)
    await NewPost.next()


@dp.callback_query_handler(post_callback.filter(action="post"), state=NewPost.Confirm)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = data.get("text")
        mention = data.get("mention")
        photo = data.get("photo")
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post Adminga yuborildi")
    await bot.send_message(ADMINS[0], f"Foydalanuvchi {mention} quyidagi postni chop etmoqchi:")
    for photo in photo:
        pass
    await bot.send_photo(ADMINS[0], photo.file_id,caption=text,reply_markup=confirmation_keyboard)


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=NewPost.Confirm)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post rad etildi.")


@dp.message_handler(state=NewPost.Confirm)
async def post_unknown(message: Message):
    await message.answer("Chop etish yoki rad etishni tanlang")


# @dp.callback_query_handler(post_callback.filter(action="post"), user_id=ADMINS)
# async def approve_post(call: CallbackQuery):
#     await call.message.answer("Chop etishga ruhsat berdingiz.")
#     target_channel = CHANNELS[0]
#     message = await call.message.edit_reply_markup()
#     await message.send_copy(chat_id=target_channel)
@dp.callback_query_handler(post_callback.filter(action="post"), user_id=ADMINS)
async def approve_post(call: CallbackQuery):
    await call.answer("Chop etishga ruhsat berdingiz.✅",show_alert=True)
    target_channel = CHANNELS[0]
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_channel)
    users_id = user_id[-1]
    logging.info(user_id)
    await bot.send_message(users_id, "✅ Tabriklaymiz Post kanalga Joylandi")
@dp.message_handler(user_id=ADMINS)
async def admin_comment(message: Message):
    await bot.send_message(user_id,message.text)

@dp.callback_query_handler(post_callback.filter(action="cancel"), user_id=ADMINS)
async def decline_post(call: CallbackQuery):
    await call.answer("Post rad etildi.", show_alert=True)
    await call.message.edit_reply_markup()
    target_channel = user_id[-1]
    await bot.send_message(target_channel, f"{call.message.text}❌ Afsuski Sizning postingiz rad etildi")