from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

class Poem(models.Model):
    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('premium', 'Premium'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='poems')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    phone_number = PhoneNumberField(null=True, blank=True)  
    country = models.CharField(max_length=100, null=True, blank=True)  

class Image(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    alt_text = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class PasswordResetCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reset_codes')
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class Collaborator(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='collaborators')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collaborations')

class Friend(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friends')
    friend_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(auto_now_add=True)

class ActivityLog(models.Model):
    ACTIVITY_TYPE_CHOICES = (
        ('view', 'View'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('edit', 'Edit'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPE_CHOICES)
    target_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserSettings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    preference_key = models.CharField(max_length=100)
    preference_value = models.TextField()

class PaymentTransaction(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

class PoemTag(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='poem_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tagged_poems')

class CountryCurrency(models.Model):
    country_name = models.CharField(max_length=100)
    currency_code = models.CharField(max_length=10)
    currency_symbol = models.CharField(max_length=10)
