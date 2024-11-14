from env import QuerybookSettings

from .all_ai_assistants import get_ai_assistant_class
from .assistants.tongyi_assistant import TongyiAssistant

if QuerybookSettings.AI_ASSISTANT_PROVIDER:
    ai_assistant = get_ai_assistant_class(QuerybookSettings.AI_ASSISTANT_PROVIDER)
    ai_assistant.set_config(QuerybookSettings.AI_ASSISTANT_CONFIG)

else:
    ai_assistant = None


__all__ = ["ai_assistant"]
