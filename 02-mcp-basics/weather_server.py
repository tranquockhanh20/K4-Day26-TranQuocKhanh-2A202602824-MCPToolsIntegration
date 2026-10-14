"""MCP SERVER minh hoạ — công bố tool `get_weather` qua giao thức MCP.

Khác với function calling: tool nằm ở một server ĐỘC LẬP. Server tự "khai
báo" tool của mình; bất kỳ MCP client nào (Claude Code, Claude Desktop,
Cursor, hoặc weather_client.py) cũng cắm vào dùng được mà không cần biết
code bên trong.

Schema của tool được TỰ ĐỘNG sinh ra từ type hints + docstring.

Chạy trực tiếp:
    pip install -r ../requirements.txt
    python weather_server.py

Đăng ký với Claude Code (làm 1 lần, dùng mãi):
    claude mcp add weather -- python /đường/dẫn/tới/weather_server.py
"""

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("weather")

_MOCK_DB = {
    "Hanoi": "29°C, trời mưa",
    "Haiphong": "33°C, mưa rào",
    "Danang": "30°C, nhiều mây",
}


@mcp.tool()
def get_weather(city: str) -> str:
    """Lấy thời tiết hiện tại của một thành phố."""
    return f"{city}: {_MOCK_DB.get(city, '28°C, không có dữ liệu chi tiết')}"


_MOCK_FORECAST = {
    "Hanoi": [
        "Ngày 1: 30°C, nắng nhẹ",
        "Ngày 2: 28°C, mưa dông",
        "Ngày 3: 27°C, nhiều mây",
    ],
    "Danang": [
        "Ngày 1: 31°C, trời nắng",
        "Ngày 2: 32°C, nắng nóng",
        "Ngày 3: 30°C, có mây",
    ],
    "Haiphong": [
        "Ngày 1: 32°C, nhiều mây",
        "Ngày 2: 31°C, mưa rào",
        "Ngày 3: 29°C, gió nhẹ",
    ],
}


@mcp.tool()
def get_forecast(city: str, days: int = 2) -> str:
    """Dự báo thời tiết N ngày tới cho một thành phố.

    Args:
        city: Tên thành phố (Hanoi, Danang, Haiphong)
        days: Số ngày dự báo, 1-3 (mặc định 2)
    """
    days = max(1, min(days, 3))
    forecasts = _MOCK_FORECAST.get(
        city,
        [f"Ngày {i+1}: 28°C, thời tiết ổn định" for i in range(days)],
    )
    selected = forecasts[:days]
    return f"{city} ({days} ngày tới): " + " | ".join(selected)


if __name__ == "__main__":
    mcp.run()  # mặc định chạy qua stdio
