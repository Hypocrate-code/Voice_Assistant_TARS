import threading

from response_to_speech import Tars_vocal

def say_this(mot):
    Tars_vocal().say(mot)

phrase = "salut comment vas tu"
phrase = phrase.split()
print(phrase)

# thread1 = threading.Thread(target=say_after_3, args=[mot])
for mot in phrase:
    threading.Thread(target=say_this, args=[mot]).start()


# import asyncio

# async def say_after(delay, what):
#     await asyncio.sleep(delay)
#     print(what)

# async def streaming():
#     task1 = asyncio.create_task(
#         say_after(4, 'hello'))

#     task2 = asyncio.create_task(
#         say_after(4, 'world'))


#     # Wait until both tasks are completed (should take
#     # around 2 seconds.)
#     await task1
#     await task2

# asyncio.run(streaming())





# import threading

# from response_to_speech import Tars_vocal
# from utils import get_api_key
# from errors_response import api_key_invalid

# from openai import OpenAI, AuthenticationError

# class Tars_answering:
#     def __init__(self):
#         self.client = OpenAI(api_key=get_api_key("openai"))
#         self.tars_vocal = Tars_vocal()
#     def answer(self, requete):
#         try:
#             stream = self.client.chat.completions.create(
#                 model="gpt-3.5-turbo-0125",
#                 messages=[
#                     {"role": "system", "content": "Tu es Tars, un assistant vocal. N'utilise pas plus de 260 caractères, écris les chiffres en toute lettre."},
#                     {"role": "user", "content": requete}
#                 ],
#                 stream=True,
#             )
#             print(stream)

#             total = ""
#             for chunk in stream:
#                 if chunk.choices[0].delta.content is not None:
#                     # total+=chunk.choices[0].delta.content
#                     self.tars_vocal.say(chunk.choices[0].delta.content)
#         except AuthenticationError:
#             api_key_invalid("openai")

# Bot = Tars_answering()
# Bot.answer("salut quelle est l'utliité des nombres complexes dans l'informatique")