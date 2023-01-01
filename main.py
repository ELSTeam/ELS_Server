import sys
from flask import Flask, jsonify, request
import pymongo

if __name__ == "__main__":
    # connection_url = f'mongodb+srv://els_admin:{sys.argv[1]}@els.r9xuzuv.mongodb.net/test'
    # client = pymongo.MongoClient(connection_url)
    # collection = client.els_db.els_db

    # get all users
    # users = collection.find_one({"username": "omerap12"})
    # print(users["username"])
    users = [{"username": "omerap12", "password": "1234Aa"}, {"username": "avitalos", "password": "98876A"}]
    app = Flask(__name__)
    @app.route('/sign_in', methods=['GET'])
    def sign_in():
        # get username and password from UI - now its hard-coded
        username = "avitalos"
        password = "98876A"
        for user in users:
            if user["username"] == username and user["password"] == password:
                return 'ok', 200
        return 'not found', 404

    app.run()


