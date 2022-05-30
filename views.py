import pandas as pd

from sys_init import *
from models import *
from db_op import *


def get_sum():
    session = get_session(DB_ENGINE)

    recs = session.query(Record, Player).join(Player, Record.player_id == Player.id)

    data = pd.read_sql(sql=recs.statement, con=recs.session.bind)

    pivot = data.pivot_table(index='name', aggfunc=sum)
    print(pivot['points'].sort_values(ascending=False))


if __name__ == '__main__':
    get_sum()
