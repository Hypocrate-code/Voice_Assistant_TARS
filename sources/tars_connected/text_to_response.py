from utils import get_api_key

from openai import OpenAI, AuthenticationError
from errors_response import api_key_invalid

client = OpenAI(api_key=get_api_key("openai"))

requête = input("Veuillez entrez votre requete")
try:
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are Tars, a voice assistant that can't use more than 350 tokens"},
            {"role": "user", "content": requête}
        ],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
except AuthenticationError:
    api_key_invalid()

