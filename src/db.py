from envparse import env
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR.joinpath('.env')
if ENV_FILE_PATH.is_file():
    env.read_envfile(path=ENV_FILE_PATH)

user = env.str('ATLAS_USER')
password = env.str('ATLAS_PASSWORD')
server = env.str('ATLAS_SERVER')
mongo_uri = f"mongodb+srv://{user}:{password}@{server}/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(mongo_uri)
db = client.gpt_api
contexts = db.contexts
contexts.create_index("name", unique=True)
