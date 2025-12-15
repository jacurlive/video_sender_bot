from aiogram import Bot
from aiogram.types import ChatMember

async def check_subscriptions(bot: Bot, user_id: int, channels: list) -> bool:
    for ch in channels:
        try:
            member: ChatMember = await bot.get_chat_member(ch, user_id)

            # Разрешённые статусы
            allowed_statuses = [
                "member",
                "administrator",
                "creator",
                "restricted",
            ]

            if member.status not in allowed_statuses:
                return False

        except Exception as e:
            print(f"Ошибка проверки канала {ch}: {e}")
            return False

    return True
