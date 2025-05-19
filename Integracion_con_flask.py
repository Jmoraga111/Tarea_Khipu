from flask import Flask, request, redirect, url_for
import requests
import os

app = Flask(__name__)

KHIPU_API_KEY = os.environ.get('APIKEY')
KHIPU_PAYMENTS_URL = "https://payment-api.khipu.com/v3/payments"

@app.route('/initiate_payment')
def initiate_payment():
    # Generate the webhook URL *within* the application context
    webhook_url = url_for('webhook_listener', _external=True)

    payload = {
        "amount": 1000,
        "currency": "CLP",
        "subject": "Cobro de prueba",
        "return_url": url_for('payment_success', _external=True),
        "cancel_url": url_for('payment_cancelled', _external=True),
        "webhook_url": webhook_url
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": KHIPU_API_KEY
    }
    response = requests.post(KHIPU_PAYMENTS_URL, json=payload, headers=headers)
    data = response.json()
    payment_id = data.get('payment_id')
    return redirect(data['payment_url'])

@app.route('/payment_success')
def payment_success():
    return "Payment successful!"

@app.route('/payment_cancelled')
def payment_cancelled():
    return "Payment cancelled."

@app.route('/webhook_listener', methods=['POST'])
def webhook_listener():
    data = request.form
    payment_id = data.get('payment_id')
    status = data.get('status')
    print(f"Webhook received for payment ID: {payment_id}, Status: {status}")
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)