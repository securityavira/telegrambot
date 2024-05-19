import asyncio
import random

import config
import utils
from loader import dp
from aiogram import types


async def even_game(data: dict):
    msg_dice = await dp.bot.send_dice(config.CHANNEL_ID)

    await asyncio.sleep(2)

    if msg_dice.dice.value % 2:
        await utils.lose_notify(
            f"Выпало значение {msg_dice.dice.value}.",
            "https://i.imgur.com/V63Bk1U.png"
        )

        return (0,)
    else:
        return (
            float(round(data['bid'] * 1.9, 2)), 
            await utils.win_notify(
                float(round(data['bid'] * 1.9, 2)),
                f"Выпало значение {msg_dice.dice.value}.",
                "https://i.imgur.com/aGyuJ0Y.png"
            )
        )


async def odd_game(data: dict):
    msg_dice = await dp.bot.send_dice(config.CHANNEL_ID)

    await asyncio.sleep(2)

    if not msg_dice.dice.value % 2:
        msg = await utils.lose_notify(
            f"Выпало значение {msg_dice.dice.value}.",
            "https://i.imgur.com/aGyuJ0Y.png"
        )

        return (0,)
    else:
        return (
            float(round(data['bid'] * 1.9, 2)),
                await utils.win_notify(
                float(round(data['bid'] * 1.9, 2)),
                f"Выпало значение {msg_dice.dice.value}.",
                "https://i.imgur.com/V63Bk1U.png"
            )
        )


async def more_game(data: dict):
    msg_dice = await dp.bot.send_dice(config.CHANNEL_ID)

    await asyncio.sleep(2)

    if msg_dice.dice.value < 4:
        msg = await utils.lose_notify(
            f"Выпало значение {msg_dice.dice.value}.",
            "https://i.imgur.com/Iiim5Y4.png"
        )

        return (0,)
    else:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.9, 2)),
            f"Выпало значение {msg_dice.dice.value}.",
            "https://i.imgur.com/VoCoxdx.png"
        )

        return (float(round(data['bid'] * 1.9)), msg,)


async def less_game(data: dict):
    msg_dice = await dp.bot.send_dice(config.CHANNEL_ID)

    await asyncio.sleep(2)

    if msg_dice.dice.value > 3:
        msg = await utils.lose_notify(
            f"Выпало значение {msg_dice.dice.value}.",
            "https://i.imgur.com/VoCoxdx.png"
        )
        return (0,)
    else:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.9, 2)),
            f"Выпало значение {msg_dice.dice.value}.",
            "https://i.imgur.com/Iiim5Y4.png"
        )
        return (float(round(data['bid'] * 1.9, 2)), msg,)


