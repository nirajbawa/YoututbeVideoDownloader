# from pymongo import MongoClient


# conn = MongoClient("")
# conn = conn.fastApi

import motor.motor_asyncio

DATABASE_URL = "mongodb+srv://nirajbava222:A69MmysMxiO2AY0V@cluster0.lpesy3f.mongodb.net/test"

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
database = client.get_database("fastApi")