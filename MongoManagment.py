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
        :param user_name: user name string of the new user
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


# mongo = Mongo()
# print(mongo.find_user("omerap12"))
# mongo.add_user("test", "testme")
