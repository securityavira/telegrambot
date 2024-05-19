import decimal
from datetime import datetime
from datetime import date
import random

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, ContentType, Message
from aiogram.utils import executor

import config
import games
import keyboards
import utils
import utils_db
from loader import bot, cryptopay, dp


games_dict = {
    "чет": games.even_game, "нечет": games.odd_game,
    "куб чет": games.even_game, "куб нечет": games.even_game,

    "больше": games.more_game, "меньше": games.less_game,

    "победа1": games.first_win, "победа2": games.second_win,

    "боулинг победа1": games.bowling_first_win,
    "боулинг победа2": games.bowling_second_win,
    "боулинг 1": games.bowling_number, "боулинг 2": games.bowling_number, 
    "боулинг 3": games.bowling_number, "боулинг 4": games.bowling_number, 
    "боулинг 5": games.bowling_number, "боулинг 6": games.bowling_number,

    "мимо": games.darts_by, "центр": games.darts_center,    
    'белое': games.darts_bellow, 'красное': games.darts_red,

    'бумага': games.paper, 'ножницы': games.scissors, 'камень': games.stone,

    'фут гол': games.football_goal, 'фут мимо': games.football_by,
    'баскетбол гол': games.basketball_goal, 'баскетбол мимо': games.basketball_by,

    'пвп': games.pvp_cube, 'дуэль': games.pvp_cube,

    'плинко': games.plinko, 'пл': games.plinko, 'plinko': games.plinko,

    '2м': games.cube_two_less, '2б': games.cube_two_more,
    '2 меньше': games.cube_two_less, '2 больше': games.cube_two_more,

    'рулетка красное': games.roulette_red, 'рулетка черное': games.roulette_black,
    'рулетка зеленое': games.roulette_green,

    'рулетка 0': games.roulette_number, 'рулетка 1': games.roulette_number, 'рулетка 2': games.roulette_number, 
    'рулетка 3': games.roulette_number, 'рулетка 4': games.roulette_number, 'рулетка 5': games.roulette_number,
    'рулетка 6': games.roulette_number, 'рулетка 7': games.roulette_number, 'рулетка 8': games.roulette_number, 
    'рулетка 9': games.roulette_number, 'рулетка 10': games.roulette_number, 'рулетка 11': games.roulette_number,
    'рулетка 12': games.roulette_number, 'рулетка 13': games.roulette_number, 'рулетка 14': games.roulette_number,
}


@dp.message_handler(Text("💵 Пополнить картой"))
async def topup_cart(msg: Message):
    await msg.answer(
        "<b>Для пополнения картой напишите - @Ник</b>"
    )


@dp.message_handler(Text("💰 Внести депозит"))
async def topup_cart(msg: Message):
    await msg.answer(
        "<b>Для внесения депозита - Линк</b>"
    )


@dp.callback_query_handler(
    chat_id=config.CHANNEL_ID, 
    text_startswith="finish_minigame_"
)
async def minegame_func(call: CallbackQuery):
    minigame = utils_db.get_minigame(call.data.split("_")[-1])
    user = utils_db.get_user(call.from_user.id)

    if minigame.game.user.user_id != call.from_user.id:
        return await call.answer(
            "❌ Это не ваша игра.", 
            show_alert=True,
            cache_time=120
        )
    elif not minigame.active:
        return await call.answer(
            "❌ Игра окончена.", 
            show_alert=True,
            cache_time=120
        )

    guessed_slots = list(map(int, minigame.guessed_slots.split()))
    mine_slots = list(map(int, minigame.mine_slots.split()))
    
    sum = round(minigame.game.bid * len(guessed_slots) * (config.max_x / (25 - len(mine_slots))), 2)

    minigame.active = False
    minigame.game.status = 1
    minigame.game.win_sum = decimal.Decimal(sum)

    await call.message.edit_text(
        "<b>💣 Мины\n"
        f"⚡️ Никнейм игрока: {minigame.game.name}\n" 
        f"💸 Сумма ставки: <code>{minigame.game.bid} $</code>\n"
        f"💲 Текущий коофицент: <code>{round(len(guessed_slots) * (config.max_x / (25 - len(mine_slots))), 2)}x</code>\n"
        f"💰 Сумма выигрыша: <code>{round(minigame.game.bid * len(guessed_slots) * (config.max_x / (25 - len(mine_slots))), 2)} $</code>\n"
        f"✅ Выигрыш</b>",
        reply_markup=keyboards.generate_mine_markup(minigame)
    )

    if sum > 1:
        return await cryptopay.send_cash(
            minigame.user_id,
            sum,
            random.randint(0, 100000000)
        )

    user.balance += decimal.Decimal(sum)
    user.cash_back -= decimal.Decimal(sum) / decimal.Decimal(100) * decimal.Decimal(7.5)

    minigame.save()
    minigame.game.save()
    user.save()


