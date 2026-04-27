from first_agent.agent import TravelAgent
from first_agent.llm_client import MockTravelLLMClient
from first_agent.prompts import DEFAULT_USER_PROMPT


def test_mock_agent_completes_travel_loop() -> None:
    agent = TravelAgent(
        llm=MockTravelLLMClient(),
        tools={
            "get_weather": lambda city: f"{city}当前天气:Sunny，气温26摄氏度",
            "get_attraction": lambda city, weather: f"{city}在{weather}适合去颐和园。",
        },
    )

    result = agent.run(DEFAULT_USER_PROMPT, verbose=False)

    assert result.completed is True
    assert "北京" in result.final_answer
    assert "颐和园" in result.final_answer
    assert any("Observation:" in item for item in result.history)
