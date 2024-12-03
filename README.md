# trading-bot-example-code
MarketRaker AI A modular cryptocurrency trading bot framework that demonstrates MarketRaker AI webhook integration and common trading operations. To be used as a template.  







# BINANCE API INTEGRATION

## Table of Contents

1. [Introduction](#introduction)
2. [Account Management](#account-management)
3. [Market Data](#market-data)
4. [Placing & Managing Orders](#placing--managing-orders)
5. [Advanced Trading](#advanced-trading)
6. [Error Handling](#error-handling)
7. [Useful Tools](#useful-tools)


## Introduction

The Binance API allows you to interact programmatically with Binance's exchange. It provides access to various functionalities such as retrieving market data, placing orders, checking account balances, and managing trading positions. 

### Getting Started

-To begin using the Binance API, you'll need to:

1. Create an account on Binance (if you don't already have one).
2. Generate an API Key and Secret in the API Management section of your Binance account.
3. Store your API Key and Secret in the appropriate variables in the .env file  

-Authentication in the Binance API is done by using the *create_signature()* function. This signature needs to be added in the params section of every request that is send to the Binance API.



## Account Management

### Get Account Information
--- To retrieve your account information, including balances, assets, and account status: ---
**GET**: `/api/v3/account`
- Usage: Use this to fetch all balances for all coins in the account and basic account settings.

### Check Trading Status
--- Check if the account has been enabled for trading: ---
**GET**: `/api/v3/apiTradingStatus`
- Usage: Useful to verify the current trading status of your account before attempting to place orders.


## Market Data

### Get Current Average Price
--- Retrieve the average price of a symbol over the last 24 hours. ---
**GET**: `/api/v3/avgPrice`
- Usage: Useful for checking market prices for trading.

### Get Symbol Order Book (Depth)
--- Retrieve order book depth data (bid/ask prices and quantities). ---
**GET**: `/api/v3/depth`
- Usage: Useful for showing order book data (order depth) on the user interface.

### Get Symbol Price Ticker
--- Get the latest price for a symbol. ---
**GET**: `/api/v3/ticker/price`
- Usage: This is one of the most basic calls to fetch the current price for any symbol (e.g., BTCUSDT).

### Get 24-hour Price Change Statistics
--- Retrieve 24-hour price change statistics. ---
**GET**: `/v3/ticker/24hr`
- Usage: This endpoint will help you gather information like 24hr high/low, price change, and volume for a symbol.

### Get Historical Trades
--- Get the recent trades for a symbol (requires X-MBX-APIKEY). ---
**GET**: `/api/v3/historicalTrades`
- Usage: Useful for reviewing recent trade history.


## Placing & Managing Orders

### Place an Order:
--- Place a new order (LIMIT, MARKET, etc.). ---
**POST**: `/api/v3/order`
- Usage: You'll need this for placing both market and limit orders. You should include functionality for different order types (LIMIT, MARKET, STOP_LIMIT, etc.).

### Get All Open Orders:
--- Retrieve a list of all open orders for a given symbol. ---
**GET**: `/api/v3/openOrders`
- Usage: This is essential for checking which orders are still open for a symbol.

### Get Order Details:
--- Retrieve the status of a specific order using the orderId or clientOrderId. ---
**GET**: `/api/v3/order`
- Usage: This is critical for checking whether an order is open or has been filled.

### Cancel an Order:
--- Cancel a specific order by orderId or origClientOrderId. ---
**DELETE**: `/api/v3/order`
- Usage: For canceling open orders.


## Advanced Trading

## *Margin and Futures trading*

### Futures Account Information:
--- Retrieve information about your futures account, including balance and positions. ---
**GET**: `/fapi/v2/account`
- Usage: Use this to fetch all balances and positions for the account.

### Place Futures Order:
--- Place an order on the Binance Futures market. ---
**POST**: `/fapi/v1/order`
- Usage: You'll need this for futures trading (requires Futures API).

### Cancel Futures Order:
--- Cancel a specific futures order. ---
**DELETE**: `/fapi/v1/order`
- Usage: Use this to cancel futures orders.

### Get Futures Order History:
--- Retrieve the order history for your futures account. ---
**GET**: `/fapi/v1/allOrders`
- Usage: Useful for reviewing recent trade history.


## *Trading History & Information*

### Get All Orders:
--- Retrieve all orders for a specific symbol, including closed, filled, and canceled orders. ---
**GET**: `/api/v3/allOrders`
- Usage: Useful for retrieving the full history of orders for a symbol.

### Get Recent Trades:
--- Retrieve the recent trades (market or limit) made on a symbol. ---
**GET**: `/api/v3/trades`
- Usage: Useful for retrieving only recent history of orders for a symbol.


## *User Data Stream*

### Start User Data Stream:
--- Start a new user data stream for real-time order updates. ---
**POST**: `/api/v1/userDataStream`
- Usage: This is useful for getting live updates on orders and balances.

### Keepalive User Data Stream:
--- Keep the user data stream alive, used to refresh the connection. ---
**PUT**: `/api/v1/userDataStream`
- Usage: Ensure that the stream stays active.

### Close User Data Stream:
--- Close the user data stream. ---
**DELETE**: `/api/v1/userDataStream`
- Usage: Disconnect the stream when no longer needed.


## Error Handling

When encountering an error from the Binance API, The common respons is a JSON payload structured like this:
{
  "code":-1121,
  "msg":"Invalid symbol."
}

More Infomation can be found about the error you receive from the binance Docs, accessed by the following link:
https://binance-docs.github.io/apidocs/spot/en/#error-codes


## Useful Tools

### OCO (One Cancels Other) Orders
--- Place an OCO (One-Cancels-the-Other) order, which automatically cancels the other order if one is filled. ---
**POST**: `/api/v3/orderList`

### Get System Status
--- Retrieve the status of the Binance system, which is helpful for debugging. ---
**GET**: `/api/v3/systemStatus`








### 
---  ---
****: ``
- 







