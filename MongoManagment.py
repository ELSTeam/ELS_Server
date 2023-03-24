import pymongo
from bson.binary import Binary
import os


class Mongo:
    def __init__(self):
        print("Connecting to Atlas")
        try:
            mongo_key = os.environ["KEY"]
            self.url = f'mongodb+srv://els_admin:{mongo_key}@els.r9xuzuv.mongodb.net/test'
            self.client = pymongo.MongoClient(self.url)
            self.db = self.client.els_db
            self.collection = self.db.els_db
        except Exception as e:
            print("Error from Atlas")
            print(e)
            exit(1)
        print("Connected.")

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

    def add_user(self, user_name: str, password: str) -> bool:
        """
        Function adds new user, first checking if username already in db, if not it adds him to the db.
        :param user_name: username string of the new user
        :param password: password string of the new user
        :return: True if user added else false
        """
        check_for_user = self.find_user(user_name)
        if check_for_user:
            return False
        userDocument = {
            "username": user_name,
            "password": password,
            "dateOfBirth": None,
            "contacts": [],
            "historyOfFalls": []
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
        user = self.find_user(username)
        if not user:
            return False
        self.collection.update_one(
            {"username": username},
            {"$push": {"historyOfFalls": fall_info}}, upsert=True)
        return True



# print(mongo.find_user("omerap12"))
# mongo.add_user("test", "testme")
# print(mongo.check_username_password("omerap12", "Aa123456!"))  # return True
# print(mongo.check_username_password("omerap12", "false"))  # return False
