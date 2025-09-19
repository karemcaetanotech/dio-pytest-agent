import os, requests, json
from dotenv import load_dotenv
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
api_version = os.environ["AZURE_OPENAI_API_VERSION"]
dep = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

url = f"{endpoint}/openai/deployments/{dep}/chat/completions?api-version={api_version}"
headers = {"api-key": os.environ["AZURE_OPENAI_API_KEY"], "Content-Type": "application/json"}
payload = {"messages": [{"role":"user","content":"Diga apenas: OK"}], "temperature": 0}

r = requests.post(url, headers=headers, json=payload, timeout=30)
print("status:", r.status_code)
print("body:", r.text[:400])
