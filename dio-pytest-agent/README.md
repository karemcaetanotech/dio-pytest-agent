# DIO - Agente que gera testes Pytest (LangChain + Azure OpenAI)

Como rodar:
```bash
python -m venv .venv && source .venv/bin/activate   # Win: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # preencha as chaves Azure OpenAI
python src/main.py --input samples/math_ops.py --out tests/test_math_ops.py --sys-path-dir samples
pytest -q
```