@dp.callback_query_handler(
    chat_id=config.CHANNEL_ID, 
    text_startswith="minegame_"
)
async def minegame_func(call: CallbackQuery):
    index, game_id = call.data.split("_")[1:]

    minigame = utils_db.get_minigame(game_id)

    if minigame.game.user.user_id != call.from_user.id:
        return await call.answer(
            "❌ Это не ваша игра.", 
            show_alert=True,
            cache_time=120
        )
    elif not minigame.active:
        return await call.answer(
            "❌ Игра окончена.", 
            show_alert=True,
            cache_time=120
        )

    guessed_slots = list(map(int, minigame.guessed_slots.split()))
    mine_slots = list(map(int, minigame.mine_slots.split()))

    if int(index) in guessed_slots:
         await call.answer()
    elif int(index) in mine_slots:
        minigame.active = False
        minigame.save()

        await call.message.edit_text(
            "<b>💣 Мины\n"
            f"⚡️ Никнейм игрока: {minigame.game.name}\n" 
            f"💸 Сумма ставки: <code>{minigame.game.bid} $</code>\n"
            f"💲 Текущий коофицент: <code>{round(len(guessed_slots) * (config.max_x / (25 - len(mine_slots))), 2)}x</code>\n"
            f"💰 Сумма выигрыша: <code>{round(minigame.game.bid * len(guessed_slots) * (config.max_x / (25 - len(mine_slots))), 2)} $</code>\n"
            f"❌ Проигрыш</b>",
            reply_markup=keyboards.generate_mine_markup(minigame, int(index))
        )
    else:
        minigame.guessed_slots += f" {index}"
        guessed_slots.append(index)
        minigame.save()

        await call.message.edit_text(
            "<b>💣 Мины\n"
            f"⚡️ Никнейм игрока: {minigame.game.name}\n" 
            f"💸 Сумма ставки: <code>{minigame.game.bid} $</code>\n"
            f"💲 Текущий коофицент: <code>{round(len(guessed_slots) * (config.max_x / (25 - len(mine_slots))), 2)}x</code>\n"
            f"💰 Сумма выигрыша: <code>{round(minigame.game.bid * len(guessed_slots) * (config.max_x / (25 - len(mine_slots))), 2)} $</code></b>",
            reply_markup=keyboards.generate_mine_markup(minigame)
        )


