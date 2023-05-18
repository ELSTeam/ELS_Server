import json
import time
import threading
from typing import List

import requests
from flask import Flask, request
import MongoManagment
from datetime import datetime
from bson.binary import Binary
from sms_sender import SMSSender
from email_sender import EmailSender
from flask_cors import CORS
from io import BytesIO
import base64
import zlib

if __name__ == "__main__":
    mongo_db = MongoManagment.Mongo()
    app = Flask(__name__)
    TIME=10
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
            if request.args:
                username = request.args.get("username")
            else:
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


    @app.route('/update_contact', methods=['PUT'])
    def update_contact():
        try:
            data = request.json
            username = data["username"]
            contact_name = data["contact_name"]
            contact_info = data["contact_info"]
            if mongo_db.update_contact_details(username, contact_name, contact_info):
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            else:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    @app.route('/delete_contact', methods=['DELETE'])
    def delete_contact():
        try:
            data = request.json
            username = data["username"]
            contact_name = data["contact_name"]
            if mongo_db.delete_contact_from_user(username, contact_name):
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            else:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    @app.route('/fall_detected', methods=['POST'])
    def fall_detected():
        try:
            video_file = request.files['file']
            username = video_file.filename.split('#')[1].split('.')[0]
            file_data = {'filename': video_file.filename, 'data': video_file.read()}
            # send mail and sms alerts using threading
            mail_sender = EmailSender()
            sms_sender = SMSSender()
            contacts_list = mongo_db.get_all_contacts(username)
            threading.Thread(target=send_alerts, args=(username, contacts_list, sms_sender, mail_sender)).start()
            if mongo_db.fall_detected(username, file_data):
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            else:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    def send_alerts(username: str, contacts_list: List[dict], sms_sender: SMSSender, email_sender: EmailSender) -> None:
        """
        Send alert every x time (can change the time variable at the beggining of the file)
        """
        # get fallinprogress - replace the flag
        while not mongo_db.get_fall_in_process(username):
            for contact in contacts_list:
                phone = contact['phone']
                email = contact['email']
                email_sender.send_mail(email, "Fall detected",f'KUDOS!\nClick here to confirm: http://127.0.0.1:5000/fall_in_process/{username}')
                # sms_sender.send_message(phone,f'KUDOS!\nClick here to confirm: http://127.0.0.1:5000/fall_detected/{user_name}')
                # sms_sender.. - production
            time.sleep(TIME)
        # close the fall in progress
        mongo_db.update_fall_in_process(username, False)
        for contact in contacts_list:
            phone = contact['phone']
            email = contact['email']
            email_sender.send_mail(email, "Someone is on the way", f'KUDOS!')
            # sms_sender.send_message(phone,f'KUDOS!\nClick here to confirm: http://127.0.0.1:5000/fall_detected/{user_name}')
            # sms_sender.. - production


    @app.route('/fall_in_process/<username>', methods=['GET'])
    def fall_in_process(username):
        mongo_db.update_fall_in_process(username, True)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    
    @app.route('/get_latest_video', methods=['POST'])
    def get_latest_video():
        try:
            data = request.json
            username = data["username"]
            output = mongo_db.get_latest_video(username)
            if output:
                return output, 200, {'ContentType': 'application/json'}
            else:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    @app.route('/upload_photo', methods=['POST'])
    def upload_photo():
        try:
            photo_file = request.files['file']
            content = photo_file.read()
            encoded_content = base64.b64encode(content)
            username = photo_file.filename.split('#')[1].split('.')[0]
            if mongo_db.upload_photo(username, encoded_content):
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            else:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    @app.route('/get_photo', methods=['GET'])
    def get_photo():
        try:
            data = request.json
            username = data["username"]
            output = mongo_db.get_photo(username)
            if output:
                return output, 200, {'ContentType': 'application/json'}
            else:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    app.run(port=5000, debug=True, host='0.0.0.0')
