from pydantic import BaseModel
from typing import Optional


class CoinType(BaseModel):
    """
    Request to define a coin type.

    Attributes:
        coin (Optional[str]): The name of the coin, if provided (e.g., "BTC").
    """

    coin: Optional[str] = None


class SymbolType(BaseModel):
    """
    Request to define a symbol type.

    Attributes:
        symbol (Optional[str]): The trading pair symbol, if provided (e.g., "BTCUSDT").
    """

    symbol: Optional[str] = None


class PlaceOrderRequest(BaseModel):
    """
    Request to place an order for a symbol.

    Attributes:
        category (str): The category of the order.
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        side (str): The side of the order, either "BUY" or "SELL".
        orderType (str): The type of the order, e.g., "LIMIT", "MARKET".
        qty (str): The quantity to buy or sell.
        price (Optional[str]): The price of the order for limit orders. Optional.
        timeInForce (Optional[str]): The time in force for the order (e.g., "GTC"). Optional.
        orderLinkId (Optional[str]): A client-specific order link ID. Optional.
        isLeverage (Optional[int]): Indicates whether leverage is used (1 for leverage, 0 for no leverage). Optional.
        orderFilter (Optional[str]): Filter for order details. Optional.
    """

    category: str
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
    """
    Request to cancel an order.

    Attributes:
        category (str): The category of the order.
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        orderId (Optional[str]): The unique ID of the order to be canceled. Optional.
        orderLinkId (Optional[str]): The client-specific order link ID to cancel. Optional.
    """

    category: str
    symbol: str
    orderId: Optional[str] = None
    orderLinkId: Optional[str] = None


class GetOrders(BaseModel):
    """
    Request to retrieve orders for a symbol.

    Attributes:
        category (str): The category of the orders.
        symbol (Optional[str]): The trading pair symbol to retrieve orders for. Optional.
        baseCoin (Optional[str]): The base coin for filtering orders. Optional.
        orderId (Optional[str]): The specific order ID to retrieve. Optional.
        orderLinkId (Optional[str]): The client-specific order link ID to retrieve. Optional.
        openOnly (Optional[int]): If set to 1, only open orders are retrieved. Optional.
        limit (Optional[int]): The number of orders to retrieve. Optional.
    """

    category: str
    symbol: Optional[str] = None
    baseCoin: Optional[str] = None
    orderId: Optional[str] = None
    orderLinkId: Optional[str] = None
    openOnly: Optional[int] = None
    limit: Optional[int] = None


class AmendOrder(BaseModel):
    """
    Request to amend an existing order.

    Attributes:
        category (str): The category of the order.
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        orderId (Optional[str]): The ID of the order to amend. Optional.
        orderLinkId (Optional[str]): The client-specific order link ID of the order to amend. Optional.
        triggerPrice (Optional[str]): The new trigger price for the order. Optional.
        qty (Optional[str]): The new quantity of the asset. Optional.
        price (Optional[str]): The new price for the order. Optional.
        takeProfit (Optional[str]): The new take profit price. Optional.
        stopLoss (Optional[str]): The new stop loss price. Optional.
    """

    category: str
    symbol: str
    orderId: Optional[str] = None
    orderLinkId: Optional[str] = None
    triggerPrice: Optional[str] = None
    qty: Optional[str] = None
    price: Optional[str] = None
    takeProfit: Optional[str] = None
    stopLoss: Optional[str] = None


class MarketPriceTicker(BaseModel):
    """
    Request to get the market price ticker for a symbol.

    Attributes:
        category (str): The category of the ticker.
        symbol (Optional[str]): The trading pair symbol (e.g., "BTCUSDT"). Optional.
    """

    category: str
    symbol: Optional[str] = None


