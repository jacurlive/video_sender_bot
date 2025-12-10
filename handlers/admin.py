from aiogram import Router, types, F
from aiogram.filters import Command
from config import ADMIN_ID, STORAGE_CHANNEL
from database.db import get_next_code, add_film

router = Router()

@router.message(Command("add"))
async def add_command(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ У тебя нет прав использовать эту команду.")

    await message.answer("📥 Отправь видео и его описание в одном сообщении.")
    # Ставим состояние ожидания видео — упрощённый вариант без FSM
    router.data = {"waiting_for_video": True}

@router.message(F.video)
async def handle_video(message: types.Message, bot):
    # Проверка: бот действительно ждёт видео
    if not getattr(router, "data", {}).get("waiting_for_video"):
        return

    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Только админ может добавлять видео.")

    caption = message.caption or "Без описания"
    code = get_next_code()

    # Добавляем "KOD: X" в описание
    new_caption = f"{caption}\n\nKOD: {code}"

    # Отправляем видео в канал
    sent = await bot.send_video(
        chat_id=STORAGE_CHANNEL,
        video=message.video.file_id,
        caption=new_caption
    )

    # Сохраняем в БД
    add_film(code, caption, sent.message_id)

    # Отправляем админу подтверждение
    await message.answer(f"✅ Фильм успешно добавлен!\nКОД: {code}")

    # Сбрасываем состояние
    router.data["waiting_for_video"] = False
    return None
