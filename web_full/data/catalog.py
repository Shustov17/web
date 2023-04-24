import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_wtf import FlaskForm

from .db_session import SqlAlchemyBase


class Catalog(SqlAlchemyBase):
    __tablename__ = 'catalog'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    catalog_kol = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    basket = orm.relationship("Basket")
