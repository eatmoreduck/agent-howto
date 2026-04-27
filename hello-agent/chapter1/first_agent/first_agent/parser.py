import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ToolAction:
    name: str
    kwargs: dict[str, str]


@dataclass(frozen=True)
class FinishAction:
    answer: str


@dataclass(frozen=True)
class AgentStep:
    thought: str
    action: ToolAction | FinishAction


def truncate_to_first_step(output: str) -> str:
    """Keep only the first Thought-Action pair if a model returns extra text."""

    match = re.search(
        r"(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)",
        output,
        re.DOTALL,
    )
    return match.group(1).strip() if match else output.strip()


def parse_llm_output(output: str) -> AgentStep:
    text = truncate_to_first_step(output)
    match = re.search(r"Thought:\s*(.*?)\s*Action:\s*(.*)", text, re.DOTALL)
    if not match:
        raise ValueError("未能解析到 Thought 和 Action。")

    thought = match.group(1).strip()
    action_text = match.group(2).strip().splitlines()[0].strip()

    finish_match = re.fullmatch(r"Finish\[(.*)\]", action_text)
    if finish_match:
        return AgentStep(thought=thought, action=FinishAction(answer=finish_match.group(1)))

    tool_match = re.fullmatch(r"(\w+)\((.*)\)", action_text)
    if not tool_match:
        raise ValueError(f"Action 格式不合法: {action_text}")

    tool_name = tool_match.group(1)
    args_text = tool_match.group(2)
    kwargs = dict(re.findall(r"""(\w+)\s*=\s*["']([^"']*)["']""", args_text))
    return AgentStep(thought=thought, action=ToolAction(name=tool_name, kwargs=kwargs))
