import os


def get_attraction(city: str, weather: str) -> str:
    """Recommend attractions using Tavily when configured, otherwise use local samples."""

    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return _local_recommendation(city, weather)

    try:
        from tavily import TavilyClient

        tavily = TavilyClient(api_key=api_key)
        query = f"'{city}' 在'{weather}'天气下最值得去的旅游景点推荐及理由"
        response = tavily.search(query=query, search_depth="basic", include_answer=True)
    except Exception as exc:
        return f"{_local_recommendation(city, weather)}（Tavily 调用失败:{exc}）"

    if response.get("answer"):
        return str(response["answer"])

    formatted_results = [
        f"- {result['title']}: {result['content']}"
        for result in response.get("results", [])
        if "title" in result and "content" in result
    ]
    if not formatted_results:
        return _local_recommendation(city, weather)
    return "根据搜索，为您找到以下信息:\n" + "\n".join(formatted_results)


def _local_recommendation(city: str, weather: str) -> str:
    if "rain" in weather.lower() or "雨" in weather:
        indoor = {
            "北京": "中国国家博物馆",
            "上海": "上海博物馆",
            "杭州": "浙江省博物馆",
            "厦门": "华侨博物院",
        }.get(city, "当地博物馆")
        return f"{city}当前天气不太适合长时间户外活动，推荐去{indoor}，行程更稳妥。"

    outdoor = {
        "北京": "颐和园",
        "上海": "外滩",
        "杭州": "西湖",
        "厦门": "鼓浪屿",
    }.get(city, "当地代表性景点")
    return f"{city}在{weather}天气下适合户外游览，推荐去{outdoor}，体验城市风景和文化。"
