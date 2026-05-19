from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from .models import Notification
from .serializers import NotificationSerializer
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings

from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})

TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', )
TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', )
TWILIO_PHONE_NUMBER = getattr(settings, 'TWILIO_PHONE_NUMBER', )

class NotificationView(APIView):
    permission_classes = []
    queryset = Notification.objects.all()
	
    def post(self, request):
        """
        Create a notification (email or SMS) and send it.
        """
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save()

            try:
                if notification.notification_type == 'EMAIL':
                    # Simulate email sending (use a service like SendGrid in production)
                    send_mail(
                        subject="Notification",
                        message=notification.message,
                        from_email="honoredesoke@gmail.com",
                        recipient_list=[notification.recipient],
                    )
                elif notification.notification_type == 'SMS':
                    # Simulate SMS sending (use Twilio for production)
                    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                    client.messages.create(
                        body=notification.message,
                        from_=TWILIO_PHONE_NUMBER,
                        to=notification.recipient,
                    )
                else:
                    return Response({"error": "Invalid notification type."}, status=status.HTTP_400_BAD_REQUEST)

                notification.status = 'SENT'
                notification.sent_at = now()
                notification.save()
                return Response(NotificationSerializer(notification).data, status=status.HTTP_201_CREATED)

            except Exception as e:
                notification.status = 'FAILED'
                notification.save()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Retrieve all notifications or filter by recipient.
        """
        recipient_filter = request.query_params.get('recipient')
        if recipient_filter:
            notifications = Notification.objects.filter(recipient=recipient_filter)
        else:
            notifications = Notification.objects.all()

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
