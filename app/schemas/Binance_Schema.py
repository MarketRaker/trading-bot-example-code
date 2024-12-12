from pydantic import BaseModel
from typing import Optional


### Market Data
class AvgPriceRequest(BaseModel):
    """
    Request to get the average price of a symbol.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
    """

    symbol: str


class OrderBookRequest(BaseModel):
    """
    Request to get the order book for a symbol.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        limit (int): The maximum number of order book levels to retrieve. Default is 100.
          Acceptable values are 5, 10, 20, 50, 100, 500, 1000, 5000.
    """

    symbol: str
    limit: int = (
        100  # Default is 100; acceptable values are 5, 10, 20, 50, 100, 500, 1000, 5000; Optional
    )


class PriceTickerRequest(BaseModel):
    """
    Request to get the latest price ticker for a symbol.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
    """

    symbol: str


class PriceChangeStatsRequest(BaseModel):
    """
    Request to get the price change statistics for a symbol.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
    """

    symbol: str


class HistoricalTradesRequest(BaseModel):
    """
    Request to get historical trade data for a symbol.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        limit (int): The maximum number of trades to retrieve. Default is 500, max is 1000.
        fromId (int): The trade ID to start from. Optional.
    """

    symbol: str
    limit: int = 500  # Default is 500; max is 1000
    fromId: int = None  # Trade ID to fetch from (optional)


### Placing and Managing Orders
class OrderRequest(BaseModel):
    """
    Request to place an order for a symbol.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        side (str): The side of the order, either "BUY" or "SELL".
        quantity (float): The quantity of the asset to be bought or sold.
    """

    symbol: str
    side: str
    quantity: float


class OrderDetailsRequest(BaseModel):
    """
    Request to get the details of a specific order.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        orderId (int): The ID of the order. Optional.
        clientOrderId (str): The client-specific ID of the order. Optional.
    """

    symbol: str
    orderId: int = None
    clientOrderId: str = None


class CancelOrder(BaseModel):
    """
    Request to cancel an order.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        orderId (int): The ID of the order to cancel. Optional.
        clientOrderId (str): The client-specific ID of the order to cancel. Optional.
    """

    symbol: str
    orderId: int = None
    clientOrderId: str = None


### Advanced Trading
# Margin and Futures Trading
class FuturesOrderRequest(BaseModel):
    """
    Request to place a futures order for a symbol.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        side (str): The side of the order, either "BUY" or "SELL".
        type (str): The type of the order, e.g., "LIMIT" or "MARKET".
        quantity (float): The quantity of the asset to be bought or sold.
        price (Optional[float]): The price for a LIMIT order. Optional.
        time_in_force (Optional[str]): The time in force for the order, default is "GTC" (Good Till Canceled).
    """

    symbol: str
    side: str
    type: str
    quantity: float
    price: Optional[float] = None
    time_in_force: Optional[str] = "GTC"


class CancelFuturesOrderRequest(BaseModel):
    """
    Request to cancel a futures order.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        order_id (Optional[int]): The Binance order ID to cancel.
        orig_client_order_id (Optional[str]): The client-specific order ID to cancel.
    """

    symbol: str
    order_id: Optional[int] = None
    orig_client_order_id: Optional[str] = None


class FuturesOrderHistoryRequest(BaseModel):
    """
    Request to get the order history for futures trades.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        start_time (Optional[int]): The start time for the query, in milliseconds. Optional.
        end_time (Optional[int]): The end time for the query, in milliseconds. Optional.
        limit (Optional[int]): The maximum number of orders to retrieve. Default is 500, max is 1000.
    """

    symbol: str
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    limit: Optional[int] = 500  # Default is 500, max is 1000


# Trading History & Information
class AllOrders(BaseModel):
    """
    Request to get all orders for a symbol.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
    """

    symbol: str


class RecentTradesRequest(BaseModel):
    """
    Request to get recent trades for a symbol.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        limit (int): The maximum number of trades to retrieve. Default is 500, max is 1000.
    """

    symbol: str
    limit: int = 500  # Default is 500, max is 1000


# User Data Stream
class ListenKeyRequest(BaseModel):
    """
    Request to get a listen key for a user data stream.

    Attributes:
        listenKey (str): The listen key for the user data stream.
    """

    listenKey: str


# WebSocket
class SymbolType(BaseModel):
    """
    Request to get symbol information for a WebSocket connection.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
    """

    symbol: str


### Useful Tools
class OCOOrderRequest(BaseModel):
    """
    Request to place an OCO (One Cancels Other) order.

    Attributes:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        side (str): The side of the order, either "BUY" or "SELL".
        quantity (float): The quantity of the asset to be bought or sold.
        price (float): The price for the primary order.
        stopPrice (float): The stop price for the OCO order.
        stopLimitPrice (float): The stop limit price for the OCO order.
        stopLimitTimeInForce (str): The time in force for the stop limit order, e.g., "GTC", "FOK", or "IOC".
        listClientOrderId (str): Optional client-specific ID for the OCO order.
    """

    symbol: str
    side: str
    quantity: float
    price: float
    stopPrice: float
    stopLimitPrice: float
    stopLimitTimeInForce: str  # GTC, FOK, IOC
    listClientOrderId: str  # Optional client-specific ID for the OCO order
