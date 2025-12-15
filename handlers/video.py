from aiogram import Router, types
from database.db import get_film_by_code, increment_download
from utils.check_subs import check_subscriptions
from config import REQUIRED_CHANNELS

router = Router()

@router.message()
async def handle_video_code(message: types.Message, bot):
    user_id = message.from_user.id
    text = message.text.strip()

    if not text.isdigit():
        return await message.answer("⚠️ Введи числовой код фильма!")

    is_ok = await check_subscriptions(bot, user_id, REQUIRED_CHANNELS)
    if not is_ok:
        return await message.answer("❌ Ты не подписан на нужные каналы!")

    film = get_film_by_code(int(text))
    if not film:
        return await message.answer("🎞 Фильм с таким кодом не найден!")

    film_id, code, title, message_id, downloads = film
    increment_download(code)

    await bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id="@hghghghghghg123123",
        message_id=message_id
    )
