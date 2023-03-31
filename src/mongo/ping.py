import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from envparse import env
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR.joinpath('.env')
if ENV_FILE_PATH.is_file():
    env.read_envfile(path=ENV_FILE_PATH)

user = env.str('ATLAS_USER')
password = env.str('ATLAS_PASSWORD')


async def ping_server():
    # Replace the placeholder with your Atlas connection string
    uri = f"mongodb+srv://{user}:{password}@cluster0.zl31klu.mongodb.net/?retryWrites=true&w=majority"
    # Set the Stable API version when creating a new client
    client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


asyncio.run(ping_server())