from datetime import datetime
import decimal
import random
import uuid
from peewee import *


db = SqliteDatabase("database.sqlite")


class User(Model):
    user_id = IntegerField(
        null=False,
        unique=True
    )
    balance = DecimalField(
        default=0,
        decimal_places=2,
        auto_round=True,
        null=False
    )
    cash_back = DecimalField(
        default=0,
        decimal_places=2,
        auto_round=True,
        null=False
    )
    referral_id = ForeignKeyField(
        "self",
        user_id,
        default=None,
        null=True
    )
    created_at = DateTimeField(
        default=datetime.now
    )


    class Meta:
        db_column = "games"
        database = db


class Game(Model):
    id = AutoField()
    user = ForeignKeyField(
        User,
        User.user_id
    )
    name = CharField(
        max_length=255,
        null=False
    )
    bid = FloatField(
        null=False
    )
    win_sum = DecimalField(
        default=0.0,
        decimal_places=2,
        auto_round=True,
        null=False
    )
    comment = CharField(
        null=False
    )
    status = IntegerField(
        null=False,
        default=0,
        choices=(
            (0, "lose"),
            (1, "win")
        )
    )
    created_at = DateTimeField(
        default=datetime.now
    )

    class Meta:
        db_column = "games"
        database = db


class MineGame(Model):
    id = AutoField()
    game = ForeignKeyField(
        Game,
        Game.id
    )
    active = BooleanField(
        null=False,
        default=True
    )
    guessed_slots = CharField(
        null=False,
        default=''
    )
    mine_slots = CharField(
        null=False
    )

    
    class Meta:
        db_column = "mine_games"
        database = db


class Promocode(Model):
    id = AutoField()
    code = CharField(
        null=False,
        default=lambda: str(uuid.uuid4())[:7]
    )
    sum = FloatField(
        null=False
    )
    activation_count = IntegerField(
        null=False
    )

        
    class Meta:
        db_column = "promocodes"
        database = db


class PromocodeActivation(Model):
    id = AutoField()
    user = ForeignKeyField(
        User,
        User.user_id,
    )
    promocode = ForeignKeyField(
        Promocode,
        Promocode.id
    )

    class Meta:
        db_column = "promocode_activations"
        database = db


def create_game(
        user_id: User, 
        name: str, 
        bid: float, 
        comment: str
) -> Game:
    return Game.create(
        user=user_id,
        name=name,
        bid=bid,
        comment=comment
    )


def create_user(user_id: int, referral_id: int = None) -> User:
    user = User()
    
    user.user_id = user_id
    user.referral_id = referral_id
    
    user.save()

    return user


def get_user(user_id) -> User | None:
    return User.get_or_none(user_id=user_id)


def get_all_users() -> list[User]:
    return User.select()


def get_user_games(user_id: int) -> list[Game]:
    return Game.select().where(Game.user == user_id)


def get_game(game_id: int) -> Game | None:
    return Game.get_or_none(id=game_id)


def get_games() -> list[Game]:
    return Game.select()


def get_referrals(user_id: int) -> list[User]:
    return User.select().where(User.referral_id == user_id)


def get_minigame(id: int) -> MineGame | None:
    return MineGame.get_or_none(id=id)


def create_promocode(sum: float, count: int) -> Promocode:
    return Promocode.create(sum=sum, activation_count=count)


def create_activation(promocode: Promocode, user: int):
    PromocodeActivation.create(
        user=user,
        promocode=promocode
    )


def check_activation(user: int, promocode: Promocode) -> bool:
    return bool(PromocodeActivation.get_or_none(user=user, promocode=promocode))


def get_promocode(code: str) -> Promocode | None:
    return Promocode.get_or_none(
        code=code
    )


Game.create_table()
User.create_table()
MineGame.create_table()
Promocode.create_table()

db.create_tables([
    User, Game, MineGame,
    Promocode, PromocodeActivation
])