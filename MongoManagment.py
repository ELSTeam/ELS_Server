import pymongo
import sys


class Mongo:
    def __init__(self):
        print("Connecting to Atlas")
        try:
            self.url = f'mongodb+srv://els_admin:{sys.argv[1]}@els.r9xuzuv.mongodb.net/test'
            self.client = pymongo.MongoClient(self.url)
            self.db = self.client.els_db
            self.collection = self.db.els_db
        except Exception as e:
            print("Error from Atlas")
            print(e)
            exit(1)
        print("Connected.")

    def find_user(self, user_name: str) -> object:
        """
        Function checks for user based on username.
        :param user_name: string username
        :return: user object if found else None
        """
        return self.collection.find_one({"username": user_name})

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


    def add_new_contact_to_username(self, username: str, contact_name: str, phone: str, mail: str) -> bool:
        """
        Function first check if username exists, and add contact to current username.
        :param username: username string of the user
        :param contact_name: password string of the user
        :param phone: password string of the user
        :param mail: password string of the user
        :return: True if added successfully, or False if not succeeded
        """
        user = self.find_user(username)
        if not user:
            return False
        contact_info = {"name": contact_name, "phone": phone, "email": mail}
        self.collection.update_one(
            {"username": username},
            {"$push": {"contacts": contact_info}}, upsert = True)
        return True


    def delete_user(self, username: str, password: str) -> None:
        """
        Function delete user. by checking the password and username
        :param username: username of the user
        :param password: password of the user
        """
        query = {"username": username, "password": password}
        self.collection.delete_one(query)


# mongo = Mongo()
# print(mongo.find_user("omerap12"))
# mongo.add_user("test", "testme")
# print(mongo.check_username_password("omerap12", "Aa123456!"))  # return True
# print(mongo.check_username_password("omerap12", "false"))  # return False
