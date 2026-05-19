from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'notification_type', 'status', 'sent_at', 'created_at']
        read_only_fields = ['id', 'status', 'sent_at', 'created_at']
