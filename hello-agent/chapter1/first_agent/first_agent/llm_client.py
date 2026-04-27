import os
import re
from typing import Protocol

from dotenv import load_dotenv
from openai import OpenAI

OPENAI_DEFAULT_MODEL = "gpt-4o-mini"


class LLMClient(Protocol):
    def generate(self, prompt: str, system_prompt: str) -> str:
        """Generate the next Thought-Action pair."""


class OpenAICompatibleClient:
    """Client for OpenAI-compatible chat completion APIs."""

    def __init__(self, model: str, api_key: str, base_url: str | None = None) -> None:
        self.model = model
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str, system_prompt: str) -> str:
        print("正在调用大语言模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                stream=False,
            )
        except Exception as exc:
            return f"Thought: 调用语言模型失败，需要告知用户错误。\nAction: Finish[错误:调用语言模型服务时出错 - {exc}]"

        if not response.choices:
            data = response.model_dump()
            error_message = data.get("msg") or data.get("message") or data.get("error") or data
            return (
                "Thought: 模型服务返回了异常响应，需要告知用户错误。\n"
                f"Action: Finish[错误:调用语言模型服务时出错 - {error_message}]"
            )

        answer = response.choices[0].message.content
        print("大语言模型响应成功。")
        return answer or "Thought: 模型没有返回内容。\nAction: Finish[错误:模型没有返回内容。]"


class MockTravelLLMClient:
    """A deterministic fake LLM so Chapter 1.3 can run without API keys."""

    def generate(self, prompt: str, system_prompt: str) -> str:
        _ = system_prompt
        city = _extract_city(prompt)

        if "Observation:" not in prompt:
            return (
                "Thought: 首先需要获取目标城市今天的天气情况，之后再根据天气情况推荐景点。\n"
                f'Action: get_weather(city="{city}")'
            )

        if "get_attraction" not in prompt:
            weather = _extract_weather(prompt)
            return (
                "Thought: 已经获得天气信息，接下来应该根据天气选择适合游览的景点。\n"
                f'Action: get_attraction(city="{city}", weather="{weather}")'
            )

        attraction = _extract_last_observation(prompt)
        weather = _extract_weather(prompt)
        return (
            "Thought: 已经获得天气和景点推荐，可以整合信息给用户最终答复。\n"
            f"Action: Finish[今天{city}的天气是{weather}。{attraction}]"
        )


def build_llm_client(mode: str = "mock") -> LLMClient:
    """Build a mock or real OpenAI-compatible client from environment variables."""

    load_dotenv()

    normalized = mode.lower()
    if normalized == "mock":
        return MockTravelLLMClient()

    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("OPENAI_MODEL") or OPENAI_DEFAULT_MODEL

    if not api_key:
        if normalized == "auto":
            return MockTravelLLMClient()
        raise RuntimeError("真实 LLM 模式需要在 .env 中配置 OPENAI_API_KEY。")

    return OpenAICompatibleClient(model=model, api_key=api_key, base_url=base_url)


def _extract_city(prompt: str) -> str:
    for city in ["北京", "上海", "杭州", "厦门", "广州", "深圳", "成都", "南京", "西安"]:
        if city in prompt:
            return city
    return "北京"


def _extract_weather(prompt: str) -> str:
    matches = re.findall(r"当前天气[:：]([^，。\n]+)", prompt)
    if matches:
        return matches[-1].strip()
    return "晴天"


def _extract_last_observation(prompt: str) -> str:
    observations = re.findall(r"Observation:\s*(.+)", prompt)
    if observations:
        return observations[-1].strip()
    return "推荐去当地代表性景点，并根据天气灵活安排行程。"
