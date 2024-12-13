# trading-bot-example-code
MarketRaker AI A modular cryptocurrency trading bot framework that demonstrates MarketRaker AI webhook integration and common trading operations. To be used as a template.  

# Table of Contents

1. [MarketRaker Table of Contents](#marketraker-table-of-contents)
2. [Binance Table of Contents](#binance-table-of-contents)
3. [Bybit Table of Contents](#bybit-table-of-contents)


# MARKETRAKER WEBHOOK INTEGRATION

## MarketRaker Table of Contents

1. [MarketRaker Introduction](#marketraker-introduction)
2. [Receiving Indicators](#receiving-indicators)
3. [Sending Test Notifications](#sending-test-notifications)
4. [Trading Bot Example](#trading-bot-example)

## MarketRaker Introduction


### Overview

Welcome to the **MarketRaker Webhook Integration** backend! This module is designed to provide an example of a possible integration between the **Binance** and **Bybit** APIs, and the **MarketRaker Webhook Indicators**. An example trading bot has been implemented for further clearification.

### Key Features

- **Webhook Handling**: The backend listens for incoming webhook notifications from various sources (e.g., trading signals, alerts, or strategies) to trigger automated trading actions.
  
- **Binance & Bybit Integration**: MarketRaker integrates with both Binance and Bybit APIs to interact with these exchanges, place orders, and manage trading positions.

- **Trade Bot Management**: The backend controls the trading bot, executing buy and sell operations based on incoming signals and predefined trading strategies.


### Architecture

- **FastAPI**: A fast, asynchronous web framework that powers the backend API, handling incoming webhook notifications and managing trades efficiently.
- **Binance & Bybit APIs**: These APIs allow interaction with the Binance and Bybit exchanges to place trades, check balances, and manage positions.
- **Webhook Notifications**: The backend listens for incoming webhooks and uses the data to trigger automated trading actions in real time.

### How It Works

1. **Webhook Reception**: The backend listens for webhook notifications that contain indicators.
2. **Data Processing**: The received data is parsed and validated.
3. **Trade Execution**: Based on the parsed data, the backend interacts with the Binance or Bybit API to place orders (buy/sell) based on momentum and overbought/oversold strategies.

**For More Infomation** go the the [MarketRaker Docs](https://app.raker.market/#/docs/introduction/introduction)

### Getting Started

To set up and run the **MarketRaker Webhook Integration** backend, follow these steps:

1. **Clone the repository**
  ```bash
  git clone https://github.com/MarketRaker/trading-bot-example-code
  ```
2. **Set up the Python environment**  
  Ensure you have **Python 3.x** installed. It is recommended to use a virtual environment for dependency management:
  - Create a virtual environment:
    ```bash
    python -m venv venv
    ```
  - Activate the virtual environment:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

3. **Install dependancies**
  Execute the following command in the terminal:
  ```bash
  pip install -r requirements.txt
  ```
4. **Configure environmental variables (`.env`)**
  - **MarketRaker**: Enter your Application ID and Signing ID as well as your verification key (public key). Adding "new lines"(\n) in the string might be required to keep your verification key in a single line.
  - **Binance & Bybit**: Enter your API key and secret in the appropriate fields in the `.env` file. Also Choose whether to use the testnet service by changing the base url of each service.

5. **Run the FastAPI Server**
  ```bash
  uvicorn app.main:app --reload --host 127.0.0.1 --port 5005
  ```


### Docker

This repository provides a **Dockerfile** to easily deploy the **MarketRaker Webhook Integration** backend. The Dockerfile ensures that the backend service is containerized and can be run consistently in any environment with Docker support.

## Docker Setup Instructions

Follow the steps below to build and run the **MarketRaker Webhook Integration** backend inside a Docker container.

### Prerequisites

Ensure that you have the following tools installed on your system:

- **Docker**: You can download Docker from the [official website](https://www.docker.com/get-started).
- **Configure Environment Variables**: Before building the Docker image, ensure that you have a `.env` file in the root of the repository with the appropriate environment variables for your trading bot and API keys. The `.env` file should contain sensitive information such as API keys for Binance and Bybit.

### Setup
- **Build the Docker Image**:
  Run the following command to build the Docker image from the `Dockerfile`:
  ```bash
  docker build -t trading-bot-example-code .
  ```
  This will:
  - Set up a Python 3.13 slim container.
  - Install dependencies from `requirements.txt`.
  - Copy the `.env` file and application code to the container.
  - Expose port `5005` (default backend port).

- **Run the Docker Container**:
  Once the image is built, you can run the container with the following command:
  ```bash
  docker run -d -p 5005:5005 trading-bot-example-code
  ```
  This will:
  - Run the container in the background (-d).
  - Forward the backend's port 5005 to your local machine's port 5005 (-p 5005:5005).

Your FastAPI backend will now be accessible at http://localhost:5005.

**Note:**  
For testing, Postman can interact with your FastAPI server on localhost, but because localhost is not a public IP address, it cannot be registered as a webhook URL on the MarketRaker website. MarketRaker needs a publicly accessible endpoint to send indicators to your application.  
To make your application accessible publicly, you would need to deploy it to a server with a public IP address (e.g., on a cloud service like AWS, Azure, or Heroku)


## Receiving Indicators

### Indicator Format

In this system, trading indicators will follow a specific JSON structure to ensure consistency and clarity. The indicator data will be encapsulated in an object with the following format:

```json
{
  "type": "indicator",
  "data": {
    "trading_type": "Long", 
    "leverage": 1, 
    "buy_price": 205.0, 
    "sell_price": 215.0, 
    "buy_date": 1733913000, 
    "sell_prediction_date": 1733999400, 
    "risk": 4, 
    "market_direction": "Bull", 
    "percentage_change": 5.1, 
    "stoploss": 200, 
    "trading_type_24h": null, 
    "percentage_change_24h": -1.5, 
    "risk_24h": 5, 
    "leverage_24h": 2, 
    "stoploss_24h": 190, 
    "trading_pair": "SOL/USD"
  }
}
```

### Verify Signature
--- To verify the signature of a given payload: ---  
**Function**: `verify_signature(payload: json, signature: str, public_key_str: str) -> bool`
- Usage: Use this function to check the validity of a signature against a payload and a public key.
- Parameters:
  - `payload (json)`: The payload that was signed.
  - `signature (str)`: The base64 encoded signature to verify.
  - `public_key_str (str)`: The PEM formatted public key string.
- Returns:
  - `bool`: Returns `True` if the signature is valid, otherwise `False`.

### Notification Type Indicator
--- To handle an incoming notification and process trading strategies based on the payload data: ---  
**Function**: `notification_type_indicator(request: Request)`
- Usage: Use this function to listen for webhook notifications, verify the authenticity of the data, and process trading strategies based on the market conditions.
- Parameters:
  - `request (Request)`: The incoming HTTP request containing webhook data with trading indicator information in the request body.
- Returns:
  - `None`: Performs internal processing without returning data.
- Key Features:
  - Parses payload data (string or dictionary format).
  - Verifies authenticity using a provided signature.
  - Prepares trading pairs for Binance API.
  - Executes multiple trading strategies concurrently (e.g., momentum, overbought/oversold).
- Raises:
  - `HTTPException`: Raised with status code 500 if an error occurs during webhook processing.

### Notification Type Market Direction
--- Placeholder function for handling market direction notifications: ---  
**Function**: `notification_type_market_direction(request: Request)`
- Usage: Currently a placeholder function. Intended to process market direction-related notifications in future implementations.
- Parameters:
  - `request (Request)`: The incoming HTTP request for market direction notifications.
- Returns:
  - Outputs a "Coming Soon!!!" message to indicate future implementation.
- Key Features:
  - Serves as a placeholder for upcoming functionality.



## Sending Test Notifications

### Postman Requests for MarketRaker API

This repository contains a collection of Postman requests designed for testing the **MarketRaker Webhook Integrations**. The requests simulate various trading scenarios and market conditions to help developers validate and enhance the API's functionality. 

Each request targets specific aspects of the API, such as trading types, leverage settings, market conditions, and risk levels. The collection is structured to provide clear and concise test cases that demonstrate expected outcomes and API responses.

### Features
- Pre-built Postman requests covering diverse test scenarios.
- Includes headers and payloads required for API interaction.
- Configurable to test custom scenarios by modifying payloads (Using custom scenarios require the deactivation of request validation).
- Useful for debugging and enhancing the robustness of the MarketRaker API.

### Purpose
The purpose of this collection is to:
1. Provide a reliable testing framework for developers.
2. Validate API responses under varying trading and market conditions.
3. Identify potential edge cases or inconsistencies in API behavior.

### Prerequisites
Before using this collection:
1. Ensure the MarketRaker API is running locally or on the designated server.
2. Import the collection into your Postman workspace.
3. Verify that the required `x-signature` header is configured and matches your API's authentication mechanism.

### Quick Start
1. Clone or download this repository.
2. Import the Postman collection file into Postman.
3. Configure the base URL in Postman to point to your local API endpoint (default: `http://localhost:5005/marketraker/notification`).
4. Start testing the provided requests or create new ones by modifying the payloads.

This collection provides a structured and efficient way to test the MarketRaker API, ensuring reliable and accurate functionality for all supported scenarios.




## Trading Bot Example

This **trading bot** serves as a sample implementation of how an automated trading bot can be set up using a FastAPI backend integrated with the **Binance** and **Bybit** APIs.

This bot is designed to demonstrate two popular trading strategies:
1. **Momentum Strategy**: A strategy that places a trade based on market momentum, utilizing market direction and percentage change.
2. **Overbought/Oversold Strategy**: A strategy that executes a trade when the market shows signs of being overbought or oversold based on recent price changes.



## Overview

The **MarketRaker Test Trading Bot** works by connecting to Binance's API and using specific strategies to execute trades automatically. The strategies are triggered when certain market conditions are met, and trades are monitored in real-time via WebSockets.

### Key Features

- **Momentum Strategy**: Executes trades based on a combination of market direction (Bull or Bear) and percentage change.
- **Overbought/Oversold Strategy**: Places trades when the market will be overbought or oversold, based on the predicted percentage change in 24 hours.
- **Real-Time Monitoring**: After placing the trade, the bot uses WebSockets to monitor the trade and ensure it exits according to the defined conditions (e.g., stop loss or target price).
- **Leverage & Stoploss Support**: Customizable leverage and stoploss values for each trade to manage risk.

## Strategies

### 1. Momentum Strategy

The **Momentum Strategy** is designed to trade based on the market's momentum. It follows these steps:

- **Bull Market + Long Trade**: If the market is bullish and the percentage change is greater than 2%, the bot enters a **BUY** (Long) trade.
- **Bear Market + Short Trade**: If the market is bearish and the percentage change is less than -2%, the bot enters a **SELL** (Short) trade.
- The bot monitors the trade and adjusts based on the stoploss or target price using WebSockets.

### 2. Overbought/Oversold Strategy

The **Overbought/Oversold Strategy** is based on identifying market conditions where a reversal is likely, either due to the market being overbought (when the price has increased rapidly) or oversold (when the price has decreased rapidly). This strategy uses the predicted percentage change of the comming 24 hours to identify these conditions and take action accordingly.

#### How It Works:

- **Bull Market + Overbought**: If the market is bullish and the predicted percentage change to come exceeds a certain threshold (e.g., > 5%), it indicates that the market might be overbought. In this case, the bot will **SELL** (Short) to capitalize on a potential price reversal.
  
- **Bear Market + Oversold**: If the market is bearish and the predicted percentage change to come is below a certain threshold (e.g., < -5%), it indicates that the market might be oversold. In this case, the bot will **BUY** (Long) to take advantage of a potential price reversal.

The bot then places the order (BUY or SELL) and monitors it via WebSocket, tracking the stoploss and exit conditions.



# BINANCE API INTEGRATION
This section gives the routes that can be used to call and test API functions used for the **Binance** API. It is recommended that these functions be used for **testing purposes**. The functions these routes call can directly be used when implementing your own trading bot.

## Binance Table of Contents

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

**For More Infomation** go the the [Binance API Docs](https://binance-docs.github.io/apidocs/spot/en/#change-log)


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
This section gives the routes that can be used to call and test API functions used for the **Bybit** API. It is recommended that these functions be used for **testing purposes**. The functions these routes call can directly be used when implementing your own trading bot.

## Bybit Table of Contents

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

**For More Infomation** go to the [Bybit API Docs](https://bybit-exchange.github.io/docs/v5/intro)
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

