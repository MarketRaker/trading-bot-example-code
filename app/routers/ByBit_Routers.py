from fastapi import APIRouter
from app.crud.ByBit_CRUD import *
from app.models.Bybit_Models import *

router = APIRouter()




@router.get("/account")
async def binance_account():
    return await get_account_info()

@router.get("/account/balance")
async def binance_account_balance():
    return await get_account_funding_balance()

@router.post("/order/create")
async def create_order(order:PlaceOrderRequest):
    return await place_test_order(order.symbol,order.side,order.qty,order.category,order.orderType)
