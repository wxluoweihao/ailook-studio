from langchain_community.llms.tongyi import Tongyi

from lib.ai_assistant.assistants.tongyi_assistant import TongyiAssistant

ALL_PLUGIN_AI_ASSISTANTS = [TongyiAssistant()]

# Example to add openai assistant
#
# from lib.ai_assistant.assistants.openai_assistant import OpenAIAssistant
#
# ALL_PLUGIN_AI_ASSISTANTS = [OpenAIAssistant()]
