import config as config
from sqlalchemy import Column , String, Integer , ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from database.configdb import db
from database.configdb import engine


class Cart(db.Model):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    product_name = Column(String(80) , nullable=False)
    quantity = Column(Integer , nullable=False)


class BuyLog(db.Model):
    __tablename__ = "buylog"
    id = Column(Integer , primary_key=True)
    product_id =  Column(Integer, nullable=False)
    product_name =  Column(String(80), nullable=False)
    user_id = Column(Integer, nullable=False)
    quantity = Column(Integer , nullable=False)
    category_id = Column(Integer, nullable=False)
    category_name = Column(String(80) , nullable=False)
    date = Column(String(80 ), nullable=False)
    time = Column(String(80 ), nullable=False)

class Manager(db.Model):
    __tablename__ = "manager"
    id = Column(Integer, primary_key=True)
    managername = Column(db.String(80), nullable=False)
    password = Column(db.String(80), nullable=False)

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    password = Column(String(80), nullable=False)
    phone = Column( String(15) , nullable=False)
    address = Column(String(80), nullable=False)


class Product(db.Model):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    unit = Column(String(80), nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    manufacture_date = Column(String(80), nullable=False)
    expiry_date = Column(String(80), nullable=False)


class Category(db.Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(db.String(80), nullable=False, unique=True)

db.Model.metadata.create_all(engine)

