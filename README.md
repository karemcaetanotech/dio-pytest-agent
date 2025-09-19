# dio-pytest-agent
# Agente que gera testes Pytest (LangChain + Azure OpenAI)

Gera automaticamente `test_*.py` a partir de um arquivo Python.

## Requisitos
- Python 3.10+  
- `pip install -r requirements.txt`
- Criar `.env` com base em `.env.example`

## Como rodar
```bash
python src/main.py --input samples/math_ops.py --out tests/test_math_ops.py --sys-path-dir samples
pytest -q
