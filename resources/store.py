from flask_restful import reqparse, Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": f"store {name} not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"a store with name {name} already exists in the databse"}, 400
        store: StoreModel = StoreModel(name)
        try:
            store.save_to_db()
        except Exception as e:
            return {"message": f"an error occurred while creating the store"}, 500
        return store.json(), 201

    def delete(self, name):
        store: StoreModel = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": f"store {name} deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
