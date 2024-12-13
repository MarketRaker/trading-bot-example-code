from fastapi import APIRouter
from app.crud.Binance_CRUD import *
from app.schemas.Binance_Schema import *
import asyncio
import websockets


router = APIRouter()
stop_event = asyncio.Event()


####################################################### Account Management
#######################################################


##### Get your account info
@router.get("/account")
async def binance_account():
    """
    Endpoint to retrieve the account information of the user on Binance.
        Input:
            - None
    """
    return await get_binance_account_info()


##### Check if you can trade on your account
@router.get("/tradingstatus")
async def binance_trading_status():
    """
    Endpoint to retrieve the current trading status of the Binance API.
        Input:
            - None
    """
    return await get_binance_trading_status()


######################################################  End of Account Management
######################################################
#
######################################################  Market Data
######################################################


##### Get the average price
@router.get("/avgprice")
async def binance_avg_price(request: AvgPriceRequest):
    """
    Endpoint to retrieve the average price of a symbol on Binance.
        Input:
            - symbol (str): The symbol for which the average price is being queried (e.g., "BTCUSDT").
    """
    return await get_binance_avg_price(request.symbol)


##### Get order book
@router.get("/orderbook")
async def binance_order_book(request: OrderBookRequest):
    """
    Endpoint to retrieve order book depth data.
        Input:
            - symbol (str): The symbol for which the order book is being queried (e.g., "BTCUSDT").
            - limit (int): The number of order book entries to return. Common values are 5, 10, 20, 50, 100, 500, and 1000.
    """
    return await get_binance_order_book(request.symbol, request.limit)


##### Get symbol price
@router.get("/priceticker")
async def binance_price_ticker(request: PriceTickerRequest):
    """
    Endpoint to retrieve the latest price of a symbol on Binance.
        Input:
            - symbol (str): The symbol for which the price ticker is being queried (e.g., "BTCUSDT").
    """
    return await get_binance_price_ticker(request.symbol)


##### Get 24 hour price statistics
@router.get("/pricechangestats")
async def binance_24hr_price_change_stats(request: PriceChangeStatsRequest):
    """
    Endpoint to retrieve the 24-hour price change statistics for a symbol on Binance.
        Input:
            - symbol (str): The symbol for which the 24-hour price change is being queried (e.g., "BTCUSDT").
    """
    return await get_binance_24hr_price_change_stats(request.symbol)


##### Get Historic trades
@router.get("/historicaltrades")
async def binance_historical_trades(request: HistoricalTradesRequest):
    """
    Endpoint to retrieve historical trades for a specific symbol from Binance.
        Input:
            - symbol (str): The trading pair (e.g., "BTCUSDT").
            - limit (int): The maximum number of trades to retrieve.
            - fromId (Optional[int]): The trade ID to start from (optional, for pagination).
    """
    return await get_binance_historical_trades(
        request.symbol, request.limit, request.fromId
    )


######################################################  End of Market Data
######################################################
#
######################################################  Placing & Managing Orders
######################################################


##### Make Trade
@router.post("/order")
async def binance_Trade(order: OrderRequest):
    """
    Endpoint to place a trade order on Binance.
        Input:
            - symbol (str): The trading pair (e.g., "BTCUSDT").
            - side (str): The side of the order ("BUY" or "SELL").
            - quantity (float): The quantity to buy/sell.
    """
    return await Binance_place_order(order.symbol, order.side, order.quantity)


##### Get all open orders by type
@router.get("/allopenorders")
async def binance_GetOpenOrders(all_OpenOrders: AllOrders):
    """
    Endpoint to retrieve all open orders for a specific trading pair.
        Input:
            - symbol (str): The trading pair (e.g., "BTCUSDT").
    """
    return await Binance_get_open_orders(all_OpenOrders.symbol)


##### Get Order Detail by Id
@router.get("/orderdetails")
async def binance_order_details(request: OrderDetailsRequest):
    """
    Endpoint to retrieve details of a specific order by its ID or client order ID.
        Input:
            - symbol (str): The trading pair (e.g., "BTCUSDT").
            - orderId (Optional[int]): The Binance order ID.
            - clientOrderId (Optional[str]): The client order ID (optional).
    """
    return await get_binance_order_details(
        request.symbol, request.orderId, request.clientOrderId
    )


