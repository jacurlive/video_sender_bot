from aiogram import Router, types
from database.db import get_film_by_code, increment_download
from utils.check_subs import check_subscriptions
from config import REQUIRED_CHANNELS_ID, ADMIN_ID

router = Router()

@router.message()
async def handle_video_code(message: types.Message, bot):
    user_id = message.from_user.id
    text = message.text.strip()

    if not text.isdigit():
        return await message.answer("⚠️ Введи числовой код фильма!\n\n⚠️ Enter the movie's numeric code!")

    is_ok = await check_subscriptions(bot, user_id, REQUIRED_CHANNELS_ID)
    if not is_ok:
        return await message.answer("❌ Ты не подписан на нужные каналы!Нажми /start\n\n❌ You're not subscribed to the channels you want! Press /start")

    film = get_film_by_code(int(text))
    if not film:
        return await message.answer("🎞 Movie with this code not found!")

    film_id, code, title, message_id, downloads = film
    increment_download(code)

    await bot.send_message(ADMIN_ID, f"User: @{message.from_user.username} - {message.from_user.id} \n\n\n Code: {text}")
    await bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id="@hghghghghghg123123",
        message_id=message_id
    )
