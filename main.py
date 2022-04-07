from fastapi import FastAPI, Request, Header
import stripe
import os
import uvicorn
from pyairtable import Table


app = FastAPI()

stripe.api_key = os.environ.get("STRIPE_API_KEY")

@app.post("/webhook")
async def webhook(request: Request, stripe_signature: str = Header(None)):
    data = await request.body()
    endpoint_secret = os.environ.get("ENDPOINT_SECRET")
    print(data)
    print(stripe_signature)
    try:
        event = stripe.Webhook.construct_event(payload=data, sig_header=stripe_signature, secret=endpoint_secret)
        event_data = event['data']
    except Exception as e:
        print(e)
        return{"error": str(e)}

    if event['type'] == 'payment_intent.succeeded':
      print(event['data']['object'])
      print('success')
    else:
      print('Unhandled event type {}'.format(event['type']))

    return {"status":"success"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)