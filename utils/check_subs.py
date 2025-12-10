from aiogram import Bot

async def check_subscriptions(bot: Bot, user_id: int, channels: list, groups: None) -> bool:
    for ch in channels:
        try:
            member = await bot.get_chat_member(ch, user_id)
            if member.status == "left":
                return False
        except Exception as e:
            print(e)
            return False

    return True