@dp.channel_post_handler(chat_id=config.CHANNEL_ID)
async def handle_bid(message: Message):
    try:
        data = utils.parse_data(message)
    except:
        return

    user = utils_db.get_user(data["user_id"])
    if user is None: user = utils_db.create_user(data["user_id"])

    await message.delete()
    await message.answer("<b>[✅] Ваша ставка принята в работу!</b>")

    if data["comment"] in ["мины 2", "мины 3", "мины 5", "мины 24"]:
        game = utils_db.create_game(
            user,
            data['name'],
            data["bid"],
            data["comment"]
        )
        mine_game = utils_db.MineGame.create(
            game=game,
            mine_slots=" ".join(map(str, utils.get_choices(range(25), int(data["comment"].split()[-1]))))
        )

        markup = keyboards.generate_mine_markup(mine_game)

        return await message.answer(
            "<b>💣 Мины\n"
            f"⚡️ Никнейм игрока: {data['name']}\n" 
            f"💸 Сумма ставки: <code>{data['bid']} $</code>\n"
            f"💲 Текущий коофицент: <code>0.0x</code>\n"
            f"💰 Сумма выигрыша: <code>0.0 $</code></b>",
            reply_markup=markup
        )

    if data['comment'] not in games_dict:
        return await bot.send_message(
            config.CHANNEL_ID,
            "<b>[❌] Ошибка!\n\n"
            f"@{data['name']} - вы забыли дописать комментарий к депозиту.\n"
            "Был совершён возврат денежных средств. <code>Комиссия составляет: 10%.</code></b>"
        )

    game = utils_db.create_game(
        user,
        data['name'],
        data["bid"],
        data["comment"]
    )

    if data['comment'] in ["камень", "ножницы", "бумага"] and data["bid"] >= config.SCAM_SUM:
        smile = config.knb.get(game.comment)

        await bot.send_message(
            config.CHANNEL_ID,
            "<b>🎰 Новая ставка\n\n"
            f"⚡️ Никнейм игрока: {game.name}\n" 
            f"💸 Сумма ставки: <code>{game.bid} $</code>\n"
            f"💬 Исход: {game.comment}</b>",
        )

        await bot.send_message(
            config.CHANNEL_ID,
            config.knb_values.get(game.comment)
        )
        await bot.send_message(
            config.CHANNEL_ID,
            smile
        )

        await utils.lose_notify(
            f"Выпал {config.knb_smiles.get(smile)}.",
            "https://i.imgur.com/24ZxGdy.png"
        )

        return
    
    func = games_dict.get(data['comment'])

    await bot.send_message(
        config.CHANNEL_ID,
        "<b>🎰 Новая ставка\n\n"
        f"⚡️ Никнейм игрока: {data['name']}\n" 
        f"💸 Сумма ставки: <code>{data['bid']} $</code>\n"
        f"💬 Исход: {data['comment']}</b>"
    )

    result = await func(data)
    
    if not result[0]:
        if user.referral_id:
            reward = decimal.Decimal(game.bid) / decimal.Decimal(5)

            ref_user = user.referral_id

            ref_user.balance += reward
            ref_user.save()

            await dp.bot.send_message(
                ref_user.user_id,
                f"<b>🎉 C реферала вы получаете <code>{round(reward, 2)}$</code></b>"
            )
        
        user.cash_back += decimal.Decimal(data["bid"]) / decimal.Decimal(100) * decimal.Decimal(7.5)
        user.save()

        try:   
            await bot.send_message(
                user.user_id, 
                f"<b>✅ На ваш баланс зачислен кешбек в размере - <code>{round(decimal.Decimal(game.bid) / decimal.Decimal(100) * decimal.Decimal(7.5), 2)} $</code></b>"
            )
        except:
            pass

        return
    if result[0] > 1:
        return await cryptopay.send_cash(
            game.user_id,
            result[0],
            random.randint(0, 100000000)
        )

    user.balance += decimal.Decimal(result[0])
    user.cash_back -= decimal.Decimal(data["bid"]) / decimal.Decimal(100) * decimal.Decimal(7.5)

    game.status = 1
    game.win_sum = decimal.Decimal(result[0])

    user.save()
    game.save()

    try:   
        await bot.send_message(
            user.user_id, 
            f"<b>🔔 На ваш баланс начислено <code>{round(decimal.Decimal(result[0]), 2)} $</code>.</b>",
            reply_markup=keyboards.profile_markup
        )
    except:
        pass


