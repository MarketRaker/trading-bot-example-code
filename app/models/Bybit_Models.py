from pydantic import BaseModel
from typing import Optional


class CoinType(BaseModel):
    coin:Optional[str] = None

class SymbolType(BaseModel):
    symbol:Optional[str] = None

class PlaceOrderRequest(BaseModel):
    category:str
    symbol: str
    side: str
    orderType: str
    qty: str
    price: Optional[str] = None
    timeInForce: Optional[str] = None
    orderLinkId: Optional[str] = None
    isLeverage: Optional[int] = None
    orderFilter: Optional[str] = None

class CancelOrder(BaseModel):
    category:str
    symbol:str
    orderId:Optional[str]=None
    orderLinkId:Optional[str]=None

class GetOrders(BaseModel):
    category: str
    symbol:Optional[str]=None
    baseCoin:Optional[str]=None
    orderId:Optional[str]=None
    orderLinkId:Optional[str]=None
    openOnly:Optional[int]=None
    limit:Optional[int]=None

class AmendOrder(BaseModel):
    category: str
    symbol: str
    orderId: Optional[str]=None
    orderLinkId: Optional[str]=None
    triggerPrice: Optional[str]=None
    qty: Optional[str]=None
    price:  Optional[str]=None
    takeProfit: Optional[str]=None
    stopLoss: Optional[str]=None

class MarketPriceTicker(BaseModel):
    category:str
    symbol: Optional[str]=None

class GetKline(BaseModel):
    category:Optional[str]=None
    symbol:str
    interval:str
    start:Optional[int]=None
    end:Optional[int]=None
    limit:Optional[int]=None

class OrderBook(BaseModel):
    category:str
    symbol:str
    limit:Optional[int]=None

class RecentTrades(BaseModel):
    category:str
    symbol:Optional[str]=None
    limit:Optional[int]=None

class PositionInfo(BaseModel):
    category:str
    symbol:Optional[str]=None
    settleCoin:Optional[str]=None
    limit:Optional[int]=None
    cursor:Optional[str]=None

class SetLeverage(BaseModel):
    category:str
    symbol:str
    buyLeverage:str
    sellLeverage:str

class SwitchPositionMode(BaseModel):
    category:str
    symbol:Optional[str]=None
    coin:Optional[str]=None
    mode:int

class RiskLimit(BaseModel):
    category:str
    symbol:Optional[str]=None
    cursor:Optional[str]=None

class FundingRateHistory(BaseModel):
    category:str
    symbol:str
    startTime:Optional[int]=None
    endTime:Optional[int]=None
    limit:Optional[int]=None

class CoinExchangeRecord(BaseModel):
    fromCoin:Optional[str]=None
    toCOin:Optional[str]=None
    limit:Optional[int]=None
    cursor:Optional[str]=None




