from fastapi import APIRouter, Request, HTTPException
from app.crud.MarketRaker_CRUD import *
router = APIRouter()

############################## Receive the indicator notifications from the MarketRaker API through the webhooks registered under your profile
@router.post("/notification")
async def webhook_endpoint(request: Request):
    try:
        # Parse the incoming JSON payload
        payload: dict = await request.json()

        # Process the payload (e.g., log it, validate it, or trigger other actions)
        ############################################################################## e.g. validate payload signature
        headers = request.headers
        xSign = headers.get("x-signature")
        is_valid: bool = verify_signature(payload, xSign, public_key_str)
        output: str = (
            "The signature is valid." if is_valid else "The signature is invalid."
        )
        print(output)

        ############################################################################## e.g. decide If a purchase should be make
        # Acceptable_Risk:int = 5
        # decision_maker(Acceptable_Risk, payload['risk'])
        # print(payload.get("risk"))
        ###############################################################################

        return
    except Exception as e:
        print(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")