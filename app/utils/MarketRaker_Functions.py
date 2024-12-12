import base64
import json
import asyncio
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from decouple import config
from fastapi import Request, HTTPException
from app.utils.TradingBot import *


SIGNING_KEY = str(config("SIGNING_KEY"))
APPLICATION_ID = str(config("APPLICATION_ID"))
PUBLIC_KEY_STR = str(config("PUBLIC_KEY_STR"))
PUBLIC_KEY_STR = PUBLIC_KEY_STR.replace("\\n", "\n")


############################## Validate the indicator that was send from the marketraker api
def verify_signature(payload: json, signature: str, public_key_str: str) -> bool:
    """
    Verifies the signature of a payload.

    Parameters:
    - payload (json): The payload that was signed.
    - signature (str): The base64 encoded signature to verify.
    - public_key_str (str): The PEM formatted public key string.

    Returns:
    - bool: True if the signature is valid, False otherwise.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:
        payload_bytes: bytes = payload.encode("utf-8")
        signature_bytes: bytes = base64.b64decode(signature.encode("utf-8"))

        public_key = serialization.load_pem_public_key(
            public_key_str.encode("utf-8"), backend=default_backend()
        )

        public_key.verify(
            signature_bytes,
            payload_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        print(f"An error occurred during signature verification: {e}")
        return False


def change_USD_to_USDT(trading_pair: str):
    """
    Accepts a trading pair (str) as input and converts it to a standardized format.

    Parameters:
    - trading_pair (str): The trading pair to standardize. If the pair contains "USD", it will be converted to "USDT".

    Returns:
    - str: The standardized trading pair. This ensures compatibility with Binance and Bybit APIs.

    Last Reviewed Date:
        11 Dec 2024
    """
    if "USD" in trading_pair:
        trading_pair = trading_pair + "T"
        return trading_pair
    return trading_pair


def prepare_binance_trading_pair(trading_pair: str):
    """
    Converts a trading pair from MarketRaker's standard to Binance and Bybit's format.

    Parameters:
    - trading_pair (str): The trading pair to convert (e.g., "BTC/USD").

    Returns:
    - str: The converted trading pair (e.g., "BTCUSDT").

    Last Reviewed Date:
        11 Dec 2024
    """
    binance_prepared_trading_pair = trading_pair.replace("/", "").replace("_", "")
    binance_prepared_trading_pair = change_USD_to_USDT(binance_prepared_trading_pair)
    return binance_prepared_trading_pair


async def notification_type_indicator(request: Request):
    """
    Handles an incoming notification and processes the trading strategy based on the payload data.

    This function listens for a webhook notification, verifies the authenticity of the data using
    a provided signature, and then processes the data to execute multiple trading strategies
    depending on the market conditions. The payload can either be in string or dictionary format,
    and it will be parsed accordingly. The strategies include a momentum strategy and an overbought/oversold
    strategy, which are executed concurrently.

    Args:
        request (Request): The incoming HTTP request containing the webhook data, which includes
                            the trading indicator information in the request body.

    Returns:
        None: The function performs internal processing and does not return any data to the caller.

    Raises:
        HTTPException: If an error occurs during the processing of the webhook, an HTTPException
                       with status code 500 (Internal Server Error) is raised.

    Last Reviewed Date:
        11 Dec 2024
    """
    try:

        # Parse the incoming JSON payload
        response = await request.json()

        # Postman sends out an indicator in json form, but MarketRaker sends indicators in str form.
        # payload_str is mainly used for verification. Use payload_dict for easy access to indicator keys.

        if isinstance(response["data"], str):
            payload_dict: dict = json.loads(response["data"])
            payload_str = json.dumps(response)
        else:
            payload_dict: dict = response["data"]
            data_str = json.dumps(response["data"])
            payload_str = {"type": "indicator", "data": data_str}
            payload_str = json.dumps(payload_str)

        # verify indicator
        x_Sign = request.headers.get("x-signature")
        is_valid: bool = verify_signature(payload_str, x_Sign, PUBLIC_KEY_STR)
        verified: str = (
            "The signature is valid." if is_valid else "The signature is invalid."
        )
        print(verified)

        # Process the payload, add any functionality here:
        ##############################################################################

        # prepare the trading pair string for Binance API
        trading_pair = payload_dict["trading_pair"]
        binance_prepared_trading_pair = prepare_binance_trading_pair(trading_pair)

        # call all the trading strategies that the bot should implement.
        await asyncio.gather(
            momentum_strategy(
                binance_prepared_trading_pair,
                payload_dict["market_direction"],
                payload_dict["percentage_change"],
                payload_dict["leverage"],
                payload_dict["buy_price"],
                payload_dict["stoploss"],
                payload_dict["trading_type"],
            ),
            overbought_oversold_strategy(
                binance_prepared_trading_pair,
                payload_dict["market_direction"],
                payload_dict["percentage_change_24h"],
                payload_dict["leverage"],
                payload_dict["stoploss"],
                payload_dict["trading_type"],
            ),
        )

        return
    except Exception as e:
        print(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def notification_type_market_direction(request: Request):
    """
    Placeholder function for handling market direction notifications.

    This function is a placeholder that currently outputs a simple "Coming Soon!!!" message.
    It is intended to be implemented with functionality that processes market direction-related
    notifications in the future.

    Last Reviewed Date:
        11 Dec 2024
    """
    return print("Coming Soon!!!")
