from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from markdown import markdown

from src.gpt.client import gpt_query

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    # content = await gpt_query('Provide a single sentence with cats in it')
    return templates.TemplateResponse('client.html', {
        'request': request,
        # 'content': content
    })


@app.get("/web_request/", response_class=HTMLResponse)
async def web_request(request: Request, question: str, temperature: str, context: str): #Annotated[str, Form()]):

    print(question, temperature, context)

    tmp = float(temperature)

    content = await gpt_query(question, context=context, temperature=tmp)
    return templates.TemplateResponse('client.html', {
        'request': request,
        'content': content
    })


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
