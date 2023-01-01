import sys
from flask import Flask, jsonify, request
import pymongo


if __name__ == "__main__":
    connection_url = f'mongodb+srv://els_admin:{sys.argv[2]}@els.r9xuzuv.mongodb.net/test'
    # app = Flask(__name__)
    client = pymongo.MongoClient(connection_url)