##### Cancel open order
@router.delete(
    "/cancelorder"
)  # only works if the order is still open. open orders can be found by using the binance_GetOpenOrders function
async def cancel_order(cancel_Order: CancelOrder):
    """
    Endpoint to cancel an order on Binance Spot Testnet.
        Input:
            - symbol: Trading pair (e.g., BTCUSDT)
            - order_id: Binance order ID
            - orig_client_order_id: Client order ID
    """
    return await Binance_cancel_order(
        cancel_Order.symbol, cancel_Order.orderId, cancel_Order.clientOrderId
    )


######################################################  End of Placing & Managing Orders
######################################################
#
######################################################  Advanced Trading
######################################################

####### Trading History & Information


##### Get all orders on account by type
@router.get("/allorders")
async def binance_GetOrders(all_Orders: AllOrders):
    """
    Endpoint to retrieve all orders for a specific symbol on Binance.
        Input:
            - symbol (str): The symbol for which the orders are being queried (e.g., "BTCUSDT").
    """
    return await Binance_get_orders(all_Orders.symbol)


##### Get all recent trades
@router.get("/recenttrades")
async def binance_recent_trades(request: RecentTradesRequest):
    """
    Endpoint to retrieve recent trade data for a symbol on Binance.
        Input:
            - symbol (str): The symbol for which recent trades are being queried (e.g., "BTCUSDT").
            - limit (int): The number of recent trades to return.
    """
    return await get_binance_recent_trades(request.symbol, request.limit)


####### User Data Stream
##### Start data stream
@router.post("/startuserdatastream")
async def binance_start_user_data_stream():
    """
    Endpoint to start a new user data stream.
        Input:
            - None
    """
    return await start_user_data_stream()


##### Keep the data stream alive
@router.put("/keepuserdatastreamalive")
async def binance_keep_user_data_stream_alive(request: ListenKeyRequest):
    """
    Endpoint to keep the user data stream alive.
        Input:
            - listen_key (str): The listen key for the user data stream.
    """
    return await keep_user_data_stream_alive(request.listenKey)


######################################################  End of Advanced Trading
######################################################
#
######################################################  Useful Tools
######################################################


##### One-Cancels-the-Other
@router.post("/ocoorder")
async def binance_oco_order(order_data: OCOOrderRequest):
    """
    Endpoint to place an OCO (One Cancels Other) order on Binance.
        Input:
            - symbol (str): The symbol for which the OCO order is placed (e.g., "BTCUSDT").
            - side (str): The side of the order, either "BUY" or "SELL".
            - quantity (float): The quantity of the symbol to buy/sell.
            - price (float): The price of the limit order.
            - stopPrice (float): The stop price of the stop-limit order.
            - stopLimitPrice (float): The stop-limit price.
            - stopLimitTimeInForce (str): The time in force for the stop-limit order (e.g., "GTC").
            - listClientOrderId (str): The client order ID for the OCO order.
    """
    return await place_oco_order(order_data)


##### Get system Status
@router.get("/servertime")
async def binance_system_status():
    """
    Endpoint to retrieve the current system status of the Binance API.
        Input:
            - None
    """
    return await get_system_time()


######################################################  End of Useful Tools
######################################################


####################################################### Websocket functions


async def listen_stream(symbol: str):
    symbol = symbol.lower()
    url = f"wss://testnet.binance.vision/ws/{symbol}@trade"

    async with websockets.connect(url) as ws:
        print("Connected to Binance User Data Stream.")

        while not stop_event.is_set():
            message = await ws.recv()
            event = json.loads(message)

            quantity = float(event["q"])
            price = float(event["p"])
            print("$" + str(quantity * price))
            print("R" + str(quantity * price * 18))
            print("")

            # You can add more processing here as needed
    print("websocket has stopped")


@router.post("/startwebsocket")
async def start_listening(symbol: SymbolType):
    asyncio.create_task(listen_stream(symbol.symbol))


@router.delete("/stopwebsocket")
async def stop_listening():
    stop_event.set()
    await asyncio.sleep(1)
    stop_event.clear()
    return {"status": "Stopped listening to WebSocket."}