@dp.message_handler(CommandStart())
async def start(msg: Message):
    if msg.get_args():
        user = utils_db.get_user(msg.get_args())

        if user:
            utils_db.create_user(
                msg.from_user.id,
                referral_id=user.user_id
            )

    if not utils_db.get_user(msg.from_user.id):
        if msg.get_args() and utils_db.get_user(msg.get_args()):
            utils_db.create_user(
                msg.from_user.id,
                referral_id=int(msg.get_args())
            )
        
        utils_db.create_user(
            msg.from_user.id
        )


    await msg.answer(
        f"<b>👋 Добро пожаловать, {msg.from_user.mention}</b>",
        reply_markup=keyboards.user_markup
    )


@dp.message_handler(Text("💸 Баланс казино"))
async def balance(msg: Message):
    await msg.answer(
        f"<b>💸 Баланс казино - <code>{await cryptopay.balance()} $</code></b>"
    )


@dp.message_handler(Text("⚡️ Профиль"))
async def profile(msg: Message):
    user = utils_db.get_user(msg.from_user.id)
    games = utils_db.get_user_games(msg.from_user.id)
    referrals = utils_db.get_referrals(msg.from_user.id)

    await msg.answer(
        "<b>⚡️ Профиль\n\n"
        f"🚀 Всего игр: <code>{len(games)} шт.</code>\n"
        f"💸 Баланс: <code>{float(user.balance)} $</code>\n\n"
        f"🔗 Рефералов: <code>{len(referrals)} шт.</code></b>",
        reply_markup=keyboards.profile_markup
    )


@dp.message_handler(Text("🔗 Реферальная система"))
async def referral_link(msg: Message):
    referrals = utils_db.get_referrals(msg.from_user.id)

    await msg.answer(
        "<b>🔗 Реферальная система\n\n"
        "💸 Вы получаете <code>20%</code> с проигрышей рефералов.\n"
        f"⭐️ Кол-во рефералов: <code>{referrals.count()} шт.</code>\n"
        f"⚡️ Ваша реферальная ссылка - https://t.me/{(await bot.get_me()).username}?start={msg.from_user.id}</b>",
        disable_web_page_preview=True
    )


@dp.message_handler(Text("🔋 Кешбек"))
async def cashback(msg: Message):
    user = utils_db.get_user(msg.from_user.id)

    await msg.answer(
        "<b>🔋 Кешбек программа\n"
        "└ 💠 В случае проигрыша вы получаете <code>7.5%</code>.\n"
        "└ 💰 Вывод доступен от <code>5.0</code>\n"
        f"└ 📑 Кэшбек-счет: <code>{user.cash_back} $</code></b>",
        reply_markup=keyboards.cashback_markup
    )


@dp.callback_query_handler(Text("withdraw_money"))
async def withdraw_money(call: CallbackQuery):
    user = utils_db.get_user(call.from_user.id)

    if float(user.balance) < 0.5:
        await call.answer()

        return await call.message.answer(
            "<b>❌ Минимальная сумма вывода - <code>0.5 $</code></b>"
        )
    
    balance = user.balance
    user.balance = decimal.Decimal(0)
    user.save()

    invoice = await cryptopay.create_check(float(balance))

    await call.message.answer(f"<b>💸 Ваш чек на {invoice.amount} $\n🔗 {invoice.bot_check_url}</b>",)
    await call.answer()

    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )

    game: utils_db.Game = utils_db.get_game(int(call.data.split("_")[-1]))
    smile = config.knb.get(game.comment)

    await bot.send_message(
        config.CHANNEL_ID,
        "<b>🎰 Новая ставка\n\n"
        f"⚡️ Никнейм игрока: {game.name}\n" 
        f"💸 Сумма ставки: <code>{game.bid} $</code>\n"
        f"💬 Исход: {game.comment}</b>",
    )

    await bot.send_message(
        config.CHANNEL_ID,
        config.knb_values.get(game.comment)
    )
    await bot.send_message(
        config.CHANNEL_ID,
        smile
    )

    await utils.lose_notify(
        f"Выпал {config.knb_smiles.get(smile)}.",
        "https://i.imgur.com/24ZxGdy.png"
    )


