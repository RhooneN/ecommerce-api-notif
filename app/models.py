from django.db import models

# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
    ]
    recipient = models.CharField(max_length=255)  # Email address or phone number
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')  # PENDING, SENT, FAILED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification {self.id} - {self.notification_type}"
