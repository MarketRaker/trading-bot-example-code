from pydantic import BaseModel
from typing import Optional


class PlaceOrderRequest(BaseModel):
    symbol: str
    side: str
    qty: str
    category:str
    orderType: str = "Market"

