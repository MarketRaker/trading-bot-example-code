from decouple import config
from fastapi import HTTPException
import hmac
import hashlib
import time
import httpx
import json
import requests


BYBIT_API_KEY = str(config("BYBIT_API_KEY"))
BYBIT_API_SECRET = str(config("BYBIT_API_SECRET"))
BYBIT_BASE_URL = str(config("BYBIT_BASE_URL"))

def create_bybit_signature(params: dict, api_secret: str) -> str:
    sorted_params = "&".join(f"{key}={value}" for key, value in sorted(params.items()))
    return hmac.new(api_secret.encode(), sorted_params.encode(), hashlib.sha256).hexdigest()


async def get_account_info():
    """
    Get wallet balance for Bybit account.
    """
    endpoint = "/v5/account/info"
    url = BYBIT_BASE_URL + endpoint
    timestamp = str(time.time() * 1000)
    
    # Request parameters
    payload={}

    headers = {
        'X-BAPI-API-KEY': BYBIT_API_KEY,
        'X-BAPI-TIMESTAMP': timestamp,
        'X-BAPI-SIGN': create_bybit_signature(payload, BYBIT_API_SECRET)
    }
    
    async with httpx.AsyncClient() as client:
        #response = await client.get(url,headers=headers, params=params)
        response = requests.request("GET",url,headers=headers,data=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            try:
                error_detail = response.json()
            except:
                error_detail = response.text or "No response content"
            raise HTTPException(status_code=response.status_code, detail=error_detail)
        

async def get_account_funding_balance():
    """
    Get wallet balance for Bybit account.
    """
    endpoint = "/v5/account/wallet-balance"
    url = BYBIT_BASE_URL + endpoint
    timestamp = int(time.time() * 1000)
    
    # Request parameters
    params = {
        "accountType": "UNIFIED",
        "api_key": BYBIT_API_KEY,
        "timestamp": timestamp,
    }
    params["sign"] = create_bybit_signature(params, BYBIT_API_SECRET)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            try:
                error_detail = response.json()
            except:
                error_detail = response.text or "No response content"
            raise HTTPException(status_code=response.status_code, detail=error_detail)



async def place_test_order(symbol: str, side: str, qty: str, category:str, order_type: str):
    """
    Place a test order on Bybit Spot Testnet
    """
    endpoint = "/v5/order/create"
    url = BYBIT_BASE_URL + endpoint
    timestamp = int(time.time() * 1000)


    params = {
        "category": category,
        "symbol": symbol,
        "side": side,
        "orderType": order_type,
        "qty": qty,
        #"timeInForce": "GTC",
        "timestamp": timestamp,
        "api_key": BYBIT_API_KEY
    }
    params["sign"] = create_bybit_signature(params, BYBIT_API_SECRET)

    headers = {
        'X-BAPI-API-KEY': BYBIT_API_KEY,
        'X-BAPI-TIMESTAMP': timestamp,
        'X-BAPI-SIGN': '223f7ec2c145264d39c5f025a9882f4f44d153a6e2a0bc7ac8f6d6d16331af41'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            try:
                error_detail = response.json()
            except:
                error_detail = response.text or "No response content"
            raise HTTPException(status_code=response.status_code, detail=error_detail)



