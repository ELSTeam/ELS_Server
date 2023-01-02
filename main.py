import json
import sys
from flask import Flask, jsonify, request
import pymongo
import MongoManagment

if __name__ == "__main__":
    mongo_db = MongoManagment.Mongo()
    app = Flask(__name__)

    @app.route('/sign_in', methods=['POST'])
    def sign_in():
        try:
            data = request.json
            username = data["username"]
            password = data["password"]
            if mongo_db.check_username_password(username, password):
                # returns 200 if username and password are correct
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            else:
                # returns 400 if username or password is incorrect or username is exists
                return json.dumps({'success': True}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    @app.route('/sign_up', methods=['POST'])
    def sign_up():
        try:
            data = request.json
            username = data["username"]
            password = data["password"]
            if mongo_db.add_user(username, password):
                # returns 200 if username is not exists and created successfully new user in DB.
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            else:
                # returns 400 if username is already exists
                return json.dumps({'success': True}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    @app.route('/delete', methods=['DELETE'])
    def delete():
        try:
            data = request.json
            username = data["username"]
            password = data["password"]
            mongo_db.delete_user(username, password)
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    @app.route('/add_contact', methods=['PUT'])
    def add_contact():
        pass


    app.run()


