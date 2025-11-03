from django.contrib import admin
from .models import (
    Poem, Image, Comment, Like, Favorite, Follow, Notification,
    PasswordResetCode, Collaborator, Friend, ActivityLog, UserSettings,
    PaymentTransaction, Tag, PoemTag, CountryCurrency
)

admin.site.register(Poem)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(Notification)
admin.site.register(PasswordResetCode)
admin.site.register(Collaborator)
admin.site.register(Friend)
admin.site.register(ActivityLog)
admin.site.register(UserSettings)
admin.site.register(PaymentTransaction)
admin.site.register(Tag)
admin.site.register(PoemTag)
admin.site.register(CountryCurrency)
