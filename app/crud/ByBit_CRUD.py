from decouple import config
from pybit.exceptions import InvalidRequestError
from pybit.unified_trading import HTTP
from app.schemas.Bybit_Schema import *
from pybit.unified_trading import WebSocket
from time import sleep
import asyncio


BYBIT_API_KEY = str(config("BYBIT_API_KEY"))
BYBIT_API_SECRET = str(config("BYBIT_API_SECRET"))
BYBIT_BASE_URL = str(config("BYBIT_BASE_URL"))

session = HTTP(
    testnet=True,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)

stop_event = asyncio.Event()


############################################################################### Account and Wallet Management:
async def get_account_info_f():
    """
    Retrieve the account information from Bybit.

    This function interacts with the Bybit API to fetch the account information.
    It handles exceptions such as `InvalidRequestError` to provide meaningful error messages.

    Returns:
        dict: The account information if the API call is successful.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        balance = session.get_account_info()
        return balance
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def get_wallet_balance_f(coin: CoinType):
    """
    Retrieve the unified account wallet balance for a specified coin from Bybit.

    This function interacts with the Bybit API to fetch the wallet balance
    from the unified account for a specific coin. It gracefully handles
    `InvalidRequestError` to provide meaningful error feedback in case of
    an invalid request.

    Args:
        coin:
            An instance of the `CoinType` class containing the
            optional coin symbol (e.g., "USDT"). If no coin is
            provided, the balance for all coins is returned.

    Returns:
        dict: The wallet balance data if the API call is successful.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        balance = session.get_wallet_balance(
            accountType="UNIFIED", coin=coin if coin else None
        )

        return balance
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def get_account_funding_f(coin: CoinType):
    """
    Retrieve the funding account balance for a specified coin from Bybit.

    This function interacts with the Bybit API to fetch the balance
    for a specific coin or all coins within the funding account.
    It handles `InvalidRequestError` exceptions gracefully, providing
    clear feedback when an error occurs.

    Args:
        coin:
            An instance of the `CoinType` class containing the
            optional coin symbol (e.g., "BTC"). If no coin is
            specified, the balance for all coins is retrieved.

    Returns:
        dict: The funding account balance data if the API call is successful.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        balance = session.get_coins_balance(
            accountType="FUND", coin=coin if coin else None
        )
        return balance
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def get_user_trading_fee_f(symbol: SymbolType):
    """
    Retrieve the trading fee rates for a specific symbol from Bybit.

    This function interacts with the Bybit API to fetch the trading fee rates
    associated with a specified symbol. If no symbol is provided, it fetches
    default fee rate information. It also handles `InvalidRequestError`
    exceptions, returning an error message if the request fails.

    Args:
        symbol:
            An instance of the `SymbolType` class containing the
            optional trading pair symbol (e.g., "BTCUSDT").
            If no symbol is provided, the function may retrieve
            default fee rates depending on API behavior.

    Returns:
        dict: The trading fee rates data if the API call is successful.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.get_fee_rates(symbol=symbol if symbol else None)

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


