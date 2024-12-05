from fastapi import HTTPException
import hmac
import hashlib
import time
import httpx
import json
from decouple import config
from app.models.Binance_Models import OCOOrderRequest,FuturesOrderRequest,CancelFuturesOrderRequest,FuturesOrderHistoryRequest


BINANCE_API_KEY = str(config("BINANCE_API_KEY"))
BINANCE_API_SECRET = str(config("BINANCE_API_SECRET"))
BINANCE_BASE_URL = str(config("BINANCE_BASE_URL"))


########################################################################################## Signature
def create_signature(params: dict) -> str:
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    return hmac.new(BINANCE_API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()

########################################################################################## Account Info
async def get_binance_account_info():
    """
    Fetch the account information from Binance.

    This function sends a request to the Binance API to retrieve account details 
    such as balances, order status, and other account-level information. It 
    includes authentication using an API key and a signature for security. 

    Args:
        None

    Returns:
        dict: The response from the Binance API, which contains account information.
    """
    endpoint = "/api/v3/account"
    params = {
        "timestamp": int(time.time() * 1000)
    }
    params["signature"] = create_signature(params)
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        return response.json()
########################################################################################### Trading Status
async def get_binance_trading_status():
    """
    Fetch the trading status from Binance.

    This function sends a request to the Binance API to retrieve the current trading 
    status of the platform, which provides information about whether trading is 
    enabled or temporarily suspended. It uses authentication via an API key and a 
    signature for secure communication.

    Args:
        None

    Returns:
        dict: The response from the Binance API containing trading status information.

    Raises:
        HTTPException: If the API response status code is not 200, an exception 
        with the corresponding error message is raised.
    """
    endpoint = "/api/v3/apiTradingStatus"
    params = {
        "timestamp": int(time.time() * 1000)
    }
    params["signature"] = create_signature(params)
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
################################################################################################# Avg price
async def get_binance_avg_price(symbol: str):
    """
    Fetch the average price for a specified symbol from Binance.

    This function sends a request to the Binance API to retrieve the average price 
    of a trading pair (symbol). The response contains the most recent average 
    price for the specified symbol.

    Args:
        symbol (str): The symbol for which the average price is being queried 
        (e.g., "BTCUSDT").

    Returns:
        dict: The response from the Binance API containing the average price data 
        for the specified symbol.

    Raises:
        HTTPException: If the API response status code is not 200, an exception 
        with the corresponding error message is raised.
    """
    endpoint = "/api/v3/avgPrice"
    params = {"symbol": symbol}
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
################################################################################################# Show symbol order
async def get_binance_order_book(symbol: str, limit: int):
    """
    Fetch the order book for a specified symbol from Binance.

    This function sends a request to the Binance API to retrieve the order book 
    for a specific symbol (trading pair). The response includes the current order 
    book depth for the symbol with the specified limit.

    Args:
        symbol (str): The symbol for which the order book is being queried (e.g., "BTCUSDT").
        limit (int): The number of order book entries to return. Common values are 5, 10, 20, 50, 100, 500, and 1000.

    Returns:
        dict: The response from the Binance API containing the order book data 
        for the specified symbol and limit.

    Raises:
        HTTPException: If the API response status code is not 200, an exception 
        with the corresponding error message is raised.
    """
    endpoint = "/api/v3/depth"
    params = {"symbol": symbol, "limit": limit}
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
################################################################################################# Get symbol price
async def get_binance_price_ticker(symbol: str):
    """
    Fetch the current price ticker for a specified symbol on Binance.

    This function sends a request to the Binance API to retrieve the latest 
    price ticker for a specified symbol (trading pair). The response includes 
    the most recent price for the symbol.

    Args:
        symbol (str): The symbol for which the price ticker is being queried (e.g., "BTCUSDT").

    Returns:
        dict: The response from the Binance API containing the current price 
        for the specified symbol.

    Raises:
        HTTPException: If the API response status code is not 200, an exception 
        with the corresponding error message is raised.
    """
    endpoint = "/api/v3/ticker/price"
    params = {"symbol": symbol}
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
################################################################################################# Get 24 hour price change statistics
async def get_binance_24hr_price_change_stats(symbol: str):
    """
    Fetch the 24-hour price change statistics for a specified symbol on Binance.

    This function sends a request to the Binance API to retrieve the 24-hour price 
    change statistics for a specified symbol. The response includes information 
    such as the price change, price percentage change, high/low prices, and 
    other relevant statistics for the last 24 hours.

    Args:
        symbol (str): The symbol for which the 24-hour price change statistics are being queried (e.g., "BTCUSDT").

    Returns:
        dict: The response from the Binance API containing the 24-hour price 
        change statistics for the specified symbol.

    Raises:
        HTTPException: If the API response status code is not 200, an exception 
        with the corresponding error message is raised.
    """

    endpoint = "/api/v3/ticker/24hr"
    params = {"symbol": symbol}
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
################################################################################################# Historic Trades
async def get_binance_historical_trades(symbol: str, limit: int, from_id: int = None):
    """
    Fetch historical trades for a specified symbol on Binance.

    This function sends a request to the Binance API to retrieve historical trades 
    for a specified symbol. It allows you to specify the number of trades to 
    retrieve and an optional trade ID to start from.

    Args:
        symbol (str): The symbol for which the historical trades are being queried (e.g., "BTCUSDT").
        limit (int): The maximum number of trades to retrieve (up to 1000).
        from_id (Optional[int]): The trade ID to start the query from (optional).

    Returns:
        dict: The response from the Binance API containing historical trades for 
        the specified symbol.

    Raises:
        HTTPException: If the API response status code is not 200, an exception 
        with the corresponding error message is raised.
    """

    endpoint = "/api/v3/historicalTrades"
    params = {"symbol": symbol, "limit": limit}
    if from_id:
        params["fromId"] = from_id

    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

#################################################################################################  Buy Trade Function    
async def Binance_place_order(symbol: str, side: str, quantity: float):
    """
    Place a test order on Binance Spot Testnet.

    This function sends a request to the Binance API to place a test market order 
    on the Binance Spot Testnet. It allows you to specify the symbol, side (buy/sell), 
    and quantity for the test order. This test ensures the validity of the API interaction 
    without executing a real trade.

    Args:
        symbol (str): The symbol for the market order (e.g., "BTCUSDT").
        side (str): The side of the order ("BUY" or "SELL").
        quantity (float): The quantity of the asset to buy or sell.

    Returns:
        dict: A response indicating that the test order was successfully placed.

    Raises:
        HTTPException: If the API response status code is not 200, an exception 
        with the corresponding error message is raised.
    """

    endpoint = "/api/v3/order" # Replace with /api/v3/order/test if you just want to test if the interaction is valid
    url = BINANCE_BASE_URL + endpoint

    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": int(time.time() * 1000),
    }
    params["signature"] = create_signature(params)

    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, params=params)
        if response.status_code == 200:
            return {"status": "success", "message": "Test order placed successfully"}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

