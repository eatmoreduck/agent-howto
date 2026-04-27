from collections.abc import Callable

from first_agent.tools.attraction import get_attraction
from first_agent.tools.weather import get_weather

available_tools: dict[str, Callable[..., str]] = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

__all__ = ["available_tools", "get_attraction", "get_weather"]
