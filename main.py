from fastapi import FastAPI, Header, Request
import stripe
import os
import uvicorn


app = FastAPI()

stripe.api_key = os.environ.get("STRIPE_API_KEY")
endpoint_secret = os.environ.get("ENDPOINT_SECRET")

@app.post("/webhook")
async def webhook(request: Request, stripe_signature:str = Header(None)):
    event = None
    data = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload = data, 
            sig_header = stripe_signature, 
            secret = endpoint_secret
        )
    except Exception as e:
        return{"error": str(e)}

    if event['type'] == 'payment_intent.succeeded':
      print(event['data']['object'])
    else:
      print('Unhandled event type {}'.format(event['type']))

    return {"status":"success"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)