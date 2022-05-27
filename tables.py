from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime as dt


Base = declarative_base()


class Named:
    def __init__(self, *args, **kwargs):
        pass

    name = Column(String(100))
    nick = Column(String(100))


class Id:
    def __init__(self, *args, **kwargs):
        pass

    id = Column(Integer, primary_key=True, autoincrement=True)


class TimeRange:
    def __init__(self, *args, **kwargs):
        pass

    st_date = Column(DateTime)
    ed_date = Column(DateTime)


class Player(Base, Id, Named):
    __tablename__ = 'player'

    game_userid = Column(String(50))


class Game(Base, Id, TimeRange):
    __tablename__ = 'game'

    sb = Column(Integer, default=1)
    bb = Column(Integer, default=2)
    ante = Column(Integer, default=0)
    max_player = Column(Integer, default=9)


class Record(Base, Id):
    __tablename__ = 'record'

    game_id = Column(Integer, ForeignKey('game.id'), nullable=False)
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    points = Column(Integer, nullable=False)
    hands_count = Column(Integer)


def _test():
    p = Player(name='a', nick='aa')
    g = Game(st_date=dt(2022, 5, 20, 21, 0, 0), ed_date=dt(2022, 5, 21, 0, 10, 0))
    print(p.id)
    print(g.st_date)


if __name__ == '__main__':
    _test()
