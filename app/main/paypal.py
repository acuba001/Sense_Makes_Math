from app import app, cache

import requests
import inspect
import paypalrestsdk

# PLease see: https://github.com/paypal/PayPal-Python-SDK/blob/master/README.md
paypalrestsdk.configure({
  'mode': app.config['PAYPAL_MODE'],
  'client_id': app.config['PAYPAL_CLIENT_ID'],
  'client_secret': app.config['PAYPAL_CLIENT_SECRET']
  })