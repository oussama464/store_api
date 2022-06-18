from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="this filed cannot be left black")
    parser.add_argument("store_id", type=int, required=True, help="every item need a store_id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f'an item with name {name} already exists'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except Exception as e:
            return {"message": f"an error occurred inserting the item {e}"}
        return item.json(), 201

    def delete(self, name):
        item: ItemModel = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "item deleted !"}

    def put(self, name):
        data = Item.parser.parse_args()
        item: ItemModel = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