################################################################################################### get all open orders by spesific type
async def Binance_get_open_orders(symbol: str):
    """
    Retrieve open orders for a specific symbol on Binance.

    This function sends a request to the Binance API to fetch all open orders 
    for a given trading pair (symbol). The function returns the current active 
    orders that have not been filled or canceled.

    Args:
        symbol (str): The symbol for which to retrieve open orders (e.g., "BTCUSDT").

    Returns:
        dict: A list of open orders for the specified symbol.

    Raises:
        HTTPException: If the API response status code is not 200, an exception 
        with the corresponding error message is raised.
    """

    endpoint = "/api/v3/openOrders"
    url = BINANCE_BASE_URL + endpoint

    params = {
        "symbol": symbol,
        "timestamp": int(time.time() * 1000),
    }
    params["signature"] = create_signature(params)
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
################################################################################################### Get order details by order ID
async def get_binance_order_details(symbol: str, order_id: int = None, client_order_id: str = None):
    """
    Retrieve details of an order from Binance.

    This function retrieves information about a specific order on Binance by 
    either its `orderId` or `clientOrderId`. If neither is provided, a 400 
    HTTP error is raised.

    Args:
        symbol (str): The symbol of the order (e.g., "BTCUSDT").
        order_id (int, optional): The unique ID of the order.
        client_order_id (str, optional): The unique client-specified ID of the order.

    Returns:
        dict: The details of the order, including its status, price, quantity, etc.

    Raises:
        HTTPException: If the API response status code is not 200, or if 
        neither `orderId` nor `clientOrderId` is provided.
    """

    endpoint = "/api/v3/order"
    params = {
        "symbol": symbol,
        "timestamp": int(time.time() * 1000),
    }

    # Include either orderId or clientOrderId
    if order_id:
        params["orderId"] = order_id
    elif client_order_id:
        params["clientOrderId"] = client_order_id
    else:
        raise HTTPException(status_code=400, detail="Either orderId or clientOrderId must be provided.")

    # Generate the signature for authentication
    params["signature"] = create_signature(params)

    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

