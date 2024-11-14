import openai
import tiktoken
from langchain_community.llms.tongyi import Tongyi
from dashscope import get_tokenizer

from lib.ai_assistant.base_ai_assistant import BaseAIAssistant
from lib.logger import get_logger

LOG = get_logger(__file__)


TONGYI_MODEL_CONTEXT_WINDOW_SIZE = {
    # Legacy models
    "qwen-max": 128000
}
DEFAULT_MODEL_NAME = "qwen-max"


class TongyiAssistant(BaseAIAssistant):
    """To use it, please set the following environment variable:
    OPENAI_API_KEY: OpenAI API key
    """

    @property
    def name(self) -> str:
        return "TongyiAssistant"

    def _get_context_length_by_model(self, model_name: str) -> int:
        return (
            TONGYI_MODEL_CONTEXT_WINDOW_SIZE.get(model_name)
            or TONGYI_MODEL_CONTEXT_WINDOW_SIZE[DEFAULT_MODEL_NAME]
        )

    def _get_default_llm_config(self):
        default_config = super()._get_default_llm_config()
        if not default_config.get("model_name"):
            default_config["model_name"] = DEFAULT_MODEL_NAME

        return default_config

    def _get_token_count(self, ai_command: str, prompt: str) -> int:
        model_name = self._get_llm_config(ai_command)["model_name"]
        encoding = get_tokenizer(model_name)
        return len(encoding.encode(prompt))

    def _get_error_msg(self, error) -> str:
        if isinstance(error, openai.AuthenticationError):
            return "Invalid TongYi API key"

        return super()._get_error_msg(error)

    def _get_llm(self, ai_command: str, prompt_length: int):
        config = self._get_llm_config(ai_command)
        return Tongyi(**config)
