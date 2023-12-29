from foolish_admin.config import config

import random
import string
from sqlalchemy import create_engine,Column,String,Integer,insert,select,text
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base,sessionmaker

Base=declarative_base()

engine=create_engine(config['sqlite_url'])
connection=engine.connect()

Session=sessionmaker(bind=engine)
session=Session()

class Users(Base):
    __tablename__="users"
    id=Column(Integer(),primary_key=True)
    user=Column(String(128),nullable=False)
    password=Column(String(128),nullable=False,unique=True)

class Keys(Base):
    __tablename__="keys"
    id=Column(Integer(),primary_key=True)
    n=Column(String(255),nullable=False)
    e=Column(String(255),nullable=False)
    phi=Column(String(255),nullable=True)

class Sessions(Base):
    __tablename__="sessions"
    id=Column(Integer(),primary_key=True)
    session=Column(String(128),nullable=False)


Base.metadata.create_all(engine)

admin_list=session.execute(select(Users)).first()
if admin_list is not None:
    admin_query=insert(Users).values(**{"id":0,"user":"admin","password":''.join(random.choices(string.ascii_letters,k=8))})
    session.execute(admin_query)
    session.commit()

def verify_password(password:str) -> bool:
    output=session.execute(select(Users.password)).first()
    return output[0]==password
    
def session_checker(sessionID:str) -> bool:
    statement="SELECT id,session FROM sessions where session='{}'".format(sessionID)
    rs=connection.execute(text(statement)).fetchall()
    session.rollback()
    return bool(1 if rs is not None else 0)

def add_session(sessionID:str) -> bool:
    session_list=session.execute(select(Sessions)).first()
    if session_list is not None:
        query=insert(Sessions).values(**{"id":0,"session":sessionID})
        session.execute(query)
        session.commit()

def rsa_keys(add=False,keys=None):
    if not add:
        output=session.execute(select(Keys.n,Keys.e)).first()
        return output
    else:
        query=insert(Keys).values(id=0,n=keys[0],e=keys[1],phi=keys[2])
        session.execute(query)
        session.commit()
