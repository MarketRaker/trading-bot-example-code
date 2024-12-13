from app.crud.Binance_CRUD import *
from app.crud.ByBit_CRUD import *


async def momentum_strategy(
    trading_pair: str,
    market_direction: str,
    percentage_change: float,
    leverage: int,
    buy_price: float,
    stoploss: float,
    trading_type: str,
):
    """
    Executes a momentum trading strategy based on market direction and percentage change.

    See README for more infomation about this strategy.

    Args:
        trading_pair (str): The trading pair for the order (e.g., 'BTCUSDT').
        market_direction (str): The market direction, either 'Bull' or 'Bear'.
        percentage_change (float): The predicted percentage change in the market to trigger the trade.
        leverage (int): The leverage to be used in the trade.
        buy_price (float): The price at which the order should be executed.
        stoploss (float): The stoploss price to limit potential losses.
        trading_type (str): The type of trade, either 'Long' or 'Short'.

    Returns:
        None: The function does not return any values. It executes a trade and monitors it.

    Raises:
        Exception: If an error occurs during the execution of the strategy or placing the order,
                   an exception is raised and logged.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        # Determine the trade side based on market direction and trading type
        if trading_type == "Long":
            if market_direction == "Bull" and percentage_change > 2:
                side = "BUY"  # Enter a long position if conditions are met
            else:
                print("Long trade conditions not met. No trade executed.")
                return

        elif trading_type == "Short":
            if market_direction == "Bear" and percentage_change < -2:
                side = "SELL"  # Enter a short position if conditions are met
            else:
                print("Short trade conditions not met. No trade executed.")
                return
        else:
            print("Invalid trading type. Trade not executed.")
            return

        # Get current price
        current_price_data = await get_binance_price_ticker(trading_pair)
        current_price = float(current_price_data["price"])

        # Check conditions and place an order
        if (side == "BUY" and current_price <= buy_price) or (
            side == "SELL" and current_price >= buy_price
        ):
            quantity = 1 / leverage  # Example quantity
            response = await Binance_place_order(
                symbol=trading_pair, side=side, quantity=quantity
            )
            print(f"Momentum trade executed: {response}")
            orderId = response["orderId"]

            # Use WebSocket to monitor exit conditions
            await listen_to_websocket(
                trading_pair, side, buy_price, stoploss, orderId, quantity
            )

        else:
            print("Price conditions not favorable for momentum trade entry.")

    except Exception as e:
        print(f"Error in momentum strategy: {e}")


async def overbought_oversold_strategy(
    trading_pair: str,
    market_direction: str,
    percentage_change_24h: float,
    leverage: int,
    stoploss: float,
    trading_type: str,
):
    """
    Executes a trading strategy based on overbought or oversold market conditions.

    See README for more infomation about this strategy.

    Args:
        trading_pair (str): The trading pair for the order (e.g., 'BTCUSDT').
        market_direction (str): The market direction, either 'Bull' or 'Bear'.
        percentage_change_24h (float): The predicted percentage change to come in the next 24 hours   
                                        to identify overbought or oversold conditions.
        leverage (int): The leverage to be used in the trade.
        stoploss (float): The stoploss price to limit potential losses.
        trading_type (str): The type of trade, either 'Long' or 'Short'.

    Returns:
        None: The function does not return any values. It executes a trade and monitors it.

    Raises:
        Exception: If an error occurs during the execution of the strategy or placing the order,
                   an exception is raised and logged.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        # Determine the trade side based on market direction and trading type
        if trading_type == "Long":
            # If market is bullish and there's a significant percentage change in the last 24 hours (overbought condition)
            if market_direction == "Bull" and percentage_change_24h > 5:
                side = "SELL"  # Enter a short position (SELL) to capitalize on reversal
            else:
                print("Long trade conditions not met. No trade executed.")
                return

        elif trading_type == "Short":
            # If market is bearish and there's a significant percentage change in the last 24 hours (oversold condition)
            if market_direction == "Bear" and percentage_change_24h < -5:
                side = "BUY"  # Enter a long position (BUY) to capitalize on reversal
            else:
                print("Short trade conditions not met. No trade executed.")
                return
        else:
            print("Invalid trading type. Trade not executed.")
            return

        # Fetch price stats and place order
        stats = await get_binance_24hr_price_change_stats(trading_pair)
        current_price = float(stats["lastPrice"])
        quantity = 1 / leverage
        response = await Binance_place_order(
            symbol=trading_pair, side=side, quantity=quantity
        )
        orderId = response["orderId"]
        print(f"Reversal trade executed: {response}")

        # Monitor exit conditions using WebSocket
        await listen_to_websocket(
            trading_pair, side, current_price, stoploss, orderId, quantity
        )

    except Exception as e:
        print(f"Error in overbought_oversold strategy: {e}")
