import base64
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
from django.conf import settings

def get_access_token():
    """
    Obtain an OAuth access token from Safaricom MPESA Daraja API.
    Uses basic authentication with consumer key and secret.
    """
    auth_url = f"{settings.MPESA_SANDBOX_URL}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    response.raise_for_status()
    access_token = response.json().get("access_token")
    return access_token

def lipa_na_mpesa_password():
    """
    Generate password and timestamp needed for STK Push request.
    Password = base64 encoded string of (BusinessShortCode + Passkey + Timestamp).

    Returns:
        password (str): Encoded password.
        timestamp (str): Current timestamp in required format.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data_to_encode = f"{settings.MPESA_BUSINESS_SHORT_CODE}{settings.MPESA_PASSKEY}{timestamp}"
    encoded_string = base64.b64encode(data_to_encode.encode('utf-8')).decode('utf-8')
    return encoded_string, timestamp
