import os

import openai

from envparse import env
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR.joinpath('.env')
if ENV_FILE_PATH.is_file():
    env.read_envfile(path=ENV_FILE_PATH)

openai.api_key = env.str('OPENAI_API_KEY')


async def gpt_query(message, prev_messages=None, temperature=0.7, model="gpt-3.5-turbo"):
    messages = []
    if not prev_messages:
        all_messages = []
    else:
        all_messages = prev_messages.copy()
    all_messages.append(message)
    for m in all_messages:
        messages.append({"role": "user", "content": m})

    chat = await openai.ChatCompletion.acreate(model=model, messages=messages, temperature=temperature)
    reply = chat.choices[0].message.content
    reply = reply.strip()
    return reply
