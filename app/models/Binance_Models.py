from pydantic import BaseModel
from typing import Optional

### Market Data
class AvgPriceRequest(BaseModel):
    symbol: str

class OrderBookRequest(BaseModel):
    symbol: str
    limit: int = 100  # Default is 100; acceptable values are 5, 10, 20, 50, 100, 500, 1000, 5000; Optional

class PriceTickerRequest(BaseModel):
    symbol: str

class PriceChangeStatsRequest(BaseModel):
    symbol: str

class HistoricalTradesRequest(BaseModel):
    symbol: str
    limit: int = 500  # Default is 500; max is 1000
    fromId: int = None  # Trade ID to fetch from (optional)

### Placing and Managing orders
class OrderRequest(BaseModel):
    symbol: str
    side: str
    quantity: float
    '''
    "symbol": "BTCUSDT",
    "side": "BUY",
    "quantity": 0.01
    '''

class OrderDetailsRequest(BaseModel):
    symbol: str
    orderId: int = None
    clientOrderId: str = None


class cancelOrder(BaseModel):
    symbol: str
    orderId: int = None
    clientOrderId: str = None

### Advanced Trading
# Margin and Futures trading
class FuturesOrderRequest(BaseModel):
    symbol: str  # Trading pair (e.g., "BTCUSDT")
    side: str  # "BUY" or "SELL"
    type: str  # e.g., "LIMIT", "MARKET"
    quantity: float  # Quantity to buy/sell
    price: Optional[float] = None  # Required for LIMIT orders
    time_in_force: Optional[str] = "GTC"  # Good Till Canceled (for LIMIT orders)

class CancelFuturesOrderRequest(BaseModel):
    symbol: str  # Trading pair (e.g., "BTCUSDT")
    order_id: Optional[int] = None  # Binance order ID
    orig_client_order_id: Optional[str] = None  # Client order ID (optional)

class FuturesOrderHistoryRequest(BaseModel):
    symbol: str  # Trading pair (e.g., "BTCUSDT")
    start_time: Optional[int] = None  # Start time for the query (timestamp in ms)
    end_time: Optional[int] = None  # End time for the query (timestamp in ms)
    limit: Optional[int] = 500  # Number of orders to retrieve (default is 500, max is 1000)


# Trading History & Information
class AllOrders(BaseModel):
    symbol: str
    '''
    "symbol": "BTCUSDT"
    '''

class RecentTradesRequest(BaseModel):
    symbol: str
    limit: int = 500  # Default is 500, max is 1000

# User Data Stream
class ListenKeyRequest(BaseModel):
    listenKey: str

# websocket
class SymbolType(BaseModel):
    symbol:str

### Useful Tools
class OCOOrderRequest(BaseModel):
    symbol: str
    side: str  # 'BUY' or 'SELL'
    quantity: float
    price: float
    stopPrice: float
    stopLimitPrice: float
    stopLimitTimeInForce: str  # GTC, FOK, IOC
    listClientOrderId: str  # Optional client-specific ID for the OCO order



