# from rest_framework import serializers
# from .models import Poem, PaymentTransaction, UserSettings  # Add more serializers as needed

# class PoemSerializer(serializers.ModelSerializer):
#     author = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = Poem
#         fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'visibility', 'price', 'currency', 'is_deleted']
#         read_only_fields = ['id', 'created_at', 'updated_at']

# from rest_framework import serializers
# from .models import PaymentTransaction

# class PaymentTransactionSerializer(serializers.ModelSerializer):
#     buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())

#     class Meta:
#         model = PaymentTransaction
#         fields = ['id', 'buyer', 'poem', 'amount', 'currency', 'payment_status', 'created_at']
#         read_only_fields = ['id', 'created_at']


# class UserSettingsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserSettings
#         fields = '__all__'

from rest_framework import serializers
from .models import Poem, PaymentTransaction, UserSettings

class PoemSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    phone_number = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Poem
        fields = [
            'id', 'author', 'title', 'content', 'created_at', 'updated_at',
            'visibility', 'price', 'currency', 'is_deleted',
            'phone_number', 'country'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        visibility = data.get('visibility', 'public')
        phone = data.get('phone_number')
        country = data.get('country')
        
        # Require phone and country only if premium poem
        if visibility == 'premium':
            if not phone:
                raise serializers.ValidationError({"phone_number": "Phone number is required for premium poems."})
            if not country:
                raise serializers.ValidationError({"country": "Country is required for premium poems."})
        return data


class PaymentTransactionSerializer(serializers.ModelSerializer):
    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PaymentTransaction
        fields = ['id', 'buyer', 'poem', 'amount', 'currency', 'payment_status', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'