################################################################################################### cancel open orders
async def Binance_cancel_order(symbol: str, order_id: int = None, orig_client_order_id: str = None):
    """
    Cancel an order on Binance.

    This function cancels an existing order on Binance using either its `orderId` 
    or `orig_client_order_id`. If neither is provided, a 400 HTTP error is raised.

    Args:
        symbol (str): The symbol of the order to be canceled (e.g., "BTCUSDT").
        order_id (int, optional): The unique ID of the order to cancel.
        orig_client_order_id (str, optional): The unique client-specified ID of the order to cancel.

    Returns:
        dict: The response indicating the cancellation status, including details 
        about the canceled order.

    Raises:
        HTTPException: If the API response status code is not 200, or if 
        neither `order_id` nor `orig_client_order_id` is provided.
    """

    endpoint = "/api/v3/order"
    url = BINANCE_BASE_URL + endpoint

    params = {
        "symbol": symbol,
        "timestamp": int(time.time() * 1000),
    }
    # Include either order_id or orig_client_order_id
    if order_id:
        params["orderId"] = order_id
    elif orig_client_order_id:
        params["clientOrderId"] = orig_client_order_id
    else:
        raise HTTPException(status_code=400, detail="Either order_id or orig_client_order_id must be provided.")

    params["signature"] = create_signature(params)
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

################################################################################################## Trading History & Information
############################################################################################### Get all the orders on account of spesific type
async def Binance_get_orders(symbol: str):
    """
    Fetch all orders for a specific symbol on Binance.

    This function retrieves all orders associated with a given symbol on Binance.
    It can be used to fetch historical order data for a specific trading pair.

    Args:
        symbol (str): Trading pair symbol (e.g., "BTCUSDT") for which the orders are to be fetched.

    Returns:
        list: A list of all orders retrieved from the Binance Spot Testnet API for the given symbol.

    Raises:
        HTTPException: If the API response status code is not 200, an error is raised indicating the failure.
    """

    endpoint = "/api/v3/allOrders"
    url = BINANCE_BASE_URL + endpoint

    params = {
        "symbol": symbol,
        "timestamp": int(time.time() * 1000),
    }
    params["signature"] = create_signature(params)

    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        
############################################################################################### Get recent orders
async def get_binance_recent_trades(symbol: str, limit: int):
    """
    Fetch recent trades for a specific symbol on Binance.

    This function retrieves a list of recent trades for a given symbol on Binance.
    The data returned includes trade details such as price, quantity, and trade timestamp.

    Args:
        symbol (str): The trading pair symbol (e.g., "BTCUSDT").
        limit (int): The number of recent trades to fetch (max 1000).

    Returns:
        list: A list of recent trades for the given symbol.

    Raises:
        HTTPException: If the API response status code is not 200, an error is raised indicating the failure.
    """

    endpoint = "/api/v3/trades"
    params = {
        "symbol": symbol,
        "limit": limit,
    }

    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

