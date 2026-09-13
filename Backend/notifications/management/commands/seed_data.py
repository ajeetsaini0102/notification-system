from django.core.management.base import BaseCommand
from notifications.models import Trigger, NotificationTemplate


class Command(BaseCommand):
    help = "Create default notification triggers and templates"

    def handle(self, *args, **kwargs):

        login, _ = Trigger.objects.get_or_create(
            name="Login",
            defaults={
                "description": "User login notification",
                "is_active": True,
            },
        )

        logout, _ = Trigger.objects.get_or_create(
            name="Logout",
            defaults={
                "description": "User logout notification",
                "is_active": True,
            },
        )

        templates = [
            (login, "whatsapp", "Login Notification", "", "Hello {{name}}, you logged in at {{time}}."),
            (login, "email", "Login Notification", "User Login", "Hello {{name}}, you logged in at {{time}}."),
            (login, "web_push", "Login Notification", "", "Hello {{name}}, you logged in at {{time}}."),
            (logout, "whatsapp", "Logout Notification", "", "Hello {{name}}, you logged out at {{time}}."),
            (logout, "email", "Logout Notification", "User Logout", "Hello {{name}}, you logged out at {{time}}."),
            (logout, "web_push", "Logout Notification", "", "Hello {{name}}, you logged out at {{time}}."),
        ]

        for trigger, channel, title, subject, body in templates:
            NotificationTemplate.objects.get_or_create(
                trigger=trigger,
                channel=channel,
                defaults={
                    "title": title,
                    "subject": subject,
                    "body": body,
                    "is_enabled": True,
                },
            )

        self.stdout.write(
            self.style.SUCCESS("Default notification data created successfully.")
        )