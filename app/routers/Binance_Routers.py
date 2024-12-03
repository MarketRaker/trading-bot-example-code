from fastapi import APIRouter
from app.crud.Binance_CRUD import *
from app.models.Binance_Models import *


router = APIRouter()


####################################################### Account Management
#######################################################

##### Get your account info
@router.get("/account")
async def binance_account():
    return await get_binance_account_info()

##### Check if you can trade on your account
@router.get("/tradingStatus")
async def binance_trading_status():
    return await get_binance_trading_status()

######################################################  End of Account Management
######################################################
#
######################################################  Market Data
######################################################

##### Get the average price
@router.post("/avgPrice")
async def binance_avg_price(request: AvgPriceRequest):
    """
    Endpoint to retrieve the average price of a symbol over the last 24 hours.
    Accepts input from the JSON body.
    """
    return await get_binance_avg_price(request.symbol)

##### Get order book
@router.post("/orderBook")
async def binance_order_book(request: OrderBookRequest):
    """
    Endpoint to retrieve order book depth data.
    Accepts input from the JSON body.
    """
    return await get_binance_order_book(request.symbol, request.limit)

##### Get symbol price
@router.post("/priceTicker")
async def binance_price_ticker(request: PriceTickerRequest):
    """
    Endpoint to get the latest price for a symbol.
    Accepts input from the JSON body.
    """
    return await get_binance_price_ticker(request.symbol)

##### Get 24 hour price statistics
@router.post("/priceChangeStats")
async def binance_24hr_price_change_stats(request: PriceChangeStatsRequest):
    """
    Endpoint to retrieve 24-hour price change statistics for a symbol.
    Accepts input from the JSON body.
    """
    return await get_binance_24hr_price_change_stats(request.symbol)

##### Get Historic trades
@router.post("/historicalTrades")
async def binance_historical_trades(request: HistoricalTradesRequest):
    """
    Endpoint to retrieve historical trades for a symbol.
    Accepts input from the JSON body.
    """
    return await get_binance_historical_trades(request.symbol, request.limit, request.fromId)

######################################################  End of Market Data
######################################################
#
######################################################  Placing & Managing Orders
######################################################

##### Make Trade
@router.post("/order/test")
async def binance_TestTrade(order:OrderRequest):
    return await Binance_place_order(order.symbol,order.side,order.quantity)

##### Get all open orders by type
@router.get("/allOpenOrders")
async def binance_GetOpenOrders(all_OpenOrders:AllOrders):
    return await Binance_get_open_orders(all_OpenOrders.symbol)

##### Get Order Detail by Id
@router.post("/orderDetails")
async def binance_order_details(request: OrderDetailsRequest):
    """
    Endpoint to retrieve the status of a specific order using orderId or clientOrderId.
    Accepts input from the JSON body.
    """
    return await get_binance_order_details(request.symbol, request.orderId, request.clientOrderId)

##### Cancel open order
@router.delete("/cancelOrder") # only works if the order is still open. open orders can be found by using the binance_GetOpenOrders function
async def cancel_order(cancel_Order:cancelOrder):
    print(cancel_Order)
    """
    Endpoint to cancel an order on Binance Spot Testnet.
    param: 
        symbol: Trading pair (e.g., BTCUSDT)
        order_id: Binance order ID
        orig_client_order_id: Client order ID
    """
    return await Binance_cancel_order(cancel_Order.symbol, cancel_Order.orderId, cancel_Order.clientOrderId)

######################################################  End of Placing & Managing Orders
######################################################
#
######################################################  Advanced Trading
######################################################

####### Margin and Futures trading
##### Get Futures Account Info
@router.get("/testnet/futuresAccount")
async def futures_account_testnet():
    """
    Endpoint to retrieve Binance Futures account information on Testnet.
    """
    return await get_futures_account_info()

##### Make Futures Trade
@router.post("/futures/order")
async def futures_order(order: FuturesOrderRequest):
    """
    Endpoint to place an order on the Binance Futures Testnet.
    """
    return await place_futures_order(order)

##### Cancel Futures Order
@router.delete("/futures/order")
async def cancel_futures_order_endpoint(request: CancelFuturesOrderRequest):
    """
    Endpoint to cancel a Binance Futures order.
    """
    return await cancel_futures_order(request)

##### Get Futures Order History
@router.get("/futures/orderHistory")
async def futures_order_history(request: FuturesOrderHistoryRequest):
    """
    Endpoint to retrieve Binance Futures order history.
    """
    return await get_futures_order_history(request)

####### Trading History & Information

##### Get all orders on account by type
@router.get("/allOrders")
async def binance_GetOrders(all_Orders:AllOrders):
    return await Binance_get_orders(all_Orders.symbol)

##### Get all recent trades
@router.post("/recentTrades")
async def binance_recent_trades(request: RecentTradesRequest):
    """
    Endpoint to retrieve recent trades for a symbol.
    Accepts input from the JSON body.
    """
    return await get_binance_recent_trades(request.symbol, request.limit)

####### User Data Stream
##### Start data stream
@router.post("/startUserDataStream")
async def binance_start_user_data_stream():
    """
    Endpoint to start a new user data stream for real-time order updates.
    No input is required for this endpoint.
    """
    return await start_user_data_stream()

##### Keep the data stream alive
@router.put("/keepUserDataStreamAlive")
async def binance_keep_user_data_stream_alive(request: ListenKeyRequest):
    """
    Endpoint to keep the user data stream alive by sending a PUT request to Binance.
    The listenKey is passed in the JSON body.
    """
    return await keep_user_data_stream_alive(request.listenKey)

##### Delete the data stream
@router.delete("/closeUserDataStream")
async def binance_close_user_data_stream(request: ListenKeyRequest):
    """
    Endpoint to close the user data stream by sending a DELETE request to Binance.
    The listenKey is passed in the JSON body.
    """
    return await close_user_data_stream(request.listenKey)

######################################################  End of Advanced Trading
######################################################
#
######################################################  Useful Tools
######################################################

##### One-Cancels-the-Other 
@router.post("/ocoOrder")
async def binance_oco_order(order_data: OCOOrderRequest):
    """
    Endpoint to place an OCO (One-Cancels-the-Other) order on Binance.
    The order_data is provided in the JSON body.
    """
    return await place_oco_order(order_data)

##### Get system Status
@router.get("/systemStatus")
async def binance_system_status():
    """
    Endpoint to retrieve the status of the Binance system.
    Useful for debugging and checking if the Binance system is operational.
    """
    return await get_system_status()

######################################################  End of Useful Tools
######################################################