################################################################################################## User Data Stream
############################################################################################### Start Data stream
async def start_user_data_stream():
    """
    Start a new user data stream on Binance.

    This function initiates a new user data stream on Binance and returns a listenKey,
    which can be used to subscribe to the stream and receive real-time updates for user account events
    like orders, balances, and positions.

    Returns:
        dict: Contains the listenKey required for subscribing to the user data stream.

    Raises:
        HTTPException: If the API response status code is not 200, an error is raised indicating the failure.
    """
   
    endpoint = "/api/v3/userDataStream"
    params = {
       # "timestamp": int(time.time() * 1000),
    }
    params["signature"] = create_signature(params)

    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BINANCE_BASE_URL + endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()  # Returns the listenKey for the user data stream
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        
############################################################################################### Keep data stream alive
async def keep_user_data_stream_alive(listen_key: str):
    """
    Keep an existing user data stream alive on Binance.

    This function is used to send a request to Binance to extend the lifetime of an active user data stream
    by refreshing the listenKey. The listenKey is required to continue receiving real-time updates for user
    account events like orders, balances, and positions.

    Args:
        listen_key (str): The listenKey of the active user data stream.

    Returns:
        dict: A confirmation message indicating that the stream was successfully kept alive.

    Raises:
        HTTPException: If the API response status code is not 200, an error is raised indicating the failure.
    """

    endpoint = "/api/v3/userDataStream"
    params = {
        "listenKey": listen_key,
        "timestamp": int(time.time() * 1000),
    }
    params["signature"] = create_signature(params)

    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return {"status": "success", "message": "Stream kept alive successfully"}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        
################################################################################################## Place an One Cancels Other order
async def place_oco_order(order_data: OCOOrderRequest):
    """
    Place an OCO (One Cancels the Other) order on Binance.

    An OCO order allows you to place two orders simultaneously where if one order is executed, the other is automatically canceled. This function places such an order with a stop-limit component and a regular limit order.

    Args:
        order_data (OCOOrderRequest): The data for the OCO order, including symbol, side, quantity, price, stop price, and limit price details.

    Returns:
        dict: The response from Binance containing details of the created OCO order.

    Raises:
        HTTPException: If the API response status code is not 200, an error is raised with the details of the failure.
    """

    endpoint = "/api/v3/orderList"
    params = {
        "symbol": order_data.symbol,
        "side": order_data.side,
        "quantity": order_data.quantity,
        "price": order_data.price,
        "stopPrice": order_data.stopPrice,
        "stopLimitPrice": order_data.stopLimitPrice,
        "stopLimitTimeInForce": order_data.stopLimitTimeInForce,
        "listClientOrderId": order_data.listClientOrderId,
        "timestamp": int(time.time() * 1000),
    }
    params["signature"] = create_signature(params)

    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        
################################################################################################## Get system Status
async def get_system_time():
    """
    Fetch the server time from Binance.

    This function retrieves the current time of the Binance API server.

    Returns:
        dict: The response from Binance, which contains the current server time.

    Raises:
        HTTPException: If the API response status code is not 200, an error is raised with the details of the failure.
        JSONDecodeError: If the response body is not valid JSON, an error will be raised indicating the invalid format.
    """

    endpoint = "/api/v3/time"
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_BASE_URL + endpoint, headers=headers)
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Received invalid JSON response from Binance.")
        else:
            try:
                error_detail = response.json()
            except json.JSONDecodeError:
                error_detail = response.text or "No response content"
            
            raise HTTPException(status_code=response.status_code, detail=error_detail)















