from fastapi.routing import APIRoute
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request


async def get_contexts_list(request: Request) -> list:
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["gpt_api"]
    cursor = await mongo_client.contexts.find_all()
    res = []
    for document in cursor:
        document["_id"] = str(document["_id"])
        res.append(document)
    return res


async def get_context(request: Request) -> dict:
    ...


async def post_context(request: Request) -> dict:
    ...


async def create_record(request: Request) -> dict:
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["test_database"]
    await mongo_client.records.insert_one({"sample": "record"})
    return {"Success": True}


async def get_records(request: Request) -> list:
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["test_database"]
    cursor = mongo_client.records.find({})
    res = []
    for document in await cursor.to_list(length=100):
        document["_id"] = str(document["_id"])
        res.append(document)
    return res


api_routes = [
    APIRoute(path="/create_record", endpoint=create_record, methods=["POST"]),
    APIRoute(path="/get_records", endpoint=get_records, methods=["GET"]),
]