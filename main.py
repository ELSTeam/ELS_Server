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
import FirebaseManagment
import os

if __name__ == "__main__":
    mongo_db = MongoManagment.Mongo()
    firebase = FirebaseManagment.Firebase()
    app = Flask(__name__)
    CORS(app)
    TIME=10

    @app.route('/sign_in', methods=['POST'])
    def sign_in():
        """
        request for sign-in process - when user enters username and password in the payload.
        """
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
        """
        Sign-up new user to the system. In order to sign in the user has to enter - username, password,
        birthday and his email. Also checks that the requested username is not exists in the system.
        """
        try:
            data = request.json
            username = data["username"]
            password = data["password"]
            email = data["email"]
            birthDay = data["birthDay"]
            if mongo_db.add_user(username, password, email, birthDay):
                # returns 200 if username is not exists and created successfully new user in DB.
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            else:
                # returns 400 if username is already exists
                return json.dumps({'success': True}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    @app.route('/update_user_details', methods=['POST'])
    def update_user_details():
        """
        User can update all his password, birthday and email that it entered.
        """
        try:
            data = request.json
            username = data["username"]
            password = data["password"]
            email = data["email"]
            birthDay = data["birthDay"]
            if mongo_db.update_user_details(username, password, email, birthDay):
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
        """
        delete user by putting in the payload username and password
        """
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
        """
        User adding a new contact as a contact person for our system. When user is fall, the contact will be notified.
        """
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
        """
        User's input is his username, this returns his all contacts that will be notified when fall is detected.
        """
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
        """
        User can update his contacts details.
        """
        try:
            data = request.json
            username = data["username"]
            contact_name = data["contact_name"]
            contact_info = data["contact_info"]
            if mongo_db.update_contact_details(username, contact_name, contact_info):
                # returns 200 if updated successfully
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            else:
                # returns 400 if not updated successfully - problem in uploading to database
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    @app.route('/get_data_of_user', methods=['POST'])
    def get_data_of_user():
        """
        Returns all data about a specific user.
        """
        try:
            data = request.json
            username = data["username"]
            output = mongo_db.get_data_of_user(username)
            if output:
                # returns 200 if output is not empty and returns the output as json object.
                return output, 200, {'ContentType': 'application/json'}
            else:
                # returns 400 if there is problem in pulling the data from database.
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    @app.route('/delete_contact', methods=['DELETE'])
    def delete_contact():
        """
        User can delete his contact by getting username and contact's name.
        """
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
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    @app.route('/fall_detected', methods=['POST'])
    def fall_detected():
        """
        Handles when fall detection is occurred - getting the video from the request from the fall detector,
        saves the filename
        """
        try:
            video_file = request.files['file']
            username = video_file.filename.split('#')[1].split('.')[0]
            file_data = {'filename': video_file.filename, 'data': video_file.read()}

            """
            Upload to firebase
            """
            file_upload_firebase(file_data['filename'],file_data['data'])
            
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
        """
        When user falls, this is updates the relevant field in user's document in database
        """
        mongo_db.update_fall_in_process(username, True)
        # returns 200 if updated successfully.
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


    @app.route('/all_history', methods=['POST'])
    def get_all_history():
        """
        By username, it returns a list of json objects that represents the history of falls of the user.
        """
        try:
            data = request.json
            username = data["username"]
            output = mongo_db.get_all_history(username)
            # adding the video url
            if output:
                for item in output:
                    item["video_url"] = firebase.get_file_from_storage(item['filename'])
                # returns 200 if output is not empty and returns list of json objects
                return output, 200, {'ContentType': 'application/json'}
            else:
                # returns 400 if output is empty - no video
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    @app.route('/get_video', methods=['POST'])
    def get_video():
        """
        By input the file name of the fall video, it returns the url for the video to present that in the UI.
        """
        try:
            data = request.json
            filename = data["filename"]
            output = firebase.get_file_from_storage(filename)
            if output:
                return output, 200, {'ContentType': 'application/json'}
            else:
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    
    @app.route('/get_latest_video', methods=['POST'])
    def get_latest_video():
        """
        By getting the username, it returns the video from the last fall that has been detected.
        """
        try:
            data = request.json
            username = data["username"]
            get_latest_video_name = mongo_db.get_latest_video_name(username)
            output = firebase.get_file_from_storage(get_latest_video_name)
            if output:
                # returns 200 and the content.
                return output, 200, {'ContentType': 'application/json'}
            else:
                # returns 400 if the output is empty - no video at all.
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    @app.route('/upload_photo', methods=['POST'])
    def upload_photo():
        """
        When user inputs a photo to his profile in the UI, this updated the photo in the database.
        """
        try:
            photo_file = request.files['file']
            content = photo_file.read()
            file_upload_firebase(photo_file.filename, content)
            username = photo_file.filename.split('#')[1].split('.')[0]
            if mongo_db.upload_photo(username, photo_file.filename):
                # returns 200 if photo uploaded successfully.
                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            else:
                # returns 400 if not uploaded.
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}
    
    def file_upload_firebase(filename:str, contents:base64) -> bool:
        with open(filename,'wb') as file:
            file.write(contents)
        file.close()
        if not firebase.upload_file_to_storage(filename,filename):
            print("Error upload file to firebase")
        else:
            print("File upload to firebase ok")
        os.remove(filename)


    @app.route('/get_photo', methods=['POST'])
    def get_photo():
        """
        By getting the username, it returns the current photo that in database that is connected to the username.
        """
        try:
            data = request.json
            username = data["username"]
            filename = mongo_db.get_photo(username)
            output = firebase.get_file_from_storage(filename)
            if output:
                # returns 200 if output is not empty
                return output, 200, {'ContentType': 'application/json'}
            else:
                # returns 400 if user do not have a profile photo - output is empty.
                return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
        except Exception as e:
            print(e)
            # returns 500 if error is internal
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}


    app.run(port=5000, debug=True, host='0.0.0.0')
