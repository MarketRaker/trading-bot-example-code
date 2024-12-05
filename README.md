# trading-bot-example-code
MarketRaker AI A modular cryptocurrency trading bot framework that demonstrates MarketRaker AI webhook integration and common trading operations. To be used as a template.  


# MARKETRAKER WEBHOOK INTEGRATION

## Table of Contents

1. [MarketRaker Introduction](#marketraker-introduction)
2. [Receiving Indicators](#receiving-indicators)
3. [Sending Test Notifications](#sending-test-notifications)

## MarketRaker Introduction

## Receiving Indicators

## Sending Test Notifications




# BINANCE API INTEGRATION

## Table of Contents

1. [Binance Introduction](#Binance-introduction)
2. [Account Management](#account-management)
3. [Market Data](#market-data)
4. [Placing & Managing Orders](#placing--managing-orders)
5. [Advanced Trading](#advanced-trading)
6. [Error Handling](#error-handling)
7. [Useful Tools](#useful-tools)


## Binance Introduction

The Binance API allows you to interact programmatically with Binance's exchange. It provides access to various functionalities such as retrieving market data, placing orders, checking account balances, and managing trading positions. 

### Getting Started

-To begin using the Binance API, you'll need to:

1. Create an account on Binance (if you don't already have one).
2. Generate an API Key and Secret in the API Management section of your Binance account.
3. Store your API Key and Secret in the appropriate variables in the .env file  
4. **Configure your url**: The base urls in the `.env` file have 2 posibilities, a production url and a testnet url. Use the production url for trades, and the testnet url for testing functions. If you want to test functions, ensure you have created a Binance testnet account. 

-Authentication in the Binance API is done by using the *create_signature()* function. This signature needs to be added in the params section of every request that is send to the Binance API.



## Account Management

### Get Account Information
--- To retrieve your account information, including balances, assets, and account status: ---
**GET**: `/account`
- Usage: Use this to fetch all balances for all coins in the account and basic account settings.

### Check Trading Status
--- Check if the account has been enabled for trading: ---
**GET**: `/tradingStatus`
- Usage: Useful to verify the current trading status of your account before attempting to place orders.


## Market Data

### Get Current Average Price
--- Retrieve the average price of a symbol over the last 24 hours. ---
**GET**: `/avgPrice`
- Usage: Useful for checking market prices for trading.

### Get Symbol Order Book (Depth)
--- Retrieve order book depth data (bid/ask prices and quantities). ---
**GET**: `/orderBook`
- Usage: Useful for showing order book data (order depth) on the user interface.

### Get Symbol Price Ticker
--- Get the latest price for a symbol. ---
**GET**: `/priceTicker`
- Usage: This is one of the most basic calls to fetch the current price for any symbol (e.g., BTCUSDT).

### Get 24-hour Price Change Statistics
--- Retrieve 24-hour price change statistics. ---
**GET**: `/priceChangeStats`
- Usage: This endpoint will help you gather information like 24hr high/low, price change, and volume for a symbol.

### Get Historical Trades
--- Get the recent trades for a symbol (requires X-MBX-APIKEY). ---
**GET**: `/historicalTrades`
- Usage: Useful for reviewing recent trade history.


## Placing & Managing Orders

### Place an Order:
--- Place a new order (LIMIT, MARKET, etc.). ---
**POST**: `/order`
- Usage: You'll need this for placing both market and limit orders. You should include functionality for different order types (LIMIT, MARKET, STOP_LIMIT, etc.).

### Get All Open Orders:
--- Retrieve a list of all open orders for a given symbol. ---
**GET**: `/allOpenOrders`
- Usage: This is essential for checking which orders are still open for a symbol.

### Get Order Details:
--- Retrieve the status of a specific order using the orderId or clientOrderId. ---
**GET**: `/orderDetails`
- Usage: This is critical for checking whether an order is open or has been filled.

### Cancel an Order:
--- Cancel a specific order by orderId or origClientOrderId. ---
**DELETE**: `/cancelOrder`
- Usage: For canceling open orders.


## Advanced Trading


## *Trading History & Information*

### Get All Orders:
--- Retrieve all orders for a specific symbol, including closed, filled, and canceled orders. ---
**GET**: `/allOrders`
- Usage: Useful for retrieving the full history of orders for a symbol.

### Get Recent Trades:
--- Retrieve the recent trades (market or limit) made on a symbol. ---
**GET**: `/recentTrades`
- Usage: Useful for retrieving only recent history of orders for a symbol.


## *User Data Stream*

### Start User Data Stream:
--- Start a new user data stream for real-time order updates. ---
**POST**: `/startUserDataStream`
- Usage: This is useful for getting live updates on orders and balances.

### Keepalive User Data Stream:
--- Keep the user data stream alive, used to refresh the connection. ---
**PUT**: `/keepUserDataStreamAlive`
- Usage: Ensure that the stream stays active.

### Close User Data Stream:
--- Close the user data stream. ---
**DELETE**: `/closeUserDataStream`
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
**POST**: `/ocoOrder`

### Get Server TIme
--- Retrieve the time of the Binance system, which is helpful for debugging. ---
**GET**: `/serverTime`





# Bybit API Documentation

## Table of Contents

1. [Bybit Introduction](#bybit-introduction)
2. [Account and Wallet Management](#account-and-Wallet-management)
3. [Order Management](#order-management)
4. [Market Data](#bybit-market-data)
5. [Position Management](#position-management)
6. [Risk Settings](#risk-settings)
7. [User Data Stream](#user-data-stream-real-time-updates)
8. [Miscellaneous/Utility](#miscellaneousutility)



## Bybit Introduction

The Bybit API allows you to programmatically interact with Bybit's exchange, enabling access to a wide range of features such as retrieving market data, placing and managing orders, checking account balances, and managing trading positions.

### Getting Started

To begin using the Bybit API, you'll need to:

1. **Create an Account**: Sign up for a Bybit account if you don’t already have one.
2. **Generate API Keys**: Navigate to the API Management section of your Bybit account to generate an API Key and Secret. Be sure to grant the appropriate permissions (read, trade, etc.) for your API Key.
3. **Secure Your API Keys**: Store your API Key and Secret in the environment file (`.env`), to prevent unauthorized access.
4. **Configure your url**: The base urls in the `.env` file have 2 posibilities, a production url and a testnet url. Use the production url for trades, and the testnet url for testing functions. If you want to test functions, ensure you have created a Bybit testnet account.    

**Authentication**: Bybit API requests requiring authentication must include a properly signed request. This authentication is done automatically when using the *pybit* library.

---

## Account and Wallet Management:

### Get Account Information
--- Retrieve detailed information about the user's account, including account status and balances. ---
**GET**: `/account/info`
- Usage: Retrieve details about the user's account such as balance, leverage, and more.

### Get Wallet Balance
--- Get the balance of the user's wallet for a specific asset. ---
**GET**: `/account/wallet`
- Usage: Request the wallet balance for a specific symbol (e.g., BTC, USDT).

### Get Account Funding
--- Retrieve funding details for the user's account, such as account status and available margin. ---
**GET**: `/account/funding`
- Usage: Get the funding status for the user's account.

### Get User’s Trading Fee
--- Retrieve the trading fees for the user on the Bybit platform. ---
**GET**: `/account/tradingFee`
- Usage: Fetch the current trading fee schedule for the user.

---

## Order Management:

### Place an Order (Limit/Market)
--- Place a new order for a specific symbol, either a limit or market order. ---
**POST**: `/order/create`
- Usage: Place a limit or market order for a given symbol with specified price and quantity.

### Cancel an Order
--- Cancel an open order for a specific symbol. ---
**POST**: `/order/cancel`
- Usage: Cancel an existing order using its order ID.

### Get Order Details
--- Retrieve details about a specific order by providing its order ID. ---
**GET**: `/order`
- Usage: Get details of a single order, including status and filled amount.

### Modify an Order
--- Modify an existing order (typically used for limit orders). ---
**POST**: `/order/amend`
- Usage: Change an existing order's price or other details, such as quantity.

---

## Bybit Market Data:

### Get Market Price Ticker
--- Get the latest price of a symbol on the Bybit market. ---
**GET**: `/market/ticker_price`
- Usage: Retrieve the latest market ticker for a specified symbol (e.g., BTCUSDT).

### Get 24-Hour Price Change
--- Get the 24-hour price change statistics for a symbol. ---
**GET**: `/market/price_change`
- Usage: Get the 24-hour price change, volume, and other metrics for a symbol.

### Get Kline (OHLCV) Data
--- Get Kline (OHLCV) data for a symbol at specific intervals. ---
**GET**: `/market/kline`
- Usage: Request Kline data for a symbol, specifying the interval (e.g., 1m, 5m, 1h).

### Get Symbol Order Book (Depth)
--- Retrieve the current order book for a specific symbol. ---
**GET**: `/market/symbol_orderbook`
- Usage: Retrieve the order book for a given symbol with price and volume information.

### Get Recent Trades
--- Get the most recent trades for a symbol. ---
**GET**: `/market/recent_trades`
- Usage: Fetch the most recent trade history for a given symbol.

### Get Funding Rate for a Symbol
--- Retrieve the funding rate for a futures contract. ---
**GET**: `/market/funding_rate`
- Usage: Get the previous funding rate for a specific symbol.

### Get Exchange Info
--- Retrieve the exchange information, such as supported symbols, trading rules, etc. ---
**GET**: `/market/exchange_info`
- Usage: Get detailed information about the exchange, including available trading pairs and limits.

---

## Position Management:

### Get Position Information
--- Retrieve position information for futures trading. ---
**GET**: `/position/info`
- Usage: Get the user's current position for futures trading, including size and margin.

### Create Leverage for a Position
--- Set the leverage for a futures position. ---
**POST**: `/position/leverage`
- Usage: Set or change the leverage for a specific position.

### Switch Position Mode
--- Switch the current position mode (single or multi). ---
**POST**: `/position/mode`
- Usage: Switch the current position mode (either single or multi).

---

## Risk Settings:

### Get Risk Limits
--- Get the risk limits for the futures trading account. ---
**GET**: `/risk/limit`
- Usage: Retrieve the risk limits, including margin requirements and position limits.

---

## User Data Stream (Real-time Updates):

### Start User Data Stream
--- Start a user data stream for real-time updates on order status, account status, and more. ---
**POST**: `/websocket`
- Usage: Start the user data stream to receive real-time updates.


### Close User Data Stream
--- Close the user data stream and stop receiving updates. ---
**DELETE**: `/websocket`
- Usage: Stop the user data stream to halt receiving updates.

---

## Miscellaneous/Utility:

### Get Server Time
--- Get the server time of the Bybit API. ---
**GET**: `/server_time`
- Usage: Retrieve the current server time from the Bybit API to synchronize requests.

