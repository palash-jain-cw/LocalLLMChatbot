from typing import Callable
from ollama import chat
from localllmchatbot.logger_setup import loguru_setup

logger = loguru_setup()


class LocalModelChat:
    def __init__(
        self,
        model: str,
        base_url: str,
        system_prompt: str,
        tools: list[Callable],
    ):
        logger.info(
            f"Initializing ChatOllama with model: {model}, base_url: {base_url}, system_prompt: {system_prompt}, and tools: {tools}"
        )
        self.model = model
        self.base_url = base_url
        self.system_prompt = system_prompt
        self.tools = tools
        self.message_history = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
        ]

    def _generate_chat_response(self, prompt, stream=False):
        logger.info(f"Generating chat response for prompt: {prompt}")
        self.message_history.append({"role": "user", "content": prompt})
        response = chat(model=self.model, messages=self.message_history, stream=stream)
        return response

    def _clear_message_history(self):
        logger.info("Clearing message history")
        self.message_history = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
        ]