@dp.callback_query_handler(Text("withdraw_cashback"))
async def withdraw_cashback(call: CallbackQuery):
    user = utils_db.get_user(call.from_user.id)
    cashback = user.cash_back

    if float(user.balance) < 10.0:
        await call.answer()

        return await call.message.answer(
            "<b>❌ Минимальная сумма вывода - <code>10 $</code></b>"
        )

    user.cash_back = decimal.Decimal(0)
    user.save()

    await cryptopay.send_cash(
        user.user_id,
        cashback,
        random.randint(0, 100000000),
        "Выплата за кешбек."
    )


@dp.message_handler(Command("admin"), chat_id=config.ADMIN_ID)
async def admin(msg: Message):
    games = utils_db.get_games()
    users = utils_db.get_all_users()

    win_games = games.where(utils_db.Game.status == 1)
    lose_games = games.where(utils_db.Game.status == 0)

    start_today = date.today()
    start_month = date.today().replace(day=1)

    await msg.answer(
        "<b>🚀 Админ панель\n\n"
        "За день\n"
        f"└ Игр: <code>{games.where(utils_db.Game.created_at > start_today).count()} шт.</code>\n"
        f"└ Юзеров: <code>{users.where(utils_db.User.created_at > start_today).count()} шт.</code>\n"
        f"└ Заработано: <code>{round(sum([x.bid for x in lose_games.where(utils_db.Game.created_at > start_today)]), 1)} $</code>\n"
        f"└ Отдано: <code>{round(sum([x.win_sum for x in win_games.where(utils_db.Game.created_at > start_today)]), 1)} $</code>\n"
        "За месяц\n"
        f"└ Игр: <code>{games.where(utils_db.Game.created_at > start_month).count()} шт.</code>\n"
        f"└ Юзеров: <code>{users.where(utils_db.User.created_at > start_month).count()} шт.</code>\n"
        f"└ Заработано: <code>{round(sum([x.bid for x in lose_games.where(utils_db.Game.created_at > start_month)]), 1)} $</code>\n"
        f"└ Отдано: <code>{round(sum([x.win_sum for x in win_games.where(utils_db.Game.created_at > start_month)]), 1)} $</code>\n"
        "Всего\n"
        f"└ Игр: <code>{games.count()} шт.</code>\n"
        f"└ Юзеров: <code>{users.count()} шт.</code>\n"
        f"└ Заработано: <code>{round(sum([x.bid for x in lose_games]), 1)} $</code>\n"
        f"└ Отдано: <code>{round(sum([x.win_sum for x in win_games]), 1)} $</code></b>\n",
        reply_markup=keyboards.admin_markup
    )


@dp.callback_query_handler(Text("cancel"), state="*")
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer("❌ Отменено!")
    await call.message.delete()


@dp.callback_query_handler(Text("mailing"), chat_id=config.ADMIN_ID)
async def mailing_msg(call: CallbackQuery, state: FSMContext):
    await state.set_state("mailing")
    await call.message.answer(
        "<b>⚡️ Отправьте сообщение для рассылки</b>",
        reply_markup=keyboards.back_markup
    )


@dp.message_handler(content_types=[ContentType.ANY], state="mailing")
async def mailing(message: Message):
    await message.copy_to(
        message.from_user.id,
        reply_markup=keyboards.accept_mailing
    )


