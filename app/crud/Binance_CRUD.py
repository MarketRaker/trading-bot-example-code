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
BINANCE_FUTURES_API_KEY = str(config("BINANCE_FUTURES_API_KEY"))
BINANCE_FUTURES_API_SECRET = str(config("BINANCE_FUTURES_API_SECRET"))
BINANCE_FUTURES_BASE_URL = str(config("BINANCE_FUTURES_BASE_URL"))


########################################################################################## Signature
def create_signature(params: dict) -> str:
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    return hmac.new(BINANCE_API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()

########################################################################################## Account Info
async def get_binance_account_info():
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
    """Place a test order on Binance Spot Testnet."""
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
    """Get all open orders for a specific symbol."""
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
    """Cancel an order on Binance Spot Testnet."""
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
        
################################################################################################## Margin and Futures trading
############################################################################################### Get futures account info
async def get_futures_account_info():
    endpoint = "/fapi/v2/account"
    params = {
        "timestamp": int(time.time() * 1000),
    }
    params["signature"] = create_signature(params)
    
    headers = {
        "X-MBX-APIKEY": BINANCE_FUTURES_API_KEY,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_FUTURES_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

############################################################################################### Make Futures Trade
async def place_futures_order(order: FuturesOrderRequest):
    endpoint = "/fapi/v1/order"
    params = {
        "symbol": order.symbol,
        "side": order.side,
        "type": order.type,
        "quantity": order.quantity,
        "timestamp": int(time.time() * 1000),
    }

    # Add optional parameters for LIMIT orders
    if order.type == "LIMIT" and order.price is not None:
        params["price"] = order.price
        params["timeInForce"] = order.time_in_force

    # Create signature
    params["signature"] = create_signature(params)

    headers = {
        "X-MBX-APIKEY": BINANCE_FUTURES_API_KEY,
    }

    # Send POST request
    async with httpx.AsyncClient() as client:
        response = await client.post(BINANCE_FUTURES_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

############################################################################################### Cancel Futures Trade
async def cancel_futures_order(request: CancelFuturesOrderRequest):
    endpoint = "/fapi/v1/order"
    params = {
        "symbol": request.symbol,
        "timestamp": int(time.time() * 1000),
    }

    # Include either order_id or orig_client_order_id
    if request.order_id:
        params["orderId"] = request.order_id
    elif request.orig_client_order_id:
        params["origClientOrderId"] = request.orig_client_order_id
    else:
        raise HTTPException(
            status_code=400,
            detail="Either order_id or orig_client_order_id must be provided."
        )

    # Add the signature
    params["signature"] = create_signature(params)

    headers = {
        "X-MBX-APIKEY": BINANCE_FUTURES_API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.delete(BINANCE_FUTURES_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

############################################################################################### Get Futures order history
async def get_futures_order_history(request: FuturesOrderHistoryRequest):
    endpoint = "/fapi/v1/allOrders"
    params = {
        "symbol": request.symbol,
        "timestamp": int(time.time() * 1000),
    }

    # Optional parameters
    if request.start_time:
        params["startTime"] = request.start_time
    if request.end_time:
        params["endTime"] = request.end_time
    if request.limit:
        params["limit"] = request.limit

    # Add the signature
    params["signature"] = create_signature(params)

    headers = {
        "X-MBX-APIKEY": BINANCE_FUTURES_API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BINANCE_FUTURES_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

################################################################################################## Trading History & Information
############################################################################################### Get all the orders on account of spesific type
async def Binance_get_orders(symbol: str):
    """Fetch all orders for a specific symbol on Binance Spot Testnet."""
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
    endpoint = "/api/v1/userDataStream"
    params = {
        "timestamp": int(time.time() * 1000),
    }
    params["signature"] = create_signature(params)

    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()  # Returns the listenKey for the user data stream
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        
############################################################################################### Keep data stream alive
async def keep_user_data_stream_alive(listen_key: str):
    endpoint = "/api/v1/userDataStream"
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

############################################################################################### End data stream
async def close_user_data_stream(listen_key: str):
    endpoint = "/api/v1/userDataStream"
    params = {
        "listenKey": listen_key,
        "timestamp": int(time.time() * 1000),
    }
    params["signature"] = create_signature(params)

    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.delete(BINANCE_BASE_URL + endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return {"status": "success", "message": "Stream closed successfully"}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        
################################################################################################## Place an One Cancels Other order
async def place_oco_order(order_data: OCOOrderRequest):
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
async def get_system_status():
    endpoint = "/sapi/v1/system/status"  # Correct endpoint for system status
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















