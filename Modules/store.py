from db import db
from itemsmodel1 import ItemModel


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel',lazy = 'dynamic')




    def __init__(self,name):
        self.name = name

    def json(self):
        return {'items': [item.json() for item in self.items.all()],'name':self.name,}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() # first() returns the first row only



    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
