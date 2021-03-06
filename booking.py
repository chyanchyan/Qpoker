import pandas as pd

from sys_init import *
from models import *
from db_op import get_session


def migrate():

    nicks = {
        '杨涛': 'yt',
        '张par': 'zp',
        '雨飞': 'yf',
        '千千': 'qq',
        '雷博士': 'lbs',
        '星爷': 'xy',
        '许哥': 'xg',
        '李法官': 'lfg',
        '猫猫侠朴par': 'pp',
        '博哥': 'bg',
        '躲躲猫': 'll',
        '二哥': 'eg',
        '冯老板': 'flb',
        '万利': 'wl',
        '嘉诚': 'jc',
        '林哥': 'lg',
    }

    data_path = 'poker_data.xlsx'
    data = pd.read_excel(data_path, index_col='date')

    names = data.columns

    session = get_session(DB_ENGINE)

    for i, name in enumerate(names):
        p = Player(name=name, nick=nicks[name])
        session.add(p)

    g_id = 1
    for index, game in data.iterrows():
        g = CashGame(id=g_id)
        session.add(g)
        g_id += 1

    g_id = 1
    for index, game in data.iterrows():
        for p_id, rec in enumerate(game.values):
            if pd.isna(rec):
                pass
            else:
                r = Record(game_id=g_id, player_id=p_id + 1, points=rec)
                session.add(r)

        g_id += 1

    session.commit()


def update_game_id():
    nicks = {
        '杨涛': '杨涛',
        '张par': 'ZZL',
        '雨飞': '雨飞',
        '千千': '千千',
        '雷博士': '雨寿',
        '星爷': '味曲奇',
        '许哥': '干朴哥',
        '李法官': '神话科比扣篮',
        '猫猫侠朴par': '猫猫侠',
        '博哥': 'burger',
        '躲躲猫': '躲躲猫',
        '二哥': '许哥',
        '冯老板': '27全压',
        '万利': '万利',
        '嘉诚': 'SEVEN',
        '林哥': '',
    }


def booking_records(recs, date=dt.today()):
    session = get_session(DB_ENGINE)
    players = session.query(Player).all()

    p_nick_map_ids = dict(zip([p.nick for p in players], [p.id for p in players]))

    g = CashGame(st_date=date)
    session.add(g)
    session.commit()

    recs = dict(zip(recs[::2], recs[1::2]))

    if sum(recs.values()) == 0:
        for nick, rec in recs.items():
            p_id = p_nick_map_ids[nick]
            r = Record(game_id=g.id, player_id=p_id, points=rec)
            session.add(r)

        session.commit()
    else:
        print('sum of points not == 0')


def check():
    session = get_session(DB_ENGINE)
    last_game = session.query(CashGame).order_by(CashGame.id.desc()).first()
    recs = session.query(Record).filter(Record.game_id == last_game.id)

    print([(rec.player_id, rec.points) for rec in recs])


def booking():

    recs = ['bg', 3521,
            'zp', 546,
            'qq', 350,
            'flb', 280,
            'll', 123,
            'lfg', 13,
            'xg', 11,
            'xy', -127,
            'pp', -4717,
            ]

    booking_records(recs, date=dt(2022, 6, 5, 23, 0, 0))


if __name__ == '__main__':
    booking()
