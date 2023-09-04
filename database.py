from pymongo import MongoClient, ASCENDING

client = MongoClient(
    "mongodb+srv://mycal:123Admin!@apitest.1egxbjh.mongodb.net/?retryWrites=true&w=majority")

db = client.todo_db

user_register_collection = db["user_register_collection"]
admin_collection = db["admin_collection"]
job_applies_collection = db["job_applies_collection"]

# Create a unique index on the 'email' field
user_register_collection.create_index([("email", ASCENDING)], unique=True)
