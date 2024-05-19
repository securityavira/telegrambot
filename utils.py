import re

import config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from loader import bot
import random


def get_choices(lst, n=3):
    unique_indices = set()
    result = []
    
    while len(result) < n:
        index = random.randint(0, len(lst) - 1)
        if index not in unique_indices:
            unique_indices.add(index)
            result.append(lst[index])

    return result

async def lose_notify(msg: str, photo: str):
    return await bot.send_photo(
        config.CHANNEL_ID,
        photo,
        f"<b>Проигрыш! {msg}\n\n"
        "<blockquote>"
        "К достойной цели нет коротких путей.\nПровал не повод останавливаться!"
        "</blockquote>\n\n"
        f'<a href="{config.RULES_LINK}">Правила</a> | '
        f'<a href="{config.SUPPORT_LINK}">Тех. поддержка</a></b>',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    "⚡️ Внести депозит",
                    config.INVOICE_LINK
                )],
                [InlineKeyboardButton(
                    "💳 Пополнить картой",
                    config.TOPUP_CARD_LINK
                )],
                [InlineKeyboardButton(
                    "✏️ Пользовательское соглашение",
                    config.TERMS_LINK
                )],
            ]
        )
    )


async def win_notify(sum: int, msg: str, photo: str):
    return await bot.send_photo(
        config.CHANNEL_ID,
        photo,
        f"<b>Победа! {msg}\n\n"
        "<blockquote>"
        f"На ваш баланс был зачислен выигрыш {sum} $.\n"
        "Опробуйте свою удачу сполна и познайте путь истинных победителей по жизни!"
        "</blockquote>\n\n"
        f'<a href="{config.RULES_LINK}">Правила</a> | '
        f'<a href="{config.SUPPORT_LINK}">Тех. поддержка</a></b>',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    "⚡️ Внести депозит",
                    config.INVOICE_LINK
                )],
                [InlineKeyboardButton(
                    "💳 Пополнить картой",
                    config.TOPUP_CARD_LINK
                )],
                [InlineKeyboardButton(
                    "✏️ Пользовательское соглашение",
                    config.TERMS_LINK
                )]
            ]
        )
    )


def parse_data(msg: Message) -> dict[str, int | str]:
    return {
        "user_id": msg.entities[0].user.id,
        "name": msg.entities[0].user.first_name,
        "bid": float(re.search(r'\(\$(.*?)\)', msg.text.split('\n')[0].split()[-1]).group(1)),
        "comment": ' '.join(msg.text.split('\n')[-1].split()[1::]).lower()
    }

