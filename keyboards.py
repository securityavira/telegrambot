from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from utils_db import MineGame
import config


user_markup = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("⚡️ Профиль"),
            KeyboardButton("🔋 Кешбек"),
        ],
        [
            KeyboardButton("🔗 Реферальная система"),
            KeyboardButton("💸 Баланс казино")
        ]
    ],
    resize_keyboard=True
)


profile_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("💸 Вывести деньги", callback_data="withdraw_money")],
        [InlineKeyboardButton("✏ Ввести промокод", callback_data="activate_promocode")],
    ]
)


cashback_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("💸 Вывести кешбек", callback_data="withdraw_cashback")]
    ]
)


admin_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                "⚡️ Рассылка",
                callback_data="mailing"
            )
        ],
        [
            InlineKeyboardButton(
                "💸 Пополнить",
                callback_data="topup"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 Создать промокод",
                callback_data="create_promocode"
            )
        ],
    ]
)


back_markup = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(
        "◀️ Отмена",
        callback_data="cancel"
    )]]
)


accept_mailing = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(
            "✅ Начать",
            callback_data="start_mailing"
        ),
        InlineKeyboardButton(
            "◀️ Отмена",
            callback_data="cancel"
        )
    ]]
)


close_mailing = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(
        "💢 Понятно",
        callback_data="close_mailing"
    )]]
)


def generate_mine_markup(game: MineGame, last_index: int | None = None):
    markup = InlineKeyboardMarkup(5)

    guessed_slots = list(map(int, game.guessed_slots.split()))
    mine_slots = list(map(int, game.mine_slots.split()))

    result_buttons = []

    for x in range(5):
        for y in range(5):
            current_index = x * 5 + y

            if not game.active and last_index is not None and current_index == last_index:
                result_buttons.append(InlineKeyboardButton(
                    "💥",
                    callback_data=f"minegame_{current_index}_{game.id}"
                ))
                continue

            if game.active:
                text = ("📦", "✅")[current_index in guessed_slots]
            else:
                text = ("✅" if current_index in guessed_slots else "📦", "💣")[current_index in mine_slots]

            result_buttons.append(InlineKeyboardButton(
                text,
                callback_data=f"minegame_{current_index}_{game.id}"
            ))

    markup.add(*result_buttons)

    if game.active:
        markup.add(InlineKeyboardButton(
            f"{round(len(guessed_slots) * (config.max_x / (25 - len(mine_slots))), 2)} ▶️ {round(len(guessed_slots) * (config.max_x / (25 - len(mine_slots))) + config.max_x / (25 - len(mine_slots)), 2)}",
            callback_data="inactive"
        ))
        markup.add(InlineKeyboardButton(
            "✅ Забрать выигрыш",
            callback_data=f"finish_minigame_{game.id}"
        ))
    else:
        markup.add(InlineKeyboardButton(
            "🔁 Попробовать снова",
            config.INVOICE_LINK
        ))

    return markup