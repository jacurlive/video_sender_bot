from aiogram import Bot

async def check_subscriptions(bot: Bot, user_id: int, channels: list, groups: None) -> bool:
    # Проверяем все каналы
    for ch in channels:
        try:
            member = await bot.get_chat_member(ch, user_id)
            if member.status == "left":
                return False
        except Exception as e:
            print(e)
            return False

    # Проверяем все группы
    # for group_id in groups:
    #     try:
    #         member = await bot.get_chat_member(group_id, user_id)
    #         if member.status == "left":
    #             return False
    #     except Exception as e:
    #         print(e)
    #         return False

    return True
