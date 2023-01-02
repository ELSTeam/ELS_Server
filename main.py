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
            # returns 200 - deleted user successfully
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    @app.route('/add_contact', methods=['PUT'])
    def add_contact():
        try:
            data = request.json
            username = data["username"]
            contact_info = data["contact_info"]
            if mongo_db.add_new_contact_to_username(username, contact_info):
                # returns 200 if added contact successfully
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            else:
                # returns 400 if username is not exists.
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    @app.route('/all_contacts', methods=['GET'])
    def get_all_contacts():
        try:
            data = request.json
            username = data["username"]
            contacts_json = mongo_db.get_all_contacts(username)
            if not contacts_json:
                # returns 400 if list of contacts is empty -> user not found.
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
            else:
                # returns 200 if user has list of contacts and returns list of json objects.
                return json.dumps({'contacts': contacts_json}), 200, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    app.run()

