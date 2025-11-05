# Django Mpesa Integration (STK Push, Query, and Callback)

This Django app integrates **Safaricom M-Pesa Daraja API** to perform **STK Push**, **Query Transaction Status**, and handle **Callback Responses**.  
It provides a clean, modular implementation for M-Pesa payments in Django-based systems.

---

## Features

- Automatic OAuth Access Token generation
- **STK Push** payment initiation
- **Transaction Status Query** support
- **Callback** response handling
- Built for the **Sandbox** environment and easily configurable for production

---

## 🧱 Project Structure

```
mpesa_app/
│
├── stkPush.py              # Handles M-Pesa STK Push request
├── query_stk.py            # Handles STK push query status
├── callback.py             # Handles M-Pesa callback responses
└── generateAccessToken.py  # Fetches OAuth access token from Safaricom Daraja API
```

---

## ⚙️ Requirements

- Python 3.10+
- Django 4+
- `requests` library

Install dependencies:

```bash
pip install django requests
```

---

## 🔑 Configuration

### 1. Safaricom Developer Setup

- Sign up on [Safaricom Developer Portal](https://developer.safaricom.co.ke/)
- Create an app and obtain:
  - **Consumer Key**
  - **Consumer Secret**
- Use the **Sandbox** environment during testing.

### 2. Environment Variables (Recommended)

Create a `.env` file or use Django’s settings to securely store credentials:

```bash
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
MPESA_CALLBACK_URL=https://yourdomain.com/callback
```

Then load them using `os.environ.get()` within your Python files.

---

## 🧩 Endpoints Overview

| Endpoint         | Method | Description                         |
| ---------------- | ------ | ----------------------------------- |
| `/access-token/` | `GET`  | Generates OAuth token               |
| `/stk-push/`     | `POST` | Initiates an STK push request       |
| `/stk-query/`    | `POST` | Queries STK push transaction status |
| `/callback/`     | `POST` | Handles M-Pesa callback response    |

---

## 🧠 How It Works

### 1. Generate Access Token

`generateAccessToken.py` authenticates using your consumer credentials and returns a valid access token.

Example response:

```json
{
  "access_token": "ACCESS_TOKEN_STRING"
}
```

---

### 2. Initiate STK Push

`stkPush.py` sends an STK push request to a customer’s phone.  
They’ll receive a prompt to enter their M-Pesa PIN.

Example request:

```bash
POST /stk-push/
```

Response example:

```json
{
  "CheckoutRequestID": "ws_CO_31102025124418368724966576",
  "ResponseCode": "0"
}
```

---

### 3. Query Transaction Status

`query_stk.py` checks the result of a previous STK push using its CheckoutRequestID.

Example request:

```bash
POST /stk-query/
```

Response example:

```json
{
  "message": "0 The transaction was successful"
}
```

**Common Result Codes:**

- `0` — Transaction successful
- `1` — Insufficient balance
- `1032` — User cancelled the transaction
- `1037` — Timeout
- Others — Unknown result

---

### 4. Handle Callback

`callback.py` processes the asynchronous callback from Safaricom and logs the data in `Mpesastkresponse.json`.

Example callback:

```json
{
  "Body": {
    "stkCallback": {
      "MerchantRequestID": "29115-34620561-1",
      "CheckoutRequestID": "ws_CO_31102025124418368724966576",
      "ResultCode": 0,
      "ResultDesc": "The service request is processed successfully.",
      "CallbackMetadata": {
        "Item": [
          { "Name": "Amount", "Value": 1.0 },
          { "Name": "MpesaReceiptNumber", "Value": "NLJ7RT61SV" },
          { "Name": "TransactionDate", "Value": 20251031125005 },
          { "Name": "PhoneNumber", "Value": 254724966576 }
        ]
      }
    }
  }
}
```

---

## 🧰 Example URL Configuration

```python
from django.urls import path
from . import stkPush, query_stk, callback, generateAccessToken

urlpatterns = [
    path('access-token/', generateAccessToken.get_access_token, name='access_token'),
    path('stk-push/', stkPush.initiate_stk_push, name='stk_push'),
    path('stk-query/', query_stk.query_stk_status, name='stk_query'),
    path('callback/', callback.process_stk_callback, name='stk_callback'),
]
```

---

## 🧪 Testing in Sandbox

1. Log in to the [M-Pesa Sandbox Portal](https://sandbox.safaricom.co.ke/)
2. Use the following test details:
   - Paybill: `174379`
   - Phone Number: `254708374149`
3. Run the Django server and trigger an STK push — you’ll receive a simulated response.

---

## 🛡️ Notes & Best Practices

- **Never** expose your credentials or passkey publicly.
- Use **HTTPS** for your callback URL in production.
- Implement persistent storage for transaction logs and results.
- Switch API URLs from sandbox to production when going live.

---

## 📄 License

MIT License  
© 2025 Austin Musuya

---

## 👨‍💻 Author

**Austin Musuya**  
Backend Developer | AI & Payment Systems Enthusiast  
🔗 [https://austinmusuya.dev](https://austinmusuya.dev)
