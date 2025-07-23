from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.item import ItemModel


class Item(Resource):
    #is a helper class in Flask-RESTful that validates and extracts data from incoming requests (usually POST, PUT, or PATCH requests)
    #It ensures: Only expected fields are accepted
    parser = reqparse.RequestParser()
    # Ensures price is a float, required, and provides an error message if missing.
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")
    #Ensures store_id is an integer and required and provides an error message if missing.
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

    #decorator modifies the behavior of another function without changing its actual code.
    #@jwt_required() ensures that only authenticated users can access this endpoint.
    @jwt_required()
    def get(self, name): #Retrieve an Item
        item = ItemModel.find_by_name(name)
        if item: #exists
            return item.json()
        return {'message': 'Item not found'}, 404

    #Create a New Item
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args() #ensures that the request includes all required fields (price and store_id).

        item = ItemModel(name, **data) # Creates a new ItemModel instance using the name (from the URL) and the parsed data (from the request body). **data unpacks the dictionary into keyword arguments, equivalent to: item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    #Update or Insert an Item
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None: ## Create a new item if it doesn't exist
            item = ItemModel(name, **data) #This is equivalent to: item = ItemModel(name, price=data['price'], store_id=data['store_id'])
            item.save_to_db()
            return item.json(), 201
        else:
            item.price = data['price'] # Update existing item
            item.store_id = data['store_id']
            item.save_to_db()
            return item.json(), 200

#Retrieving a list of all items stored in the database.
class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
