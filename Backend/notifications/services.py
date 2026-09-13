from .models import Trigger, PushSubscription
from django.core.mail import send_mail
from django.conf import settings
import os
import requests
from pywebpush import webpush, WebPushException


def render_template(text, context):
    if not text:
        return ""

    for key, value in context.items():
        text = text.replace(
            "{{" + key + "}}",
            str(value)
        )

    return text


def fire_notification(trigger_name):
    context = {
        "name": "Demo User",
        "time": __import__("datetime").datetime.now().strftime(
            "%d %b %Y, %I:%M %p"
        ),
    }

    try:
        trigger = Trigger.objects.get(
            name=trigger_name,
            is_active=True
        )
    except Trigger.DoesNotExist:
        print(f"Trigger not found or inactive: {trigger_name}")
        return

    templates = trigger.templates.filter(is_enabled=True)

    if not templates.exists():
        print(f"No enabled templates for: {trigger_name}")
        return

    for template in templates:

        # Dynamic variables
        rendered_title = render_template(
            template.title,
            context
        )

        rendered_subject = render_template(
            template.subject,
            context
        )

        rendered_body = render_template(
            template.body,
            context
        )

        # Console log
        print(
            f"[NOTIFICATION] "
            f"Trigger={trigger.name} | "
            f"Channel={template.channel} | "
            f"Title={rendered_title} | "
            f"Body={rendered_body}"
        )

        # EMAIL
        if template.channel.lower() == "email":
            try:
                send_mail(
                    subject=rendered_subject or rendered_title or "Notification",
                    message=rendered_body,
                    from_email=os.getenv("EMAIL_HOST_USER"),
                    recipient_list=[os.getenv("EMAIL_HOST_USER")],
                    fail_silently=False,
                )

                print("[EMAIL] Notification sent successfully")

            except Exception as e:
                print(f"[EMAIL] Failed: {e}")

        # WHATSAPP
        elif template.channel.lower() == "whatsapp":
            try:
                access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
                phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
                to_number = os.getenv("WHATSAPP_TO_NUMBER")

                url = (
                    f"https://graph.facebook.com/v26.0/"
                    f"{phone_number_id}/messages"
                )

                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                }

                payload = {
                    "messaging_product": "whatsapp",
                    "to": to_number,
                    "type": "text",
                    "text": {
                        "body": rendered_body
                    }
                }

                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=20
                )

                if response.ok:
                    print(
                        "[WHATSAPP] Notification sent successfully"
                    )
                    print(response.json())
                else:
                    print("[WHATSAPP] Failed")
                    print(response.status_code)
                    print(response.text)

            except Exception as e:
                print(f"[WHATSAPP] Failed: {e}")

        # WEB PUSH
        elif template.channel.lower() == "web_push":
            subscriptions = PushSubscription.objects.all()

            for subscription in subscriptions:
                subscription_info = {
                    "endpoint": subscription.endpoint,
                    "keys": {
                        "p256dh": subscription.p256dh,
                        "auth": subscription.auth,
                    },
                }

                try:
                    webpush(
                        subscription_info=subscription_info,
                        data=__import__("json").dumps({
                            "title": rendered_title or "Notification",
                            "body": rendered_body,
                        }),
                        vapid_private_key=str(
                            settings.VAPID_PRIVATE_KEY_PATH
                        ),
                        vapid_claims={
                            "sub": (
                                f"mailto:"
                                f"{os.getenv('EMAIL_HOST_USER')}"
                            )
                        },
                    )

                    print(
                        "[WEB PUSH] Notification sent successfully"
                    )

                except WebPushException as e:
                    print(f"[WEB PUSH] Failed: {e}")

                except Exception as e:
                    print(f"[WEB PUSH] Failed: {e}")


def send_template_notification(template):
    channel = template.channel.lower()

    # Demo context for Test Send
    context = {
        "name": "Demo User",
        "time": __import__("datetime").datetime.now().strftime(
            "%d %b %Y, %I:%M %p"
        ),
    }

    rendered_title = render_template(
        template.title,
        context
    )

    rendered_subject = render_template(
        template.subject,
        context
    )

    rendered_body = render_template(
        template.body,
        context
    )

    # EMAIL TEST
    if channel == "email":
        send_mail(
            subject=rendered_subject or rendered_title or "Notification",
            message=rendered_body,
            from_email=os.getenv("EMAIL_HOST_USER"),
            recipient_list=[os.getenv("EMAIL_HOST_USER")],
            fail_silently=False,
        )

        print("[EMAIL TEST] Notification sent successfully")

    # WHATSAPP TEST
    elif channel == "whatsapp":
        access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        to_number = os.getenv("WHATSAPP_TO_NUMBER")

        url = (
            f"https://graph.facebook.com/v26.0/"
            f"{phone_number_id}/messages"
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {
                "body": rendered_body
            }
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20
        )

        if response.ok:
            print(
                "[WHATSAPP TEST] Notification sent successfully"
            )
            print(response.json())
        else:
            print("[WHATSAPP TEST] Failed")
            print(response.status_code)
            print(response.text)

            raise Exception(
                f"WhatsApp API error: {response.status_code}"
            )

    # WEB PUSH TEST
    elif channel == "web_push":
        subscriptions = PushSubscription.objects.all()

        for subscription in subscriptions:
            subscription_info = {
                "endpoint": subscription.endpoint,
                "keys": {
                    "p256dh": subscription.p256dh,
                    "auth": subscription.auth,
                },
            }

            webpush(
                subscription_info=subscription_info,
                data=__import__("json").dumps({
                    "title": rendered_title or "Notification",
                    "body": rendered_body,
                }),
                vapid_private_key=str(
                    settings.VAPID_PRIVATE_KEY_PATH
                ),
                vapid_claims={
                    "sub": (
                        f"mailto:"
                        f"{os.getenv('EMAIL_HOST_USER')}"
                    )
                },
            )

        print(
            "[WEB PUSH TEST] Notification sent successfully"
        )

    else:
        raise Exception(
            f"Unsupported notification channel: {channel}"
        )