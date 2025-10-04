import os, openai, json
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

CHAT_MODEL = "gpt-4o-mini"
TEMP = 0.7

chat_history = [{"role": "system", "content": "You are a friendly, helpful eductional tutor. Make sure to keep it K-12."}]

def getAnswer():
    return openai.chat.completions.create(model=CHAT_MODEL, messages=chat_history, temperature=TEMP).choices[0].message

while True:
    query = input()
    query = {"role": "user", "content": query}
    chat_history.append(query)
    answer = getAnswer()
    print(answer.content.strip())
    chat_history.append(answer)
    if input("Quit? (y/N)").lower() == "y":
        break

with open("history.json", 'w') as f:
    json.dump(chat_history, f, indent=4)