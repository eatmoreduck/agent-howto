# agent-howto

这是一个 Agent 学习路线仓库，不是单个 demo 项目。

目标是按章节逐步沉淀 Agent 的核心概念、代码 demo 和练习记录。当前使用 `uv` 管理 Python 版本、依赖和验证命令。

## 项目结构

```text
agent-howto/
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── .env.example
├── .env                 # 本地私密文件，不提交
├── hello-agent/
│   ├── README.md
│   └── chapter1/
│       ├── README.md
│       └── first_agent/
│           ├── README.md
│           ├── run.py
│           └── first_agent/
│               ├── agent.py
│               ├── llm_client.py
│               ├── parser.py
│               ├── prompts.py
│               └── tools/
└── tests/
    ├── conftest.py
    ├── test_agent.py
    └── test_parser.py
```

## 学习路线

当前先按 Hello-Agents 的章节推进：

| 章节 | 主题 | 当前状态 |
| --- | --- | --- |
| Chapter 1 | 初识智能体，理解 Agent Loop 和 Thought-Action-Observation | 已有 demo |
| Chapter 2 | 智能体发展史 | 待补笔记 |
| Chapter 3 | 大语言模型基础 | 待补 demo |
| Chapter 4 | ReAct、Plan-and-Solve、Reflection | 待补 demo |
| Chapter 5+ | 低代码平台、框架实践、自研 Agent 框架等 | 后续扩展 |

## 当前 Demo

第一章 demo 放在：

```text
hello-agent/chapter1/first_agent/
```

它对应 Hello-Agents 1.3.1-1.3.4，实现一个最小“智能旅行助手”：

- 1.3.1：准备提示词和工具。
- 1.3.2：接入 LLM 客户端。
- 1.3.3：执行 `Thought -> Action -> Observation` 主循环。
- 1.3.4：观察完整运行过程。

运行：

```bash
uv run python hello-agent/chapter1/first_agent/run.py --mode mock
```

只看最终答案：

```bash
uv run python hello-agent/chapter1/first_agent/run.py --mode mock --quiet
```

## 真实 LLM 配置

本项目统一使用 OpenAI-compatible 接口：代码只依赖 `openai` Python SDK，不绑定某个厂商的专用 SDK。

你现在用的是智谱 GLM Coding Plan，同一个 key 在 Claude Code 能用，是因为 Claude Code 走的是智谱的编码套餐线路。这个项目仍然统一用 `openai` Python SDK，只是把 OpenAI-compatible `base_url` 指到智谱的 coding 线路：

```text
https://open.bigmodel.cn/api/coding/paas/v4/
```

推荐做法是只提交 `.env.example`，真实密钥只放本机 `.env`。

复制模板：

```bash
cp .env.example .env
```

然后只编辑 `.env`，不要把真实 key 写进 README、代码或 `.env.example`：

```bash
OPENAI_API_KEY=你的智谱 API Key
OPENAI_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4/
OPENAI_MODEL=glm-5.1
TAVILY_API_KEY=你的 Tavily Key
```

代码会用 `python-dotenv` 自动读取项目根目录 `.env`，所以通常不需要手动 `export`。如果你想临时用 shell 环境变量，也直接导出同名 `OPENAI_*` 变量。

注意：

- `https://open.bigmodel.cn/api/anthropic` 是 Claude/Anthropic 兼容接口，适合 Claude Code，不适合这里的 `openai` SDK Chat Completions 调用。
- `https://open.bigmodel.cn/api/coding/paas/v4/` 是 coding 场景的 OpenAI-compatible 地址，适合本项目和你的 Coding Plan。
- `https://open.bigmodel.cn/api/paas/v4/` 是普通开放平台 OpenAI-compatible 地址，会走普通账户余额或普通资源包。

然后运行：

```bash
uv run python hello-agent/chapter1/first_agent/run.py --mode real
```

没有真实密钥时，`--mode mock` 也能完整跑通学习流程。

安全规则：

- `.env` 放真实密钥，已经被 `.gitignore` 忽略。
- `.env.example` 只放变量名和默认配置，不放真实密钥。
- 不再使用 `ZAI_*`、`ZHIPU_*`、`API_KEY` 这类别名，统一用 `OPENAI_*`。
- 如果密钥已经提交过，应立即在智谱控制台删除或轮换该 Key。
- 终端截图、报错日志、README、测试文件里都不要出现真实密钥。

## 验证

```bash
uv run pytest
uv run ruff check .
uv run mypy hello-agent/chapter1/first_agent tests
```

当前验证结果：

```text
pytest: 4 passed
ruff: All checks passed
mypy: Success, no issues found
```

## 参考

- [Hello-Agents 在线阅读](https://datawhalechina.github.io/hello-agents/)
- [Hello-Agents GitHub 仓库](https://github.com/datawhalechina/hello-agents)
- [智谱 AI OpenAI API 兼容文档](https://docs.bigmodel.cn/cn/guide/develop/openai/introduction)
