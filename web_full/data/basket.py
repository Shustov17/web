import datetime
import sqlalchemy
from sqlalchemy import orm


from .db_session import SqlAlchemyBase


class Basket(SqlAlchemyBase):
    __tablename__ = 'basket'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    catalog_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("catalog.id"))
    basket_kol = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
   # user = orm.relationship('User', back_populates='id')
   # catalog = orm.relationship('Catalog', back_populates='id')
