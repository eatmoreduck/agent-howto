import argparse

from first_agent.agent import TravelAgent
from first_agent.llm_client import build_llm_client
from first_agent.prompts import DEFAULT_USER_PROMPT


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Chapter 1.3 travel agent demo.")
    parser.add_argument("--prompt", default=DEFAULT_USER_PROMPT, help="用户请求")
    parser.add_argument("--max-steps", type=int, default=5, help="Agent 最大循环次数")
    parser.add_argument(
        "--mode",
        choices=["mock", "auto", "real"],
        default="mock",
        help="mock 不需要密钥；real 使用 OpenAI-compatible API；auto 有密钥则 real，否则 mock",
    )
    parser.add_argument("--quiet", action="store_true", help="只输出最终结果")
    args = parser.parse_args()

    llm = build_llm_client(mode=args.mode)
    agent = TravelAgent(llm=llm)
    result = agent.run(args.prompt, max_steps=args.max_steps, verbose=not args.quiet)

    if args.quiet:
        print(result.final_answer)


if __name__ == "__main__":
    main()