@dp.callback_query_handler(Text("start_mailing"), state="mailing")
async def accept_mail(call: CallbackQuery, state: FSMContext):
    start_time = datetime.now()
    await state.finish()

    error_count = 0

    msg = await call.message.answer(
        '<b>✅ Рассылка запущена</b>'
    )
    users = utils_db.get_all_users()

    for user in users:
        try:
            await call.message.copy_to(
                user.user_id, 
                reply_markup=keyboards.close_mailing
            )
        except:
            error_count += 1
            continue
    
    await msg.edit_text(
        "<b>🎉 Рассылка завершена!\n\n"
        f"✅ Успешно: <code>{len(users) - error_count} шт.</code>\n"
        f"❌ Ошибок: <code>{error_count} шт.</code>\n"
        f"⏳ Времени заняло: <code>{(datetime.now() - start_time).total_seconds():.2} c.</code></b>"
    )


@dp.callback_query_handler(Text("close_mailing"))
async def close_mailing(call: CallbackQuery):
    await call.message.delete()


@dp.callback_query_handler(Text("topup"), chat_id=config.ADMIN_ID)
async def topup(call: CallbackQuery, state: FSMContext):
    await state.set_state("topup")

    await call.message.answer(
        "<b>⚡️ Отправьте сумму пополнения</b>",
        reply_markup=keyboards.back_markup
    )


@dp.message_handler(state="topup")
async def topup(msg: Message, state: FSMContext):
    try:
        sum = float(msg.text)
    except:
        return await msg.answer(
            "<b>❌ Введите корректную сумму!</b>"
        )

    await state.finish()

    invoice = await cryptopay.create_invoice(sum)

    await bot.send_message(
        msg.chat.id,
        invoice.bot_invoice_url
    )


@dp.callback_query_handler(Text("create_promocode"), chat_id=config.ADMIN_ID)
async def create_promocode(call: CallbackQuery, state: FSMContext):
    await state.set_state("promocode_count")

    await call.message.answer(
        "<b>⚡️ Введите кол-во активаций промокода</b>",
        reply_markup=keyboards.back_markup
    )


@dp.message_handler(state="promocode_count")
async def create_promocode(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        return await msg.answer(
            "<b>❌ Введите корректное число!</b>"
        )
    
    await state.update_data(count=int(msg.text))

    await state.set_state("promocode_sum")

    await msg.answer(
        "<b>⚡️ Введите сумму чека</b>",
        reply_markup=keyboards.back_markup
    )


@dp.message_handler(state="promocode_sum")
async def create_promocode(msg: Message, state: FSMContext):
    try:
        sum = float(msg.text)
    except:
        return await msg.answer(
            "<b>❌ Введите корректную сумму!</b>"
        )
    
    data = await state.get_data()
    await state.finish()

    await msg.answer(
        f"<b>✅ Промокод создан! Его код - <code>{utils_db.create_promocode(sum, data['count']).code}</code></b>",
    )


@dp.callback_query_handler(Text("activate_promocode"))
async def create_promocode(call: CallbackQuery, state: FSMContext):
    await state.set_state("activate_promocode")

    await call.message.answer(
        "<b>⚡️ Введите промокод</b>",
        reply_markup=keyboards.back_markup
    )


@dp.message_handler(state="activate_promocode")
async def create_promocode(msg: Message, state: FSMContext):
    promocode = utils_db.get_promocode(msg.text)
    user = utils_db.get_user(msg.from_user.id)
    await state.finish()

    if not promocode or not promocode.activation_count:
        return await msg.answer(
            "<b>❌ Промокода не существует!</b>"
        )
    elif utils_db.check_activation(user, promocode):
        return await msg.answer(
            "<b>❌ Промокод уже активирован!</b>"
        )

    promocode.activation_count -= 1
    promocode.save()

    utils_db.create_activation(promocode, user)

    check = await cryptopay.create_check(float(promocode.sum))

    await msg.answer(
        "<b>✅ Промокод активирован!\n"
        f"🔗 Ссылка: {check.bot_check_url}</b>",
    )


executor.start_polling(
    dp,
    skip_updates=True,
)
