from sys_init import *
from models import *

from sqlalchemy.orm import sessionmaker


def init_db(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_session(engine):
    session_class = sessionmaker(bind=engine)
    session = session_class()
    return session


def test_add():
    p1 = Player(name='player1', nick='p1')
    p2 = Player(name='player2', nick='p2')
    p3 = Player(name='player3', nick='p3')
    p4 = Player(name='player4', nick='p4')
    p5 = Player(name='player5', nick='p5')

    session = get_session(DB_ENGINE)

    session.add(p1)
    test_query()

    session.commit()
    test_query()

    session.add(p2)
    session.add(p3)
    test_query()

    session.flush()
    test_query()

    session.add_all([p4, p5])
    test_query()

    session.commit()
    test_query()


def test_query():
    session = get_session(DB_ENGINE)
    res = session.query(Player).all()

    print(res)
    for item in res:
        print(item.name)


def test_del():
    session = get_session(DB_ENGINE)

    q = session.query(Player)
    q = q.filter(Player.id > 3)
    q.delete()

    test_query()
    session.commit()
    test_query()


def test_update():

    session = get_session(DB_ENGINE)

    q = session.query(Player)
    ps = q.filter(Player.id == 0).all()

    for p in ps:
        print(p.name)

    p = q.filter(Player.name == 'b').first()

    p.name = 'p2'

    session.commit()

    print(p.name)


if __name__ == '__main__':
    Base.metadata.create_all(bind=DB_ENGINE)
    session = get_session(DB_ENGINE)
    s0 = Season(name='s0', nick='s0', st_date=dt(2022, 3, 23), ed_date=dt(2022, 6, 1))
    s1 = Season(name='s1', nick='s1', st_date=dt(2022, 6, 1), ed_date=dt(2022, 10, 1))
    s2 = Season(name='s1', nick='s2', st_date=dt(2022, 10, 1), ed_date=dt(2023, 1, 1))

    session.add_all([s0, s1, s2])
    session.commit()

