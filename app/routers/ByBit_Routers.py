from fastapi import APIRouter
from app.crud.ByBit_CRUD import *
from app.models.Bybit_Models import *
import asyncio


router = APIRouter()

############################################################################### Account and Wallet Management:
@router.get("/account/info")
async def bybit_account_info():
    '''
    Example of get_account_info_f() 
        Input:
        - No input parameters required.
    '''
    return await get_account_info_f()

@router.get("/account/wallet")
async def bybit_account_wallet(cointype:CoinType):
    '''
    Example of get_wallet_balance_f() 
        Input:
        - cointype.coin : "BTC" 
    '''
    return await get_wallet_balance_f(cointype.coin)

@router.get("/account/funding")
async def bybit_account_funding(cointype:CoinType):
    '''
    Example of get_account_funding_f() 
        Input:
        - cointype.coin : "BTC" 
    '''
    return await get_account_funding_f(cointype.coin)

@router.get("/account/tradingFee")
async def bybit_account_trading_fee(symboltype:SymbolType):
    '''
    Example of get_user_trading_fee_f() 
        Input:
        - symboltype.symbol : "BTCUSDT"
    '''
    return await get_user_trading_fee_f(symboltype.symbol)

############################################################################### Order Management:
@router.post("/order/create")
async def bybit_order_place(order:PlaceOrderRequest):
    '''
    Example of place_order_f() 
        Input:
        - order.category : "linear"
        - order.symbol : "BTCUSDT"
        - order.side : "Buy"
        - order.orderType : "Limit"
        - order.qty : "1"
        - order.price : "30000"
        - order.timeInForce : "GTC"
        - order.orderLinkId : "order123"
        - order.isLeverage : 1
        - order.orderFilter : "none"
    '''
    return await place_order_f(order)

@router.post("/order/cancel")
async def bybit_order_cancel(cancelorder:CancelOrder):
    '''
    Example of cancel_order_f() 
        Input:
        - cancelorder.category : "linear"
        - cancelorder.symbol : "BTCUSDT"
        - cancelorder.orderId : "123456"
        - cancelorder.orderLinkId : "order123"
    '''
    return await cancel_order_f(cancelorder)

@router.get("/order")
async def bybit_order_get(order:GetOrders):
    '''
    Example of get_orders_f() 
        Input:
        - order.category : "spot"
        - order.symbol : "BTCUSDT"
        - order.baseCoin : "BTC"
        - order.orderId : "123456"
        - order.openOnly : 1
        - order.limit : 10
    '''
    return await get_orders_f(order)

@router.post("/order/amend")
async def bybit_order_amend(order:AmendOrder):
    '''
    Example of modify_order_f()
        Input:
        - order.category : "spot"
        - order.symbol : "BTCUSDT"
        - order.orderId : "123456"
        - order.triggerPrice : "50000"
        - order.qty : "0.5"
        - order.price : "51000"
        - order.takeProfit : "52000"
        - order.stopLoss : "49000"
    '''
    return await modify_order_f(order)
############################################################################### Market Data:
@router.get("/market/ticker_price")
async def bybit_market_ticker_price(marketprice:MarketPriceTicker):
    '''
    Example of get_market_price_ticker_f()
        Input:
        - marketprice.category : "spot"
        - marketprice.symbol : "BTCUSDT"
    '''
    return await get_market_price_ticker_f(marketprice)

@router.get("/market/price_change")
async def bybit_market_price_change():

    return await get_24_hour_price_change_f()

@router.get("/market/kline")
async def bybit_market_kline(kline:GetKline):
    '''
    Example of get_Kline_data_f() 
        Input:
        - kline.symbol: "BTCUSDT"
        - kline.interval: "1m"
        - kline.start: 1630454400
        - kline.end: 1630465200
        - kline.limit: 200
    '''
    return await get_Kline_data_f(kline)