############################################################################### Order Management:
async def place_order_f(order: PlaceOrderRequest):
    """
    Place a new order on Bybit.

    This function sends a request to the Bybit API to create a new order based
    on the provided parameters. The order can include optional fields for
    advanced configurations such as price, time-in-force, and leverage settings.
    It gracefully handles `InvalidRequestError` exceptions, returning a descriptive
    error message when the request fails.

    Args:
        order:
            An instance of the `PlaceOrderRequest` class
            containing the required and optional parameters
            for placing an order. These include:
            - `category` (str): The category of the order (e.g., "linear", "spot").
            - `symbol` (str): The trading pair (e.g., "BTCUSDT").
            - `side` (str): The order side ("Buy" or "Sell").
            - `orderType` (str): The type of the order (e.g., "Limit", "Market").
            - `qty` (str): The quantity of the order.
            - `price` (Optional[str]): The price for limit orders (default is `None` for market orders).
            - `timeInForce` (Optional[str]): Time-in-force policy (e.g., "GTC" for "Good Till Canceled").
            - `orderLinkId` (Optional[str]): A unique identifier for the order (optional).
            - `isLeverage` (Optional[int]): Whether the order uses leverage (1 for true, 0 for false).
            - `orderFilter` (Optional[str]): Order filter for advanced configurations.

    Returns:
        dict: The response from the Bybit API if the order is placed successfully.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.place_order(
            category=order.category,
            symbol=order.symbol,
            side=order.side,
            orderType=order.orderType,
            qty=order.qty,
            price=order.price if order.price else None,
            timeInForce=order.timeInForce if order.price else None,
            orderLinkId=order.orderLinkId if order.price else None,
            isLeverage=order.isLeverage if order.price else None,
            orderFilter=order.orderFilter if order.price else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def cancel_order_f(cancelorder: CancelOrder):
    """
    Place a new order on Bybit.

    This function sends a request to the Bybit API to create a new order based
    on the provided parameters. The order can include optional fields for
    advanced configurations such as price, time-in-force, and leverage settings.
    It gracefully handles `InvalidRequestError` exceptions, returning a descriptive
    error message when the request fails.

    Args:
        order:
            An instance of the `PlaceOrderRequest` class
            containing the required and optional parameters
            for placing an order. These include:
            - `category` (str): The category of the order (e.g., "linear", "spot").
            - `symbol` (str): The trading pair (e.g., "BTCUSDT").
            - `side` (str): The order side ("Buy" or "Sell").
            - `orderType` (str): The type of the order (e.g., "Limit", "Market").
            - `qty` (str): The quantity of the order.
            - `price` (Optional[str]): The price for limit orders (default is `None` for market orders).
            - `timeInForce` (Optional[str]): Time-in-force policy (e.g., "GTC" for "Good Till Canceled").
            - `orderLinkId` (Optional[str]): A unique identifier for the order (optional).
            - `isLeverage` (Optional[int]): Whether the order uses leverage (1 for true, 0 for false).
            - `orderFilter` (Optional[str]): Order filter for advanced configurations.

    Returns:
        dict: The response from the Bybit API if the order is placed successfully.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.cancel_order(
            category=cancelorder.category,
            symbol=cancelorder.symbol,
            orderId=cancelorder.orderId if cancelorder.orderId else None,
            orderLinkId=cancelorder.orderLinkId if cancelorder.orderLinkId else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def get_orders_f(order: GetOrders):
    """
    Retrieve a list of open orders on Bybit.

    This function sends a request to the Bybit API to fetch open orders based on the
    provided parameters. It allows filtering of orders by various attributes like
    `symbol`, `baseCoin`, `orderId`, and more. If no specific filter is provided,
    it returns all open orders for the given category. The function gracefully handles
    `InvalidRequestError` exceptions, returning a descriptive error message when the request fails.

    Args:
        order:
            An instance of the `GetOrders` class containing the parameters
            for retrieving open orders. These include:
            - `category` (str): The category of the orders (e.g., "spot", "linear").
            - `symbol` (Optional[str]): The trading pair (e.g., "BTCUSDT").
            - `baseCoin` (Optional[str]): The base coin in the order (e.g., "BTC").
            - `orderId` (Optional[str]): The ID of the order to retrieve (optional).
            - `orderLinkId` (Optional[str]): A user-defined identifier for the order (optional).
            - `openOnly` (Optional[int]): Whether to retrieve only open orders (1 for true, 0 for false).
            - `limit` (Optional[int]): The number of orders to retrieve (default is no limit).

    Returns:
        dict: The response from the Bybit API if the orders are successfully retrieved.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.get_open_orders(
            category=order.category,
            symbol=order.symbol if order.symbol else None,
            baseCoin=order.baseCoin if order.baseCoin else None,
            orderId=order.orderId if order.orderId else None,
            orderLinkId=order.orderLinkId if order.orderLinkId else None,
            openOnly=order.openOnly if order.openOnly else None,
            limit=order.limit if order.limit else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def modify_order_f(order: AmendOrder):
    """
    Modify an existing order on Bybit.

    This function sends a request to the Bybit API to amend an existing order based
    on the provided parameters. You can modify various aspects of the order, including
    the price, quantity, stop-loss, and take-profit values. The function gracefully
    handles `InvalidRequestError` exceptions, returning a descriptive error message
    when the request fails.

    Args:
        order:
            An instance of the `AmendOrder` class containing the parameters
            for modifying an existing order. These include:
            - `category` (str): The category of the order (e.g., "spot", "linear").
            - `symbol` (str): The trading pair (e.g., "BTCUSDT").
            - `orderId` (Optional[str]): The ID of the order to be modified (optional).
            - `orderLinkId` (Optional[str]): A user-defined identifier for the order (optional).
            - `triggerPrice` (Optional[str]): The trigger price for conditional orders (optional).
            - `qty` (Optional[str]): The new quantity of the order (optional).
            - `price` (Optional[str]): The new price for the order (optional).
            - `takeProfit` (Optional[str]): The price at which to take profit (optional).
            - `stopLoss` (Optional[str]): The price at which to stop loss (optional).

    Returns:
        dict: The response from the Bybit API if the order is successfully modified.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.amend_order(
            category=order.category,
            symbol=order.symbol,
            orderId=order.orderId if order.orderId else None,
            orderLinkId=order.orderLinkId if order.orderLinkId else None,
            triggerPrice=order.triggerPrice if order.triggerPrice else None,
            qty=order.qty if order.qty else None,
            price=order.price if order.price else None,
            takeProfit=order.takeProfit if order.takeProfit else None,
            stopLoss=order.stopLoss if order.stopLoss else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


############################################################################### Market Data:
async def get_market_price_ticker_f(marketprice: MarketPriceTicker):
    """
    Retrieve the current market price for a given trading pair on Bybit.

    This function sends a request to the Bybit API to fetch the latest market price
    for a specified trading pair. It allows you to specify the market category and
    symbol, and returns the latest available market price data. The function gracefully
    handles `InvalidRequestError` exceptions, returning a descriptive error message
    when the request fails.

    Args:
        marketprice:
            An instance of the `MarketPriceTicker` class containing the parameters
            for fetching the market price ticker. These include:
            - `category` (str): The category of the market (e.g., "spot", "linear").
            - `symbol` (Optional[str]): The trading pair symbol (e.g., "BTCUSDT").

    Returns:
        dict: The response from the Bybit API, including the market price ticker data.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.get_tickers(
            category=marketprice.category,
            symbol=marketprice.symbol if marketprice.symbol else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def get_24_hour_price_change_f():
    try:
        response = session.get_fee_rates()

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def get_Kline_data_f(kline: GetKline):
    """
    Retrieve historical Kline (candlestick) data for a given trading pair.

    This function sends a request to the Bybit API to fetch historical Kline (candlestick)
    data for a specified trading pair. You can specify the interval, start and end times,
    and the number of data points to fetch. The function gracefully handles
    `InvalidRequestError` exceptions, returning a descriptive error message when the request fails.

    Args:
        kline:
            An instance of the `GetKline` class containing the parameters for fetching
            the Kline data. These include:
            - `category` (Optional[str]): The category of the market (e.g., "spot", "linear").
            - `symbol` (str): The trading pair symbol (e.g., "BTCUSDT").
            - `interval` (str): The Kline interval (e.g., "1m", "5m", "1h", etc.).
            - `start` (Optional[int]): The start time for the Kline data (in Unix timestamp).
            - `end` (Optional[int]): The end time for the Kline data (in Unix timestamp).
            - `limit` (Optional[int]): The number of Kline data points to retrieve (default is 200).

    Returns:
        dict: The response from the Bybit API, including the Kline data for the specified trading pair.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.get_kline(
            category=kline.category if kline.category else None,
            symbol=kline.symbol,
            interval=kline.interval,
            start=kline.start if kline.start else None,
            end=kline.end if kline.end else None,
            limit=kline.limit if kline.limit else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def get_symbol_order_book_f(orderbook: OrderBook):
    """
    Retrieve the order book for a given trading pair.

    This function sends a request to the Bybit API to fetch the order book for a specific
    trading pair. You can specify the category of the market and limit the number of
    order book entries returned. The function gracefully handles `InvalidRequestError`
    exceptions, returning a descriptive error message when the request fails.

    Args:
        orderbook:
            An instance of the `OrderBook` class containing the parameters for fetching
            the order book. These include:
            - `category` (str): The category of the market (e.g., "spot", "linear").
            - `symbol` (str): The trading pair symbol (e.g., "BTCUSDT").
            - `limit` (Optional[int]): The number of order book entries to retrieve (default is `None` for full order book).

    Returns:
        dict: The response from the Bybit API, including the order book for the specified trading pair.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.get_orderbook(
            category=orderbook.category,
            symbol=orderbook.symbol,
            limit=orderbook.limit if orderbook.limit else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def get_recent_trades_f(trades: RecentTrades):
    """
    Retrieve the recent trade history for a specific trading pair.

    This function sends a request to the Bybit API to fetch recent trade data for a
    specified trading pair. The user can specify the category of the market and limit
    the number of trade entries returned. The function gracefully handles `InvalidRequestError`
    exceptions, returning a descriptive error message when the request fails.

    Args:
        trades:
            An instance of the `RecentTrades` class containing the parameters for fetching
            the recent trades. These include:
            - `category` (str): The category of the market (e.g., "spot", "linear").
            - `symbol` (Optional[str]): The trading pair symbol (e.g., "BTCUSDT").
            - `limit` (Optional[int]): The number of trade entries to retrieve (default is `None` for all available trades).

    Returns:
        dict: The response from the Bybit API, including the recent trade history for the specified trading pair.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.get_public_trade_history(
            category=trades.category,
            symbol=trades.symbol if trades.symbol else None,
            limit=trades.limit if trades.limit else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


############################################################################### Position Management:
async def get_position_info_f(position: PositionInfo):
    """
    Retrieve position information for a specific trading pair or account.

    This function sends a request to the Bybit API to fetch detailed position
    information. The user can specify the category, trading pair symbol, settlement coin,
    and other optional parameters such as limit and cursor to paginate through results.
    The function gracefully handles `InvalidRequestError` exceptions, returning a
    descriptive error message when the request fails.

    Args:
        position:
            An instance of the `PositionInfo` class containing the parameters for retrieving
            the position information. These include:
            - `category` (str): The category of the market (e.g., "spot", "linear").
            - `symbol` (Optional[str]): The trading pair symbol (e.g., "BTCUSDT").
            - `settleCoin` (Optional[str]): The coin used for settlement (e.g., "USDT").
            - `limit` (Optional[int]): The number of position entries to retrieve.
            - `cursor` (Optional[str]): A cursor for pagination, used to fetch the next page of results.

    Returns:
        dict: The response from the Bybit API containing the position information.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.get_positions(
            category=position.category,
            symbol=position.symbol if position.symbol else None,
            settleCoin=position.settleCoin if position.settleCoin else None,
            limit=position.limit if position.limit else None,
            cursor=position.cursor if position.cursor else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def set_leverage_for_position_f(leverage: SetLeverage):
    """
    Set leverage for a specific trading pair on Bybit.

    This function sends a request to the Bybit API to set the leverage for a
    given position in the specified trading pair. The leverage for both buy and
    sell orders can be set separately. The function gracefully handles
    `InvalidRequestError` exceptions, returning a descriptive error message when the request fails.

    Args:
        leverage:
            An instance of the `SetLeverage` class containing the parameters
            for setting leverage on a position. These include:
            - `category` (str): The category of the market (e.g., "spot", "linear").
            - `symbol` (str): The trading pair symbol (e.g., "BTCUSDT").
            - `buyLeverage` (str): The leverage for buy orders (e.g., "5").
            - `sellLeverage` (str): The leverage for sell orders (e.g., "5").

    Returns:
        dict: The response from the Bybit API confirming the leverage has been set.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.set_leverage(
            category=leverage.category,
            symbol=leverage.symbol,
            buyLeverage=leverage.buyLeverage,
            sellLeverage=leverage.sellLeverage,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def switch_position_mode_f(positionmode: SwitchPositionMode):
    """
    Switch the position mode for a specific trading pair on Bybit.

    This function allows the user to change the position mode for a given
    trading pair. The position mode can be either "hedged" or "one-way" and
    is specified by the `mode` parameter. The function handles `InvalidRequestError`
    exceptions and returns a descriptive error message if the request fails.

    Args:
        positionmode:
            An instance of the `SwitchPositionMode` class containing the parameters
            for switching the position mode. These include:
            - `category` (str): The category of the market (e.g., "spot", "linear").
            - `symbol` (Optional[str]): The trading pair symbol (e.g., "BTCUSDT"). If not provided, defaults to `None`.
            - `coin` (Optional[str]): The coin type for the position (e.g., "USDT"). If not provided, defaults to `None`.
            - `mode` (int): The position mode to be set (1 for "one-way" mode, 2 for "hedged" mode).

    Returns:
        dict: The response from the Bybit API confirming the position mode has been switched.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.switch_position_mode(
            category=positionmode.category,
            symbol=positionmode.symbol if positionmode.symbol else None,
            coin=positionmode.coin if positionmode.coin else None,
            mode=positionmode.mode,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


############################################################################### Risk Settings:
async def get_risk_limit_f(risk: RiskLimit):
    """
    Retrieve the risk limit settings for a specific trading pair on Bybit.

    This function retrieves the current risk limits for a given trading pair
    based on the provided parameters. The `symbol` and `cursor` can be provided
    to filter the results. If no values are specified, defaults are applied.
    The function gracefully handles `InvalidRequestError` exceptions and
    returns a descriptive error message if the request fails.

    Args:
        risk:
            An instance of the `RiskLimit` class containing the required and
            optional parameters for retrieving risk limits. These include:
            - `category` (str): The category of the market (e.g., "linear", "spot").
            - `symbol` (Optional[str]): The trading pair symbol (e.g., "BTCUSDT"). If not provided, defaults to `None`.
            - `cursor` (Optional[str]): A cursor for pagination (if applicable) to retrieve the next set of results.

    Returns:
        dict: The response from the Bybit API containing the risk limits for the specified trading pair.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.get_risk_limit(
            category=risk.category,
            symbol=risk.symbol if risk.symbol else None,
            cursor=risk.cursor if risk.cursor else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


############################################################################### User Data Stream (Real-time Updates):
async def listen_stream(symbol: str, category: str):
    """
    Listens to a WebSocket stream for real-time market data or user data based on the provided symbol and category.

    This function connects to the specified WebSocket stream, continuously receives messages, and processes them
    via a callback function. The stream runs asynchronously, printing incoming messages until the stop_event is triggered.

    Args:
        symbol (str): The trading pair symbol to listen to, e.g., "BTCUSDT". The symbol will be converted to uppercase.
        category (str): The category of the stream, such as "user" or "market", specifying the type of data to receive.

    Raises:
        None: This function does not explicitly raise any exceptions, but WebSocket connection issues may cause errors.

    Note:
        The function runs asynchronously and continuously, and can be stopped by setting the `stop_event`.

    Last Reviewed Date:
        11 Dec 2024
    """
    symbol = symbol.upper()

    ws = WebSocket(
        testnet=True,
        channel_type=category,
    )

    def handle_message(message):
        if not stop_event.is_set():
            print(message)

    print("Connected to Binance User Data Stream.")

    while not stop_event.is_set():
        ws.ticker_stream(symbol=symbol, callback=handle_message)

        sleep(1)

        # You can add more processing here as needed
    ws.exit()
    print("websocket has stopped")


############################################################################### Market Data (Additional Functions):


async def get_funding_rate_for_symbol_f(fundingrate: FundingRateHistory):
    """
    Retrieve the funding rate history for a specific trading pair on Bybit.

    This function fetches the funding rate history for a specified trading pair
    over a defined time range. The `symbol`, `startTime`, `endTime`, and `limit`
    parameters allow the user to filter the data. If these values are not provided,
    defaults will be applied. The function handles `InvalidRequestError` exceptions
    and returns a descriptive error message if the request fails.

    Args:
        fundingrate:
            An instance of the `FundingRateHistory` class containing the required
            and optional parameters for fetching the funding rate history. These include:
            - `category` (str): The category of the market (e.g., "linear", "spot").
            - `symbol` (str): The trading pair symbol (e.g., "BTCUSDT").
            - `startTime` (Optional[int]): The start timestamp for filtering the data (default is `None`).
            - `endTime` (Optional[int]): The end timestamp for filtering the data (default is `None`).
            - `limit` (Optional[int]): The number of results to return (default is `None`).

    Returns:
        dict: The response from the Bybit API containing the funding rate history for the specified symbol.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.get_funding_rate_history(
            category=fundingrate.category,
            symbol=fundingrate.symbol,
            startTime=fundingrate.startTime if fundingrate.startTime else None,
            endTime=fundingrate.endTime if fundingrate.endTime else None,
            limit=fundingrate.limit if fundingrate.limit else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


async def get_exchange_info_f(exchangeinfo: CoinExchangeRecord):
    """
    Retrieve the coin exchange records for a specific pair of coins.

    This function fetches the exchange records for a specified pair of coins
    (fromCoin to toCoin) from the Bybit API. It supports optional filters like
    `fromCoin`, `toCoin`, `limit`, and `cursor` for pagination. The function
    handles `InvalidRequestError` exceptions and returns a descriptive error
    message if the request fails.

    Args:
        exchangeinfo:
            An instance of the `CoinExchangeRecord` class containing the required
            and optional parameters for fetching the coin exchange records. These include:
            - `fromCoin` (Optional[str]): The base coin in the exchange pair (e.g., "BTC").
            - `toCoin` (Optional[str]): The quote coin in the exchange pair (e.g., "USDT").
            - `limit` (Optional[int]): The number of records to return per request (default is `None`).
            - `cursor` (Optional[str]): A pagination cursor for fetching the next set of records (default is `None`).

    Returns:
        dict: The response from the Bybit API containing the coin exchange records for the specified pair of coins.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.get_coin_exchange_records(
            fromCoin=exchangeinfo.fromCoin if exchangeinfo.fromCoin else None,
            toCoin=exchangeinfo.toCOin if exchangeinfo.toCOin else None,
            limit=exchangeinfo.limit if exchangeinfo.limit else None,
            cursor=exchangeinfo.cursor if exchangeinfo.cursor else None,
        )

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"


############################################################################### Miscellaneous/Utility:


async def get_server_time_f():
    """
    Retrieve the current server time from Bybit.

    This function fetches the current server time from the Bybit API. It is used
    to obtain the accurate timestamp for the server, which can be useful for
    synchronization purposes, such as timestamp-based orders or time-sensitive operations.
    The function handles `InvalidRequestError` exceptions and returns a descriptive error
    message if the request fails.

    Returns:
        dict: The response from the Bybit API containing the current server time.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        response = session.get_server_time()

        return response
    except InvalidRequestError as e:
        return f"Invalid request error: {str(e)}"
