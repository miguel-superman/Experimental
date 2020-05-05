import sqlite3
from flask_restful import Resource , reqparse
from flask_jwt import jwt_required
from flask import jsonify
from itemsModel import ItemModel


class Item(Resource):


    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank!")

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
        item = ItemModel(name,data['price'])

        try:
            Item.insert()
        except:
            return {'message': ' An error occurred inserting item'} , 500


        return item, 201



    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()

        return {'messgae': 'Item deleted'}

    def put(self,name):
        data = request.get_json()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name,data['price']}

        if item is None:
            try:
                updated_item.insert()
            except:
                return {'messgae':{'An error occured inserting the item'}} ,500
        else:
            try:
                updted_item.update()
            except:
                return {'messgae':{'An error occured updating the item'}} ,500

        return updated_item.json()

class Itemlist(Resource):
    """ created a get function to pull all the devices from the sqlite3 database with the below code"""
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name':row[0],'price':row[1]})

        connection.close()

    return {'items':items}





            #row = item.fetchone()


        #return {"items": row}
    def post(self, name):
        request.get_json()