async def first_win(data: dict):
    msg_dice_first = await dp.bot.send_dice(config.CHANNEL_ID)
    msg_dice_second = await dp.bot.send_dice(config.CHANNEL_ID)

    await asyncio.sleep(2)

    if msg_dice_first.dice.value > msg_dice_second.dice.value:
        msg = await utils.win_notify(
            float(round(data['bid'] * 2.8, 2)),
            f"Сессия закрыта [{msg_dice_first.dice.value}:{msg_dice_second.dice.value}] в пользу первого кубика.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (float(round(data['bid'] * 2.8, 2)), msg,)
    elif msg_dice_first.dice.value == msg_dice_second.dice.value:
        msg = await utils.lose_notify(
            f"Сессия закрыта [{msg_dice_first.dice.value}:{msg_dice_second.dice.value}], ничья",
            "https://i.imgur.com/IfazgLa.png"
        )

        return (data["bid"] / 2, msg,)
    else:
        msg = await utils.lose_notify(
            f"Сессия закрыта [{msg_dice_first.dice.value}:{msg_dice_second.dice.value}] в пользу второго кубика.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (0,)


async def second_win(data: dict):
    msg_dice_first = await dp.bot.send_dice(config.CHANNEL_ID)
    msg_dice_second = await dp.bot.send_dice(config.CHANNEL_ID)

    await asyncio.sleep(2)

    if msg_dice_first.dice.value < msg_dice_second.dice.value:
        msg = await utils.win_notify(
            float(round(data['bid'] * 2.8, 2)),
            f"Сессия закрыта [{msg_dice_first.dice.value}:{msg_dice_second.dice.value}] в пользу второго кубика.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 2.8, 2)), msg,)
    elif msg_dice_first.dice.value == msg_dice_second.dice.value:
        msg = await utils.lose_notify(
            f"Сессия закрыта [{msg_dice_first.dice.value}:{msg_dice_second.dice.value}], ничья",
            "https://i.imgur.com/IfazgLa.png"
        )
        
        return (data["bid"] / 2, msg,)
    else:
        msg = await utils.lose_notify(
            f"Сессия закрыта [{msg_dice_first.dice.value}:{msg_dice_second.dice.value}] в пользу первого кубика.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (0,)


async def bowling_first_win(data: dict):
    msg_dice_first = config.bowling_values.get(
        (await dp.bot.send_dice(config.CHANNEL_ID, emoji="🎳")).dice.value
    )
    msg_dice_second = config.bowling_values.get(
        (await dp.bot.send_dice(config.CHANNEL_ID, emoji="🎳")).dice.value
    )

    await asyncio.sleep(2)

    if msg_dice_first > msg_dice_second:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.7, 2)),
            f"Сессия закрыта [{msg_dice_first}:{msg_dice_second}] в пользу первого броска.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (float(round(data['bid'] * 1.7, 2)), msg,)
    elif msg_dice_first == msg_dice_second:
        msg = await utils.lose_notify(
            f"Сессия закрыта [{msg_dice_first}:{msg_dice_second}], ничья",
            "https://i.imgur.com/IfazgLa.png"
        )

        return (data["bid"] / 2, msg,)
    else:
        msg = await utils.lose_notify(
            f"Сессия закрыта [{msg_dice_first}:{msg_dice_second}] в пользу второго броска.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (0,)


async def bowling_second_win(data: dict):
    msg_dice_first = 6 - config.bowling_values.get(
        (await dp.bot.send_dice(config.CHANNEL_ID, emoji="🎳")).dice.value
    )
    msg_dice_second = 6 - config.bowling_values.get(
        (await dp.bot.send_dice(config.CHANNEL_ID, emoji="🎳")).dice.value
    )

    await asyncio.sleep(2)

    if msg_dice_first < msg_dice_second:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.7, 2)),
            f"Сессия закрыта [{msg_dice_first}:{msg_dice_second}] в пользу второго броска.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 1.7, 2)), msg,)
    elif msg_dice_first == msg_dice_second:
        msg = await utils.lose_notify(
            f"Сессия закрыта [{msg_dice_first}:{msg_dice_second}], ничья",
            "https://i.imgur.com/IfazgLa.png"
        )

        return (data["bid"] / 2, msg,)
    else:
        msg = await utils.lose_notify(
            f"Сессия закрыта [{msg_dice_first}:{msg_dice_second}] в пользу первого броска.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (0,)


async def bowling_number(data: dict):
    msg_dice = 6 - config.bowling_values.get(
        (await dp.bot.send_dice(config.CHANNEL_ID, emoji="🎳")).dice.value
    )

    await asyncio.sleep(2)

    if msg_dice == int(data["comment"].split()[-1]):
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.7, 2)),
            f"Выпало значение - {msg_dice}.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 1.7, 2)), msg,)
    else:
        msg = await utils.lose_notify(
            f"Выпало значение - {msg_dice}.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (0,)


async def darts_by(data: dict):
    msg_dice = (await dp.bot.send_dice(config.CHANNEL_ID, emoji="🎯")).dice.value

    await asyncio.sleep(2)

    if msg_dice == 1:
        msg = await utils.win_notify(
            float(round(data['bid'] * 2.5, 2)),
            f"Дротик не попал в мишень.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 2.5, 2)), msg,)
    else:
        msg = await utils.lose_notify(
            f"Дротик попал в мишень.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (0,)


async def darts_center(data: dict):
    msg_dice = (await dp.bot.send_dice(config.CHANNEL_ID, emoji="🎯")).dice.value

    await asyncio.sleep(2)

    if msg_dice == 6:
        msg = await utils.win_notify(
            float(round(data['bid'] * 2.5, 2)),
            f"Дротик попал в центр.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 2.5, 2)), msg,)
    else:
        msg = await utils.lose_notify(
            f"Дротик не попал в центр.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (0,)


async def darts_red(data: dict):
    msg_dice = (await dp.bot.send_dice(config.CHANNEL_ID, emoji="🎯")).dice.value

    await asyncio.sleep(2)

    if not (msg_dice % 2):
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.8, 2)),
            f"Дротик попал в красное.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 1.8, 2)), msg,)
    else:
        msg = await utils.lose_notify(
            f"Дротик не попал в красное.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (0,)


async def darts_bellow(data: dict):
    msg_dice = (await dp.bot.send_dice(config.CHANNEL_ID, emoji="🎯")).dice.value

    await asyncio.sleep(2)

    if msg_dice != 1 and msg_dice % 2:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.8, 2)),
            f"Дротик попал в белое.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 1.8, 2)), msg,)
    else:
        msg = await utils.lose_notify(
            f"Дротик не попал в белое.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (0,)


async def paper(data: dict):
    msg_dice = random.choice(list(config.knb_values))

    await dp.bot.send_message(
        config.CHANNEL_ID,
        config.knb_values.get(data['comment'])
    )
    await dp.bot.send_message(
        config.CHANNEL_ID,
        config.knb_values.get(msg_dice)
    )

    if msg_dice == "ножницы":
        msg = await utils.lose_notify(
            f"Выпали ножницы.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (0,)
    elif msg_dice == "камень":
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.7, 2)),
            f"Выпал камень.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 1.7, 2)), msg,)
    else:
        msg = await utils.lose_notify(
            f"Выпала бумага.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (data["bid"] / 2, msg,)


async def stone(data: dict):
    msg_dice = random.choice(list(config.knb_values))
    
    await dp.bot.send_message(
        config.CHANNEL_ID,
        config.knb_values.get(data['comment'])
    )
    await dp.bot.send_message(
        config.CHANNEL_ID,
        config.knb_values.get(msg_dice)
    )

    if msg_dice == "ножницы":
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.7, 2)),
            "Выпали ножницы.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (float(round(data['bid'] * 1.7, 2)), msg,)
    elif msg_dice == "бумага":
        msg = await utils.lose_notify(
            f"Выпала бумага.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (0,)
    else:
        msg = await utils.lose_notify(
            f"Выпал камень.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (data["bid"] / 2, msg,)


async def scissors(data: dict):
    msg_dice = random.choice(list(config.knb_values))

    await dp.bot.send_message(
        config.CHANNEL_ID,
        config.knb_values.get(data['comment'])
    )
    await dp.bot.send_message(
        config.CHANNEL_ID,
        config.knb_values.get(msg_dice)
    )

    if msg_dice == "бумага":
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.7, 2)),
            "Выпала бумага.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (float(round(data['bid'] * 1.7, 2)), msg,)
    elif msg_dice == "камень":
        msg = await utils.lose_notify(
            f"Выпал камень.",
            "https://i.imgur.com/24ZxGdy.png"
        )
        return (0,)
    else:
        msg = await utils.lose_notify(
            f"Выпали ножницы.",
            "https://i.imgur.com/X1XxxEF.png"
        )

        return (data["bid"] / 2, msg,)


async def football_goal(data: dict):
    msg_dice = await dp.bot.send_dice(
        config.CHANNEL_ID,
        emoji='⚽️'
    )

    await asyncio.sleep(2)

    if msg_dice.dice.value >= 3:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.3, 2)),
            f"Мяч попал в ворота.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 1.3, 2)), msg,)
    else:
        await utils.lose_notify(
            f"Мяч не попал в ворота.",
            "https://i.imgur.com/VoCoxdx.png"
        )
        return (0,)


