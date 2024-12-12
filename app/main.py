from fastapi import FastAPI
from pydantic import BaseModel, Field
import requests
from datetime import datetime
from typing import Literal
from decouple import config

from app.routers import Binance_Routers, MarketRaker_Routers, ByBit_Routers


# Initialize FastAPI app
app = FastAPI()
app.include_router(Binance_Routers.router, prefix="/binance", tags=["Binance"])
app.include_router(
    MarketRaker_Routers.router, prefix="/marketraker", tags=["MarketRaker"]
)
app.include_router(ByBit_Routers.router, prefix="/bybit", tags=["Bybit"])


################################################################## Development--- REMOVE when going public
NOTIFICATION_BACKEND_URL = str(config("API_URL"))
TOKEN = str(config("TOKEN"))


class Webhook_Format(BaseModel):
    trading_pair: str
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
    # category: None


@app.get("/test")
def testNotification():

    # Endpoint URL
    request_url = f"{NOTIFICATION_BACKEND_URL}/users/notifications/test"

    # Example payload
    notification_payload = Webhook_Format(
        trading_pair="SOL/USD",
        trading_type="Long",  # Long position (expecting price increase)
        leverage=1,  # Leverage between 1 and 5
        buy_price=205.0,  # A realistic buy price near 210
        sell_price=215.0,  # Target sell price after expected increase
        buy_date=datetime(2024, 12, 11, 10, 30, 0),  # Date and time of buying
        sell_prediction_date=datetime(
            2024, 12, 12, 10, 30, 0
        ),  # Predicted date and time of sell
        risk=4,  # Moderate risk level (6 out of 10)
        market_direction="Bull",  # Bullish sentiment (expecting price increase)
        percentage_change=5.1,  # Expected percentage increase of about 5%
        stoploss=200,  # A stop loss just below the buy price to minimize losses
        trading_type_24h="Short",  # Short position in the past 24 hours
        percentage_change_24h=-1.5,  # A slight decline in the last 24 hours (Bearish)
        risk_24h=5,  # Moderate risk in the last 24 hours
        leverage_24h=2,  # Lower leverage applied in the past 24 hours
        stoploss_24h=190,  # Stoploss for the short position in the last 24 hours
    )

    # Headers (add authentication token if required)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"bearer {TOKEN}",  # Add the required token if needed
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
