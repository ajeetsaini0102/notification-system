from rest_framework import viewsets
from .models import Trigger, NotificationTemplate,PushSubscription
from .serializers import (TriggerSerializer,NotificationTemplateSerializer)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import fire_notification
from django.shortcuts import get_object_or_404
import os
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

class TriggerViewSet(viewsets.ModelViewSet):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer


@api_view(['POST'])
def test_login_notification(request):
    fire_notification("Login")

    return Response({
        "success": True,
        "message": "Login notification trigger fired"
    })
    
@api_view(['POST'])
def test_logout_notification(request):
    fire_notification("Logout")
    return Response({
        "success": True,
        "message": "Logout notification trigger fired"
    })


@api_view(['POST'])
def test_template_notification(request, template_id):
    template = get_object_or_404(
        NotificationTemplate.objects.select_related("trigger"),
        id=template_id
    )

    if not template.is_enabled:
        return Response(
            {
                "success": False,
                "message": "This notification template is disabled."
            },
            status=400
        )

    trigger = template.trigger

    # Temporarily fire only the selected channel
    from .services import send_template_notification

    try:
        send_template_notification(template)

        return Response({
            "success": True,
            "message": (
                f"Test notification sent for "
                f"{trigger.name} - {template.channel}"
            )
        })
    except Exception as e:
        return Response({
            "success": False,
            "message": str(e)
        }, status=500)

@csrf_exempt
def whatsapp_webhook(request):

    # Meta webhook verification
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if (
            mode == "subscribe"
            and token == os.getenv("WHATSAPP_VERIFY_TOKEN")
        ):
            return HttpResponse(challenge, status=200)

        return HttpResponse("Forbidden", status=403)

    # WhatsApp messages

    if request.method == "POST":
        try:
            import json

            data = json.loads(request.body)

            print("WhatsApp Webhook Received")
            print(json.dumps(data, indent=2))

            # WhatsApp message data
            entry = data.get("entry", [])

            if entry:
                changes = entry[0].get("changes", [])

                if changes:
                    value = changes[0].get("value", {})

                    messages = value.get("messages", [])

                    if messages:
                        message = messages[0]

                        sender = message.get("from")
                        message_type = message.get("type")

                        print(f"Sender: {sender}")
                        print(f"Message Type: {message_type}")

                        if message_type == "text":
                            message_text = message.get("text", {}).get("body")

                            print(f"Message: {message_text}")

            return JsonResponse({"status": "ok"}, status=200)

        except Exception as e:
            print(f"Webhook Error: {e}")
            return JsonResponse({"status": "error"}, status=400)

    return HttpResponse(status=405)


@csrf_exempt
def save_push_subscription(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        import json

        data = json.loads(request.body)

        endpoint = data.get("endpoint")
        keys = data.get("keys", {})

        p256dh = keys.get("p256dh")
        auth = keys.get("auth")

        if not endpoint or not p256dh or not auth:
            return JsonResponse(
                {"error": "Invalid push subscription"},
                status=400
            )

        PushSubscription.objects.update_or_create(
            endpoint=endpoint,
            defaults={
                "p256dh": p256dh,
                "auth": auth,
            },
        )

        return JsonResponse({
            "success": True,
            "message": "Push subscription saved"
        })

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=400
        )