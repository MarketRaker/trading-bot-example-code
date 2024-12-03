from fastapi import FastAPI
from pydantic import BaseModel, Field
import requests
from datetime import datetime
from typing import Literal

from app.routers import Binance_Routers, MarketRaker_Routers, ByBit_Routers


# Initialize FastAPI app
app = FastAPI()
app.include_router(Binance_Routers.router, prefix="/binance", tags=["Binance"])  # check the useability of (binance.router, prefix="/binance", tags=["Binance"])
app.include_router(MarketRaker_Routers.router)  # maby add a similar tag/ prefix same as Binance
app.include_router(ByBit_Routers.router, prefix="/bybit", tags=["Bybit"])


################################################################## Development--- REMOVE when going public
class Webhook_Format(BaseModel):
    trading_type: Literal["Long", "Short"]
    leverage: int = Field(..., ge=1, le=5)
    buy_price: float
    sell_price: float
    buy_date: datetime
    sell_prediction_date: datetime
    risk: int
    market_direction: Literal["Bull", "Bear"]
    percentage_change: float
    stoploss: int | None
    trading_type_24h: Literal["Long", "Short"] | None
    percentage_change_24h: float | None
    risk_24h: int | None
    leverage_24h: int | None
    stoploss_24h: int | None

def get_indicator():
    indicator: dict = {
        "trading_pair": "Solana",
        "currency": "SOL/USD",
        "leverage": 1,
        "action": "Long",
        "market_direction": "Bear",
        "entry_price": 208.48,
        "exit_price": 217.94017,
        "time": "2024-11-15T06:00:00",
        "img_src": "https://altcoinsbox.com/wp-content/uploads/2023/01/solana-logo.png",
        "risk": 4,
        "leverage_24h": 1,
        "risk_24h": 9,
        "percentage_change": 4.5376897,
        "percentage_change_24h": 0.72380304,
        "stoploss": 11,
        "stoploss_24h": 11,
        "valid_trade": None,
        "trade_closed": None,
        "trade_closed_window_number": None,
    }
    return indicator


@app.get("/test")
def testNotification():

    # Base URL for the notification backend
    NOTIFICATION_BACKEND_URL = "http://localhost:8000"

    # Endpoint URL
    request_url = f"{NOTIFICATION_BACKEND_URL}/users/notifications"

    # Example payload
    notification_payload = Webhook_Format(
        trading_type="Long",
        leverage=3,
        buy_price=1500.0,
        sell_price=1600.0,
        buy_date=datetime(2024, 11, 26, 10, 0, 0),
        sell_prediction_date=datetime(2024, 11, 27, 10, 0, 0),
        risk=4,
        market_direction="Bull",
        percentage_change=6.67,
        stoploss=1450,
        trading_type_24h="Short",
        percentage_change_24h=-3.45,
        risk_24h=7,
        leverage_24h=2,
        stoploss_24h=1420,
    )

    token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhaaTEtWF9wNlBJY19OLVZJNGYzYiJ9.eyJnaXZlbl9uYW1lIjoiRnJhbmNvIiwiZmFtaWx5X25hbWUiOiJLb2VrZW1vZXIiLCJuaWNrbmFtZSI6ImZyYW5jby5rb2VrZW1vZXIiLCJuYW1lIjoiRnJhbmNvIEtvZWtlbW9lciIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMa3gwcDRpRGtjTWhxN0hkT1ZVQ1NnYkFjejNhVGpscDNnc0I5TmJid3dSVGx0aFhNPXM5Ni1jIiwidXBkYXRlZF9hdCI6IjIwMjQtMTEtMjdUMDg6MzU6NDYuNTExWiIsImVtYWlsIjoiZnJhbmNvLmtvZWtlbW9lckBwb3RjaC5tYXRvZ2VuLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczovL21hcmtldHJha2VyLmV1LmF1dGgwLmNvbS8iLCJhdWQiOiJPSUdwYjdmelRPV1ZtSkpyU2hDODh4NUp0RXVaV3pDRiIsImlhdCI6MTczMjY5NjU1MCwiZXhwIjoxNzMyNjk2NjEwLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMDU3ODkxNjQxMTQwMTIyMDMyNSIsInNpZCI6IjF0VGJ6UUhUUGkxQ2FXVG9VS0dwbFQzNlczQ3RBcTEtIiwibm9uY2UiOiJTVGRZUTJGUVNVeE5hWEpOVDB4cVJsVlVOR0pETFROSU9EaFpkWHBmTGtaTVoyWkpNbXB3UTNkQllRPT0ifQ.Ev4pKHrZ77z7Ju5x4m89ko_75Ia8S26iNV_98CX_I5sGguvp1R33NloVFaKwHJlLSvrmna2nJVwcQPCtOG6JHSE31VPkbNim8-uuDvyEAd-tiUsSWH0LxwTmog_md8rRHWnInNEC7ULnq4i2d7zT29KKug02ZuCMDTds-VV9yNFi3siqxQJQp7_YFV8Br2pvyBa8D3pvytcY0BKpZNQT2X8vhMgWDB0c_Zhz2_T4rGvEY-6tQ-sttWdVyTLYdGb2qch0Dmao_8gjRxPEdTfN_D3CoZGZMs9Uuav4BmyAdk6HvyVyfwUeQJseKGLpn9RndjY-qU-4RJMh3aKErVO4yQ"

    # Headers (add authentication token if required)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"bearer {token}",  # Add the required token if needed
    }
    notification_payload_json = notification_payload.json()
    # Make the POST request
    response = requests.post(
        url=request_url, data=notification_payload_json, headers=headers
    )

    # Check the response
    if response.status_code == 200:
        return {
            "message": "Notification sent successfully",
            "response": response.json(),
        }
    else:
        return {"error": "Failed to send notification", "response": response.json()}


################################################################### End of Development Section

