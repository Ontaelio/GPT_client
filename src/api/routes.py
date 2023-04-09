from fastapi import HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRoute
from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.db import contexts
from src.mongo.models import Context


async def get_contexts_full() -> list:
    cursor = contexts.find()
    res = []
    for document in await cursor.to_list(length=None):
        document["_id"] = str(document["_id"])
        res.append(document)
    return res


async def get_contexts() -> list:
    cursor = contexts.find({}, {"name": 1, "description": 1, "_id": 0})
    return await cursor.to_list(length=None)


async def get_context(context: str) -> dict:
    if res := await contexts.find_one({"name": context}, {"_id": 0}):
        return res

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Context {context} not found',
    )


async def post_context(context: Context = Body(...)) -> JSONResponse:
    context = jsonable_encoder(context)
    try:
        new_context = await contexts.insert_one(context)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Error: Duplicate context name',
        )
    inserted = await contexts.find_one({"_id": new_context.inserted_id}, {"_id": 0})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=inserted)


async def update_context(context: Context = Body(...)) -> JSONResponse:
    context = jsonable_encoder(context)
    update_result = await contexts.update_one({"name": context["name"]}, {"$set": context}, upsert=True)
    updated = await contexts.find_one({"name": context["name"]}, {"_id": 0})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=updated)


api_routes = [
    APIRoute(path="/contexts_full", endpoint=get_contexts_full, methods=["GET"]),
    APIRoute(path="/contexts", endpoint=get_contexts, methods=["GET"]),
    APIRoute(path="/context", endpoint=get_context, methods=["GET"]),
    APIRoute(path="/new_context", endpoint=post_context, methods=["POST"]),
    APIRoute(path="/update_context", endpoint=update_context, methods=["PUT"]),
]
