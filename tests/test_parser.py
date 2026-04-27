from first_agent.parser import FinishAction, ToolAction, parse_llm_output, truncate_to_first_step


def test_parse_tool_action() -> None:
    step = parse_llm_output(
        'Thought: 我需要查天气。\nAction: get_weather(city="北京")'
    )

    assert step.thought == "我需要查天气。"
    assert step.action == ToolAction(name="get_weather", kwargs={"city": "北京"})


def test_parse_finish_action() -> None:
    step = parse_llm_output("Thought: 已经完成。\nAction: Finish[推荐去颐和园。]")

    assert step.action == FinishAction(answer="推荐去颐和园。")


def test_truncate_to_first_step() -> None:
    output = (
        'Thought: 第一步。\nAction: get_weather(city="北京")\n'
        'Thought: 多余内容。\nAction: Finish[不应该保留]'
    )

    assert truncate_to_first_step(output) == 'Thought: 第一步。\nAction: get_weather(city="北京")'