async def football_by(data: dict):
    msg_dice = await dp.bot.send_dice(
        config.CHANNEL_ID,
        emoji='⚽️'
    )

    await asyncio.sleep(2)

    if msg_dice.dice.value >= 3:
        await utils.lose_notify(
            f"Мяч попал в ворота.",
            "https://i.imgur.com/VoCoxdx.png"
        )
        return (0,)
    else:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.8, 2)),
            f"Мяч не попал в ворота.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 1.8, 2)), msg,)


async def basketball_goal(data: dict):
    msg_dice = await dp.bot.send_dice(
        config.CHANNEL_ID,
        emoji='🏀'
    )

    await asyncio.sleep(2)

    if msg_dice.dice.value >= 4:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.3, 2)),
            f"Мяч попал в корзину.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 1.3, 2)), msg,)
    else:
        await utils.lose_notify(
            f"Мяч не попал в корзину.",
            "https://i.imgur.com/VoCoxdx.png"
        )
        return (0,)
    

async def basketball_by(data: dict):
    msg_dice = await dp.bot.send_dice(
        config.CHANNEL_ID,
        emoji='🏀'
    )

    await asyncio.sleep(2)

    if msg_dice.dice.value >= 4:
        await utils.lose_notify(
            f"Мяч попал в корзину.",
            "https://i.imgur.com/24ZxGdy.png"
        )
        return (0,)
    else:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.8, 2)),
            f"Мяч не попал в корзину.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 1.8, 2)), msg,)
    

async def pvp_cube(data: dict):
    msg_dice_user = await dp.bot.send_dice(
        config.CHANNEL_ID
    )
    msg_dice_bot = await dp.bot.send_dice(
        config.CHANNEL_ID
    )

    await asyncio.sleep(2)

    if msg_dice_user.dice.value < msg_dice_bot.dice.value:
        await utils.lose_notify(
            "",
            "https://i.imgur.com/24ZxGdy.png"
        )
        return (0,)
    elif msg_dice_user.dice.value > msg_dice_bot.dice.value:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.9, 2)),
            "",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 1.9, 2)), msg,)
    else:
        msg = await utils.lose_notify(
            "",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] / 2, 2)), msg,)
    

