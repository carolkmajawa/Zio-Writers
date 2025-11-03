from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .utils import get_access_token, lipa_na_mpesa_password
from rest_framework import generics, permissions, status
from .models import Poem, PaymentTransaction
from .serializers import PoemSerializer, PaymentTransactionSerializer
import requests

class LipaNaMpesaStkPush(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        amount = request.data.get("amount")

        if not phone_number or not amount:
            return Response({"error": "phone_number and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mpesa_sandbox_url = settings.MPESA_SANDBOX_URL
            mpesa_business_shortcode = settings.MPESA_BUSINESS_SHORT_CODE

            access_token = get_access_token()
            password, timestamp = lipa_na_mpesa_password()

            api_url = f"{mpesa_sandbox_url}/mpesa/stkpush/v1/processrequest"

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "BusinessShortCode": mpesa_business_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": phone_number,
                "PartyB": mpesa_business_shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": settings.MPESA_CALLBACK_URL,
                "AccountReference": "Order123",
                "TransactionDesc": "Payment of order"
            }

            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()

            return Response(response.json(), status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as http_err:
            return Response({"error": f"HTTP error occurred: {http_err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PoemCreateView(generics.CreateAPIView):
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PoemListView(generics.ListAPIView):
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentTransactionView(generics.ListCreateAPIView):
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
