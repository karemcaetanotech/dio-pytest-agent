import os, re
from dataclasses import dataclass
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI

load_dotenv()

PROMPT_TEMPLATE = """
You are a senior Python QA engineer. Generate a pure Python pytest file for the module below.

Rules:
- Output ONLY Python (no backticks).
- First line MUST be: import pytest
- Include def test_* functions for success and failure cases.
- Use with pytest.raises(...) for error cases.
- Import the module under test appropriately; assume it is importable by name if unsure.

MODULE NAME:
{module_name}

MODULE CODE:
{module_code}
"""

@dataclass
class AgentConfig:
    temperature: float = 0.2
    model_deployment: str = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o-mini")
    api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
    endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")

class TestGenAgent:
    def __init__(self, config: AgentConfig | None = None):
        self.config = config or AgentConfig()
        if not all([self.config.endpoint, self.config.api_key, self.config.api_version, self.config.model_deployment]):
            raise RuntimeError("Missing Azure OpenAI configuration. Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_CHAT_DEPLOYMENT.")
        self.llm = AzureChatOpenAI(
            azure_endpoint=self.config.endpoint,
            api_key=self.config.api_key,
            api_version=self.config.api_version,
            deployment_name=self.config.model_deployment,
            temperature=self.config.temperature,
        )
        self.prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        self.chain = self.prompt | self.llm | StrOutputParser()

    @staticmethod
    def _strip(text: str) -> str:
        text = text.strip()
        text = re.sub(r'^```(?:python)?\s*', '', text)
        text = re.sub(r'\s*```\s*$', '', text)
        return text.strip() + "\n"

    @staticmethod
    def _ensure_pytest_first(text: str) -> str:
        lines = [l for l in text.splitlines() if l.strip()]
        if not lines or lines[0].strip() != 'import pytest':
            lines = ['import pytest'] + lines
        return "\n".join(lines) + "\n"

    @staticmethod
    def _inject_sys_path(text: str, rel_dir: str | None) -> str:
        if not rel_dir:
            return text
        header = (
            "\nimport sys, pathlib\n"
            f"sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / '{rel_dir}'))\n\n"
        )
        lines = text.splitlines(keepends=True)
        if lines and lines[0].strip() == 'import pytest':
            return lines[0] + header + ''.join(lines[1:])
        return header + text

    def generate(self, module_code: str, module_name: str, add_sys_path_dir: str | None = None) -> str:
        out = self.chain.invoke({"module_name": module_name, "module_code": module_code})
        out = self._strip(out)
        out = self._ensure_pytest_first(out)
        out = self._inject_sys_path(out, add_sys_path_dir)
        return out
