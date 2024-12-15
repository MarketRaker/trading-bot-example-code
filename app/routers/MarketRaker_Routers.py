from fastapi import APIRouter, Request, HTTPException
from app.utils.MarketRaker_Functions import *


router = APIRouter()


############################## Receive the indicator notifications from the MarketRaker API through the webhooks registered under your profile
@router.post("/notification")
async def webhook_endpoint(request: Request):
    """
    Webhook endpoint for processing different types of notifications.

    This function handles incoming POST requests at the "/notification" endpoint.
    It processes the request payload, determines the notification type, and
    delegates the processing to the corresponding function. Currently, it supports
    two types of notifications: "indicator" and "market_direction".

    Based on the notification type, the function calls the appropriate handler:
    - "indicator" triggers the `notification_type_indicator` function.
    - "market_direction" triggers the `notification_type_market_direction` function.

    Args:
        request (Request): The incoming HTTP request containing the notification payload.

    Returns:
        None: The function performs internal processing and does not return any data to the caller.

    Raises:
        HTTPException: If an error occurs during the processing of the webhook,
            an HTTPException with status code 500 (Internal Server Error) is raised.

    Last Reviewed Date:
        11 Dec 2024
    """
    response = await request.json()
    try:
        match response["type"]:

            case "indicator":
                await notification_type_indicator(request)

            case "market_dircetion":
                await notification_type_market_direction(request)

    except Exception as e:
        print(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
