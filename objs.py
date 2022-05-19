from datetime import datetime as dt
from settings import *
import pandas as pd
from db_op import get_engine
from django.db import models


db_engine = get_engine()


def fk_reg(local_key, foreign_key):
    pass


class Obj:
    def __init__(self, db_table_name, tags):
        self._db_table_name = db_table_name
        self.tags = tags

    def booking(self):
        #df = pd.DataFrame(self.tags)
        #df.to_sql(name=self._db_table_name, con=db_engine, schema=SYS_SCHEMA, if_exists='append', index=False)
        for i, tn in enumerate(self._db_table_name):
            print(tn, self.tags[i])


class Tagged:
    def __init__(self, **tags):
        self._tags = tags


class Named:
    def __init__(self, _id, **alias):
        self.id = _id
        self.alias = alias


class Contact(Obj, Named):
    """
    id
    name
    nick
    """
    def __init__(self, **tags):
        self.name = tags['name']
        self.nick = tags['nick']
        Named.__init__(self, _id=tags['id'], name=tags['name'], nick=tags['nick'])
        Obj.__init__(self, db_table_name='contact', tags=tags)


class BD(Contact):
    """
    id
    bd_leader_id
    """
    def __init__(self, **tags):
        self.bd_leader_id = tags['bd_leader_id']
        Contact.__init__(self, **tags)
        Obj.__init__(self,
                     db_table_name=['contact', 'bd'],
                     tags=[
                         {'id': self.id, 'name': self.name, 'nick': self.nick},
                         {'id': self.id, 'bd_leader_id': self.bd_leader_id}
                     ])


class BDLeader(BD):
    def __init__(self, **tags):
        self.location = tags['location']
        BD.__init__(self, **tags, bd_leader_id=tags['id'])
        Obj.__init__(self, db_table_name='bd_leader', tags=tags)


class Ins(Obj):
    def __init__(self, **tags):
        Obj.__init__(self, db_table_name='ins', tags=tags)


def test_init():
    bd = BD(id=1, name='a', nick='b', bd_leader_id=1)
    print(bd.tags)
    print(bd.alias)
    print(bd._db_table_name)
    bd.booking()

if __name__ == '__main__':
    test_init()
