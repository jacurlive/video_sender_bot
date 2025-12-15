from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db import add_user
from utils.check_subs import check_subscriptions
from config import REQUIRED_CHANNELS

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message, bot):
    user = message.from_user
    add_user(user.id, user.username or "-")

    is_ok = await check_subscriptions(bot, user.id, REQUIRED_CHANNELS)
    if not is_ok:
        builder = InlineKeyboardBuilder()

        # создаём по одной кнопке на каждый канал
        for idx, ch in enumerate(REQUIRED_CHANNELS, start=1):
            username = ch.replace("@", "")
            builder.row(
                types.InlineKeyboardButton(
                    text=f"📢 Канал {idx}",
                    url=f"https://t.me/{username}"
                )
            )

        # кнопка "Проверить подписку"
        builder.row(
            types.InlineKeyboardButton(
                text="✅ Проверить подписку",
                callback_data="check_subs"
            )
        )

        await message.answer(
            "🚫 Чтобы пользоваться ботом, подпишись на каналы:\n\n"
            "После этого нажми «✅ Проверить подписку».",
            reply_markup=builder.as_markup()
        )
        return

    await message.answer("✅ Привет! Отправь код фильма (например: 4)")


@router.callback_query(F.data == "check_subs")
async def check_subscription_callback(callback: types.CallbackQuery, bot):
    user_id = callback.from_user.id

    is_ok = await check_subscriptions(bot, user_id, REQUIRED_CHANNELS)
    if is_ok:
        await callback.message.edit_text("✅ Отлично! Ты подписан.\nТеперь отправь код фильма (например: 4)")
    else:
        await callback.answer("❌ Подписка не найдена. Проверь ещё раз.", show_alert=True)
