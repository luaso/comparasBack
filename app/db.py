from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

class BaseModelMixin:

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        print("netro al delete ")
        db.session.commit()


    @classmethod
    def get_joins(**kwargs):
        print("entro al get_joins")
        return db.session.query(**kwargs)

    @classmethod
    def get_all(cls):
        print("entro al get_all")
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        print("entro al get_by_id")
        return cls.query.get(id)


    @classmethod
    def simple_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()