async def plinko(data: dict):
    msg_dice = await dp.bot.send_dice(
        config.CHANNEL_ID
    )

    await asyncio.sleep(2)

    if msg_dice.dice.value == 1:
        await utils.lose_notify(
            f"Выпало значение {msg_dice.dice.value}.",
            "https://i.imgur.com/24ZxGdy.png"
        )
        return (0,)
    
    reward = {
        2: 0.3,
        3: 0.9,
        4: 1.1,
        5: 1.3,
        6: 1.9
    }

    msg = await utils.win_notify(
        float(round(data['bid'] * reward[msg_dice.dice.value], 2)),
        f"Выпало значение {msg_dice.dice.value}.",
        "https://i.imgur.com/24ZxGdy.png"
    )

    return (float(round(data['bid'] * reward[msg_dice.dice.value], 2)), msg,)


async def cube_two_more(data: dict):
    msg_dice_first = await dp.bot.send_dice(
        config.CHANNEL_ID
    )
    msg_dice_second = await dp.bot.send_dice(
        config.CHANNEL_ID
    )

    await asyncio.sleep(2)

    if msg_dice_first.dice.value > 3 and msg_dice_second.dice.value > 3:
        msg = await utils.win_notify(
            float(round(data['bid'] * 2.8, 2)),
            "Оба кубика больше",
            "https://i.imgur.com/24ZxGdy.png"
        )
        return (float(round(data['bid'] * 2.8, 2)), msg,)

    await utils.lose_notify(
        "Один из кубиков не был больше",
        "https://i.imgur.com/24ZxGdy.png"
    )

    return (0,)


async def cube_two_less(data: dict):
    msg_dice_first = await dp.bot.send_dice(
        config.CHANNEL_ID
    )
    msg_dice_second = await dp.bot.send_dice(
        config.CHANNEL_ID
    )

    await asyncio.sleep(2)

    if msg_dice_first.dice.value < 4 and msg_dice_second.dice.value < 4:
        msg = await utils.win_notify(
            float(round(data['bid'] * 2.8, 2)),
            "Оба кубика меньше",
            "https://i.imgur.com/24ZxGdy.png"
        )
        return (float(round(data['bid'] * 2.8, 2)), msg,)

    await utils.lose_notify(
        "Один из кубиков не был меньше",
        "https://i.imgur.com/24ZxGdy.png"
    )

    return (0,)


async def roulette_red(data: dict):
    number = random.randint(0, 14)
    
    await dp.bot.send_video(
        config.CHANNEL_ID,
        config.roulette_link.get(number)
    )

    await asyncio.sleep(2)

    if not number:
        await utils.lose_notify(
            "Выпал зеленый.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (0,)
    if 1 <= number <= 7:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.8, 2)),
            "Выпал красный.",
            "https://i.imgur.com/24ZxGdy.png"
        )
        return (float(round(data['bid'] * 1.8, 2)), msg,)
    else:
        await utils.lose_notify(
            "Выпал черный.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (0,)
    

async def roulette_black(data: dict):
    number = random.randint(0, 14)

    await dp.bot.send_video(
        config.CHANNEL_ID,
        config.roulette_link.get(number)
    )

    await asyncio.sleep(2)

    if not number:
        await utils.lose_notify(
            "Выпал зеленый.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (0,)
    if 8 <= number <= 14:
        msg = await utils.win_notify(
            float(round(data['bid'] * 1.8, 2)),
            "Выпал черный.",
            "https://i.imgur.com/24ZxGdy.png"
        )
        return (float(round(data['bid'] * 1.8, 2)), msg,)
    else:
        await utils.lose_notify(
            "Выпал красный.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (0,)
    

async def roulette_green(data: dict):
    number = random.randint(0, 14)

    await dp.bot.send_video(
        config.CHANNEL_ID,
        config.roulette_link.get(number)
    )

    await asyncio.sleep(2)

    if not number:
        msg = await utils.win_notify(
            float(round(data['bid'] * 14, 2)),
            "Выпал зеленый.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 14, 2)), msg,)
    if 8 <= number <= 14:
        msg = await utils.lose_notify(
            "Выпал черный.",
            "https://i.imgur.com/24ZxGdy.png"
        )
        return (0,)
    else:
        await utils.lose_notify(
            "Выпал красный.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (0,)
    

async def roulette_number(data: dict):
    number = random.randint(0, 14)

    await dp.bot.send_video(
        config.CHANNEL_ID,
        config.roulette_link.get(number)
    )

    await asyncio.sleep(2)

    if int(data['comment'].split()[-1]) == number:
        msg = await utils.win_notify(
            float(round(data['bid'] * 14, 2)),
            f"Выпало число {number}.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (float(round(data['bid'] * 14, 2)), msg,)
    else:
        await utils.lose_notify(
            f"Выпало число {number}.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return (0,)
    

