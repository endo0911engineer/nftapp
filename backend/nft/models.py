from django.db import models

class Gift(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    sender_address = models.CharField(max_length=255)
    recipient_address = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    nft_url = models.URLField(max_length=500)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gift form {self.sender_address} to {self.recipient_address}"

class User(models.Model):
    wallet_address = models.CharField(max_length=42, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wallet_address