import sqlite3
from Requests import request
from flask_restful import Resource , reqparse
from flask_jwt import jwt_required
from flask import jsonify
from Modules.itemsModel1 import ItemModel


class Item(Resource):


    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank!")

    parser.add_argument('store_id',
            type=int,
            required=True,
            help="Every item needs a store id")


    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"messsage":"Item not found"},404


    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"message":"An item with {} has already been created".format(name)} , 400

        data = Item.parser.parse_args()

        item = ItemModel(name,data['price'],data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': ' An error occurred inserting item'} , 500


        return item.json(), 201



    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self,name):
        data = request.get_json()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name,data['price'])

        if item is None:
            item = ItemModel(name,data['price'], data['store_id'])

        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()




        return item.json()

class Itemlist(Resource):

    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
        #return {'items':list(map(lambda x : x.json(),ItemModel.query.all()))}




            #row = item.fetchone()


        #return {"items": row}
    def post(self, name):
        request.get_json()
