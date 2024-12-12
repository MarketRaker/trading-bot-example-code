from fastapi import FastAPI
from decouple import config

from app.routers import Binance_Routers, MarketRaker_Routers, ByBit_Routers


# Initialize FastAPI app
app = FastAPI()
app.include_router(Binance_Routers.router, prefix="/binance", tags=["Binance"])
app.include_router(
    MarketRaker_Routers.router, prefix="/marketraker", tags=["MarketRaker"]
)
app.include_router(ByBit_Routers.router, prefix="/bybit", tags=["Bybit"])
