import array
import json
from datetime import datetime
import pymongo
from bson.binary import Binary
import os
import gridfs
import base64
import io
from gridfs import GridFSBucket


class Mongo:
    def __init__(self):
        print("Connecting to Atlas")
        try:
            mongo_key = os.environ["KEY"]
            self.url = f'mongodb+srv://els_admin:{mongo_key}@els.r9xuzuv.mongodb.net/test'
            self.client = pymongo.MongoClient(self.url)
            self.db = self.client.els_db
            self.fs = gridfs.GridFS(self.db)
            self.bucket = GridFSBucket(self.db, "files")
            self.collection = self.db.els_db
        except Exception as e:
            print("Error from Atlas")
            print(e)
            exit(1)
        print("Connected...")

    def find_user(self, username: str) -> object:
        """
        Function checks for user based on username.
        :param user_name: string username
        :return: user object if found else None
        """
        return self.collection.find_one({"username": username})

    def find_contact_by_user(self, username: str, contact_name: str) -> object:
        """
        Function checks if contact apperears in user's contact list by his contact_name.
        :param user_name: string username
        :param contact_name: string contact_name
        :return: user object if found else None
        """
        return self.collection.find_one({"username": username, "contacts.name": contact_name})

    def add_user(self, user_name: str, password: str, email: str, birthDay: str) -> bool:
        """
        Function adds new user, first checking if username already in db, if not it adds him to the db.
        :param user_name: username string of the new user
        :param password: password string of the new user
        :param email: password string of the new user
        :param birthDay: password string of the new user
        :return: True if user added else false
        """
        check_for_user = self.find_user(user_name)
        if check_for_user:
            return False
        userDocument = {
            "username": user_name,
            "password": password,
            "birthDay": birthDay,
            "email": email,
            "contacts": [],
            "historyOfFalls": [],
            "profile_img": None,
            "fallInProcess": False
        }
        self.collection.insert_one(userDocument)
        return True

    def check_username_password(self, username: str, password: str) -> bool:
        """
        Function checks if username and password are matching in the db.
        :param username: username string of the user
        :param password: password string of the user
        :return: True if valid else false
        """
        user = self.find_user(username)
        if not user:
            return False
        return user["password"] == password

    def add_new_contact_to_username(self, username: str, contact_info: object) -> bool:
        """
        Function first check if username exists, and add contact to current username.
        :param contact_info: json that contains contact_name, phone. mail.
        :param username: username string of the user
        :return: True if added successfully, or False if not succeeded
        """
        user = self.find_user(username)
        if not user:
            return False
        self.collection.update_one(
            {"username": username},
            {"$push": {"contacts": contact_info}}, upsert=True)
        return True

    def update_user_details(self, username: str, password: str, email: str, birthDay: str):
        """
        Function first check if username exists, if exists it updated the details.
        :param username: username string of the user
        :param password: password string of the password
        :param email: email string of the user's email
        :param birthDay: birthDay string of the user's birthday.
        :return: True if updated successfully, or False if user not found.
        """
        user = self.find_user(username)
        if not user:
            return False
        if user["password"] != password:
            self.collection.update_one(
                {"username": username},
                {"$set": {"password": password}})
        if user["email"] != email:
            self.collection.update_one(
                {"username": username},
                {"$set": {"email": email}})
        if user["birthDay"] != birthDay:
            self.collection.update_one(
                {"username": username},
                {"$set": {"birthDay": birthDay}})
        return True

    def get_data_of_user(self, username: str) -> json:
        """
        Function first check if username exists, and returns the json object of the details.
        :param username: username string of the user
        """
        user = self.find_user(username)
        if not user:
            return []
        json_output = {"password": user["password"], "birthDay": user["birthDay"], "email": user["email"]}
        return json.dumps(json_output)

    def delete_user(self, username: str, password: str) -> None:
        """
        Function delete user. by checking the password and username
        :param username: username of the user
        :param password: password of the user
        """
        query = {"username": username, "password": password}
        self.collection.delete_one(query)

    def get_all_contacts(self, username: str) -> list:
        """
        Function returns all contacts of the username
        :param username: username of the user
        :return list: list of json objects that represents the username contacts - returns empty list if user not exists
        """
        user = self.collection.find_one({"username": username})
        if not user:
            return []
        else:
            return user["contacts"]

    def update_contact_details(self, username: str, contact_name: str, contact_info: object) -> bool:
        """
        Function update the contact details by specific username
        :param username: username of the user
        :param contact_name: contact of the user
        :param contact_info: contact's info
        :return bool: false - if user/contact not exist, true - if succeeded
        """
        user = self.find_user(username)
        if not user:
            return False
        contact = self.find_contact_by_user(username, contact_name)
        if not contact:
            return False
        self.collection.update_one(
            {"username": username, "contacts.name": contact_name},
            {"$set": {"contacts.$": contact_info}})
        return True

    def delete_contact_from_user(self, username: str, contact_name: str) -> bool:
        """
        Function delete the contact from specific username
        :param username: username of the user
        :param contact_name: contact of the user
        :return bool: false - if user/contact not exist, true - if succeeded
        """
        user = self.find_user(username)
        if not user:
            return False
        contact = self.find_contact_by_user(username, contact_name)
        if not contact:
            return False
        self.collection.update_one(
            {"username": username, "contacts.name": contact_name},
            {"$pull": {"contacts": {"name": contact_name}}})
        return True

    def fall_detected(self, username: str, fall_info: object) -> bool:
        """
        Function update the history of falls when fall is detected.
        :param username: username of the user
        :param fall_info: contact of the user
        :return bool: false - if user/contact not exist, true - if succeeded
        """
        user = self.find_user(username)
        if not user:
            return False
        self.collection.insert_one(fall_info)
        self.collection.update_one(
            {"username": username},
            {"$push": {"historyOfFalls": {"filename": fall_info["filename"], "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}}}, upsert=True)
        return True

    def get_fall_in_process(self, username: str) -> bool:
        """
        check if the flag in the user's document is true or false.
        :param username: username of the user
        """
        user = self.collection.find_one({"username": username})
        return user["fallInProcess"]

    def update_fall_in_process(self, username: str, bool_value: bool) -> None:
        """
        update the flag in the user's document when contact clicks on the link.
        :param username: username of the user
        :param bool_value: True of False for updating if fall is still not handled.
        """
        self.collection.update_one(
            {"username": username},
            {"$set": {"fallInProcess": bool_value}})

    def get_latest_video(self, username: str) -> bytes:
        """
        Checks if user is exists and returns his last video of fall to the client.
        :param username: username of the user
        """
        user = self.collection.find_one({"username": username})
        if not user:
            return []
        fall_info_from_mongo = user["historyOfFalls"][-1]
        file_data = self.collection.find_one({'filename': fall_info_from_mongo["filename"]})
        return file_data["data"]
    
    def get_latest_video_name(self,username:str) -> str:
        """
        Checks if user is exists and returns his video of fall by it's filename.
        :param username: username of the user
        """
        user = self.collection.find_one({"username": username})
        if not user:
            return []
        fall_info_from_mongo = user["historyOfFalls"][-1]
        return fall_info_from_mongo["filename"]

    def upload_photo(self, username: str, encoded_content: bytes) -> bool:
        """
        Uploading user's profile photo that it has been uploaded. If exists, it updates it.
        :param username: username of the user.
        :param encoded_content: bytes of the user's photo.
        """
        user = self.collection.find_one({"username": username})
        if not user:
            return []
        self.collection.update_one(
            {"username": username},
            {"$set": {"profile_img": encoded_content}}, upsert=True)
        return True

    def get_photo(self, username: str) -> bytes:
        """
        Returns the photo of specific user by his username.
        :param username: username of the user.
        """
        user = self.collection.find_one({"username": username})
        if not user:
            return []
        return user["profile_img"][0]

    def get_all_history(self, username: str) -> object:
        """
        Returns list of all user's history of falls by getting his username.
        :param username: username of the user.
        """
        user = self.collection.find_one({"username": username})
        if not user:
            return []
        return user["historyOfFalls"]

    def get_video(self, filename: str) -> bytes:
        """
        Returns the video filename to pull it from firebase.
        :param filename: the filename of the video of the fall.
        """
        file = self.collection.find_one({'filename': filename})
        if not file:
            return []
        return file["data"]

