import pandas as pd

from sys_init import *
from models import *
from db_op import *
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta


def get_sum(st_date=None, label='累计'):

    session = get_session(DB_ENGINE)

    if not st_date:
        recs = session.query(Record, Player, CashGame) \
            .join(Player, Record.player_id == Player.id) \
            .join(CashGame, Record.game_id == CashGame.id) \
            .order_by(CashGame.st_date.desc())
    else:
        recs = session.query(Record, Player, CashGame)\
            .join(Player, Record.player_id == Player.id)\
            .join(CashGame, Record.game_id == CashGame.id)\
            .order_by(CashGame.st_date.desc())\
            .filter(CashGame.st_date >= st_date)

    data = pd.read_sql(sql=recs.statement, con=recs.session.bind)

    pivot = data.pivot_table(index='name', aggfunc=sum)['points'].sort_values(ascending=False)
    pivot = pd.DataFrame(pivot)
    print(pivot)
    return pivot


def get_record_set():
    acc_sum = get_sum(label='累计积分')
    weekly_sum = get_sum(get_last_monday(), label='周度积分')
    acc_sum.to_excel(r'C:\Users\Q\Desktop\结仇好工具_累计_%s.xlsx' % dt.today().strftime('%Y%m%d'))
    weekly_sum.to_excel(r'C:\Users\Q\Desktop\结仇好工具_周度_%s.xlsx' % dt.today().strftime('%Y%m%d'))


def get_last_monday(current_date: dt = dt.today() - relativedelta(days=1)):
    res = current_date - relativedelta(days=current_date.weekday())
    res = dt(res.year, res.month, res.day)
    return res


def get_records(st_date: dt, ed_date: dt = dt.today()):
    session = get_session(DB_ENGINE)

    recs = session.query(Record, Player, CashGame) \
        .join(Player, Record.player_id == Player.id) \
        .join(CashGame, Record.game_id == CashGame.id) \
        .order_by(CashGame.st_date.desc()) \
        .filter(st_date <= CashGame.st_date)

    data = pd.read_sql(sql=recs.statement, con=recs.session.bind)
    data = data[['game_id', 'st_date', 'name', 'points']]
    cols = set(data['name'])
    index = set(data['game_id'])
    res = pd.DataFrame(columns=cols, index=index)

    for i, r in res.iterrows():
        for c in cols:
            try:
                data_game = data[data['game_id'] == i]
                value = data_game[data_game['name'] == c]['points'].values[0]
                print(value)
                res.loc[i, c] = value
            except IndexError:
                pass

    res.to_excel('res.xlsx')


if __name__ == '__main__':
    get_records(st_date=dt(2022, 5, 27))