class GetKline(BaseModel):
    """
    Request to get Kline (candlestick) data for a symbol.

    Attributes:
        category (Optional[str]): The category of the Kline data. Optional.
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        interval (str): The interval for the Kline data (e.g., "1m", "5m", "1h").
        start (Optional[int]): The start time for the Kline data (timestamp in milliseconds). Optional.
        end (Optional[int]): The end time for the Kline data (timestamp in milliseconds). Optional.
        limit (Optional[int]): The number of Kline data points to retrieve. Optional.
    """

    category: Optional[str] = None
    symbol: str
    interval: str
    start: Optional[int] = None
    end: Optional[int] = None
    limit: Optional[int] = None


class OrderBook(BaseModel):
    """
    Request to get the order book for a symbol.

    Attributes:
        category (str): The category of the order book.
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        limit (Optional[int]): The number of order book levels to retrieve. Optional.
    """

    category: str
    symbol: str
    limit: Optional[int] = None


class RecentTrades(BaseModel):
    """
    Request to get recent trades for a symbol.

    Attributes:
        category (str): The category of the recent trades.
        symbol (Optional[str]): The trading pair symbol (e.g., "BTCUSDT"). Optional.
        limit (Optional[int]): The number of trades to retrieve. Optional.
    """

    category: str
    symbol: Optional[str] = None
    limit: Optional[int] = None


class PositionInfo(BaseModel):
    """
    Request to get position information for a symbol.

    Attributes:
        category (str): The category of the position.
        symbol (Optional[str]): The trading pair symbol (e.g., "BTCUSDT"). Optional.
        settleCoin (Optional[str]): The coin used for settlement. Optional.
        limit (Optional[int]): The limit on the number of positions to retrieve. Optional.
        cursor (Optional[str]): The cursor for pagination. Optional.
    """

    category: str
    symbol: Optional[str] = None
    settleCoin: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


class SetLeverage(BaseModel):
    """
    Request to set leverage for a symbol.

    Attributes:
        category (str): The category of the leverage settings.
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        buyLeverage (str): The leverage for buy orders.
        sellLeverage (str): The leverage for sell orders.
    """

    category: str
    symbol: str
    buyLeverage: str
    sellLeverage: str


class SwitchPositionMode(BaseModel):
    """
    Request to switch position mode for a symbol.

    Attributes:
        category (str): The category of the position mode.
        symbol (Optional[str]): The trading pair symbol (e.g., "BTCUSDT"). Optional.
        coin (Optional[str]): The coin for which the position mode is being switched. Optional.
        mode (int): The position mode to switch to (1 for hedge mode, 2 for one-way mode).
    """

    category: str
    symbol: Optional[str] = None
    coin: Optional[str] = None
    mode: int


class RiskLimit(BaseModel):
    """
    Request to get the risk limit for a symbol.

    Attributes:
        category (str): The category of the risk limit.
        symbol (Optional[str]): The trading pair symbol (e.g., "BTCUSDT"). Optional.
        cursor (Optional[str]): The cursor for pagination. Optional.
    """

    category: str
    symbol: Optional[str] = None
    cursor: Optional[str] = None


class FundingRateHistory(BaseModel):
    """
    Request to get the funding rate history for a symbol.

    Attributes:
        category (str): The category of the funding rate history.
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        startTime (Optional[int]): The start time for the funding rate history query (timestamp in milliseconds). Optional.
        endTime (Optional[int]): The end time for the funding rate history query (timestamp in milliseconds). Optional.
        limit (Optional[int]): The number of funding rates to retrieve. Optional.
    """

    category: str
    symbol: str
    startTime: Optional[int] = None
    endTime: Optional[int] = None
    limit: Optional[int] = None


class CoinExchangeRecord(BaseModel):
    """
    Request to get the coin exchange records.

    Attributes:
        fromCoin (Optional[str]): The coin to exchange from. Optional.
        toCOin (Optional[str]): The coin to exchange to. Optional.
        limit (Optional[int]): The number of records to retrieve. Optional.
        cursor (Optional[str]): The cursor for pagination. Optional.
    """

    fromCoin: Optional[str] = None
    toCOin: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None