@router.get("/market/symbol_orderbook")
async def bybit_market_symbol_orderbook(orderbook:OrderBook):
    '''
    Example of get_symbol_order_book_f() 
        Input:
        - orderbook.category: "spot"
        - orderbook.symbol: "BTCUSDT"
        - orderbook.limit: 10
    '''
    return await get_symbol_order_book_f(orderbook)

@router.get("/market/recent_trades")
async def bybit_market_recent_tredes(recenttrades:RecentTrades):
    '''
    Example of get_recent_trades_f() 
        Input:
        - recenttrades.category: "spot"
        - recenttrades.symbol: "BTCUSDT"
        - recenttrades.limit: 5
    '''
    return await get_recent_trades_f(recenttrades)

############################################################################### Position Management:
@router.get("/position/info")
async def bybit_position_info(position:PositionInfo):
    '''
    Example of get_position_info_f() 
        Input:
        - position.category: "linear"
        - position.symbol: "BTCUSDT"
        - position.settleCoin: "USDT"
        - position.limit: 10
        - position.cursor: "next_cursor_value"
    '''
    return await get_position_info_f(position)

@router.post("/position/leverage")
async def bybit_position_set_leverage(leverage:SetLeverage):
    '''
    Example of set_leverage_for_position_f() 
        Input:
        - leverage.category: "linear"
        - leverage.symbol: "BTCUSDT"
        - leverage.buyLeverage: "10"
        - leverage.sellLeverage: "5"
    '''
    return await set_leverage_for_position_f(leverage)

@router.post("/position/mode")
async def bybit_position_switch_mode(positionmode:SwitchPositionMode):
    return await switch_position_mode_f(positionmode)

############################################################################### Risk and Trade Settings:
@router.get("/risk/limit")
async def bybit_risk_limit(risk:RiskLimit):
    '''
    Example of switch_position_mode_f() 
        Input:
        - positionmode.category: "linear"
        - positionmode.symbol: "BTCUSDT"
        - positionmode.coin: "BTC"
        - positionmode.mode: 1  # 1 for dual mode, 0 for single mode
    '''
    return await get_risk_limit_f(risk)

############################################################################### websockets (Real-time Updates):

@router.post("/websocket")
async def start_listening(set: MarketPriceTicker):
    """Start listening to the Bybit WebSocket."""
    asyncio.create_task(listen_stream(set.symbol,set.category))
    return {"status": f"Started listening to WebSocket for {set.symbol}"}

@router.delete("/websocket")
async def stop_listening():
    """Stop listening to the Bybit WebSocket."""
    stop_event.set()
    await asyncio.sleep(2)
    stop_event.clear()
    return {"status": "Stopped listening to WebSocket."}

############################################################################### Market Data (Additional Functions):
@router.get("/market/funding_rate")
async def bybit_market_funding_rate(fundingrate:FundingRateHistory):
    '''
    Example of get_funding_rate_for_symbol_f() 
        Input:
        - fundingrate.category: "linear"
        - fundingrate.symbol: "BTCUSDT"
        - fundingrate.startTime: 1638316800  # Unix timestamp for the start time
        - fundingrate.endTime: 1638320400    # Unix timestamp for the end time
        - fundingrate.limit: 10              # Limit the number of records returned
    '''
    return await get_funding_rate_for_symbol_f(fundingrate)

@router.get("/market/exchange_info")
async def bybit_market_exchange_info(exchangeinfo:CoinExchangeRecord):
    '''
    Example of get_exchange_info_f() 
        Input:
        - exchangeinfo.fromCoin: "BTC"
        - exchangeinfo.toCOin: "USDT"
        - exchangeinfo.limit: 10
        - exchangeinfo.cursor: "abcd1234"
    '''
    return await get_exchange_info_f(exchangeinfo)

############################################################################### Miscellaneous/Utility:
@router.get("/server_time")
async def bybit_server_time():
    '''
    Example of get_server_time_f() 
        Input:
        None
    '''
    return await get_server_time_f()


