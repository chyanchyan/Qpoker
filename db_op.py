from sys_init import *
from tables import *

from sqlalchemy.orm import sessionmaker


def ini_db(engine):
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
    test_update()