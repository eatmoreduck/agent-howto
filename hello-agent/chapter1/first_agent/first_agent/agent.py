from collections.abc import Callable
from dataclasses import dataclass

from first_agent.llm_client import LLMClient
from first_agent.parser import FinishAction, ToolAction, parse_llm_output, truncate_to_first_step
from first_agent.prompts import AGENT_SYSTEM_PROMPT
from first_agent.tools import available_tools


@dataclass(frozen=True)
class AgentResult:
    final_answer: str
    history: list[str]
    completed: bool


class TravelAgent:
    """A minimal Thought-Action-Observation travel agent."""

    def __init__(
        self,
        llm: LLMClient,
        tools: dict[str, Callable[..., str]] | None = None,
        system_prompt: str = AGENT_SYSTEM_PROMPT,
    ) -> None:
        self.llm = llm
        self.tools: dict[str, Callable[..., str]] = tools or available_tools
        self.system_prompt = system_prompt

    def run(self, user_prompt: str, max_steps: int = 5, verbose: bool = True) -> AgentResult:
        prompt_history = [f"用户请求: {user_prompt}"]
        self._print(verbose, f"用户输入: {user_prompt}\n" + "=" * 40)

        for index in range(max_steps):
            self._print(verbose, f"--- 循环 {index + 1} ---")
            full_prompt = "\n".join(prompt_history)
            llm_output = truncate_to_first_step(
                self.llm.generate(full_prompt, system_prompt=self.system_prompt)
            )
            self._print(verbose, f"模型输出:\n{llm_output}\n")
            prompt_history.append(llm_output)

            try:
                step = parse_llm_output(llm_output)
            except ValueError as exc:
                observation = f"错误: {exc} 请严格输出 Thought 和 Action。"
                prompt_history.append(f"Observation: {observation}")
                self._print(verbose, f"Observation: {observation}\n" + "=" * 40)
                continue

            if isinstance(step.action, FinishAction):
                self._print(verbose, f"任务完成，最终答案: {step.action.answer}")
                return AgentResult(
                    final_answer=step.action.answer,
                    history=prompt_history,
                    completed=True,
                )

            observation = self._execute_action(step.action)
            observation_text = f"Observation: {observation}"
            prompt_history.append(observation_text)
            self._print(verbose, f"{observation_text}\n" + "=" * 40)

        final_answer = "任务未在最大循环次数内完成。"
        return AgentResult(final_answer=final_answer, history=prompt_history, completed=False)

    def _execute_action(self, action: ToolAction) -> str:
        tool = self.tools.get(action.name)
        if tool is None:
            return f"错误:未定义的工具 '{action.name}'"

        try:
            return tool(**action.kwargs)
        except TypeError as exc:
            return f"错误:工具 '{action.name}' 参数不正确 - {exc}"
        except Exception as exc:
            return f"错误:工具 '{action.name}' 执行失败 - {exc}"

    @staticmethod
    def _print(verbose: bool, message: str) -> None:
        if verbose:
            print(message)
