# First Agent: 智能旅行助手

这是第一章 1.3 的动手 demo：用 `Thought -> Action -> Observation` 循环实现一个最小智能旅行助手。

用户输入：

```text
你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。
```

Agent 会做三步：

1. `get_weather(city="北京")`
2. `get_attraction(city="北京", weather="...")`
3. `Finish[最终答案]`

运行 mock 模式：

```bash
uv run python hello-agent/chapter1/first_agent/run.py --mode mock
```

只看最终答案：

```bash
uv run python hello-agent/chapter1/first_agent/run.py --mode mock --quiet
```

真实 LLM 模式需要先配置环境变量：

```bash
cp .env.example .env
```

在项目根目录 `.env` 里填 OpenAI-compatible 配置。这里以智谱 AI 为例：

```bash
OPENAI_API_KEY=你的智谱 API Key
OPENAI_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4/
OPENAI_MODEL=glm-5.1
TAVILY_API_KEY=
```

代码会自动读取根目录 `.env`，不需要把 key 写到代码里，也不需要提交 `.env`。

不要使用 `https://open.bigmodel.cn/api/anthropic`，它是 Anthropic 兼容接口，不适合这个 demo 的 `openai` SDK 调用。

如果你使用的是普通开放平台余额或普通资源包，可以把 `OPENAI_BASE_URL` 改成：

```text
https://open.bigmodel.cn/api/paas/v4/
```

然后运行：

```bash
uv run python hello-agent/chapter1/first_agent/run.py --mode real
```

文件对应：

- `first_agent/prompts.py`：系统提示词。
- `first_agent/llm_client.py`：mock LLM 和 OpenAI-compatible LLM。
- `first_agent/tools/weather.py`：天气工具。
- `first_agent/tools/attraction.py`：景点推荐工具。
- `first_agent/parser.py`：解析 `Action`。
- `first_agent/agent.py`：主循环。
