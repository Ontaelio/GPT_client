from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from src.gpt import gpt_query

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    content = await gpt_query('Provide a single sentence with cats in it')
    return templates.TemplateResponse('client.html', {
        'request': request,
        'content': content
    })


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
