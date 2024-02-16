from openai import OpenAI

client = OpenAI(api_key="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")

stream = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[{"role": "user", "content": "Que penses tu de Shakespear, en quelques mots ?"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")