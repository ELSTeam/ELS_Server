import sys
# from flask import Flask, jsonify, request
import pymongo

if __name__ == "__main__":
    connection_url = f'mongodb+srv://els_admin:{sys.argv[1]}@els.r9xuzuv.mongodb.net/test'
    # app = Flask(__name__)
    client = pymongo.MongoClient(connection_url)
    collection = client.els_db.els_db

    # get all users
    users = collection.find_one()
    print(users)

