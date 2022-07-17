from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from flask import g

def get_db():
    if 'db' not in g:
        g.db = create_engine('sqlite://',
            connect_args = {"check_same_thread": False}, 
        poolclass = StaticPool)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.dispose()

def init_db():
    db = get_db()

    from .transaction import Base
    Base.metadata.create_all(db)