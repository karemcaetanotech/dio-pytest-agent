import os, requests, pathlib
from dotenv import load_dotenv, dotenv_values

here = pathlib.Path(__file__).resolve().parent
env_path = here / ".env"
print("ENV PATH:", env_path)

# carrega exatamente ESTE .env
load_dotenv(dotenv_path=str(env_path), override=True)
cfg = dotenv_values(str(env_path))

print("endpoint:", cfg.get("AZURE_OPENAI_ENDPOINT"))
print("deployment:", cfg.get("AZURE_OPENAI_CHAT_DEPLOYMENT"))
print("api_version:", cfg.get("AZURE_OPENAI_API_VERSION"))
print("key_length:", len((cfg.get("AZURE_OPENAI_API_KEY") or "")))

# chamada simples só pra validar rede/endpoint
url = cfg["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/openai/deployments"
params = {"api-version": cfg["AZURE_OPENAI_API_VERSION"]}
headers = {"api-key": cfg["AZURE_OPENAI_API_KEY"]}
r = requests.get(url, params=params, headers=headers, timeout=20)
print("HTTP status:", r.status_code)
print("Body head:", r.text[:300])
