from django.db import models


class Trigger(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class NotificationTemplate(models.Model):
    CHANNEL_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('web_push', 'Web Push'),
    ]

    trigger = models.ForeignKey(Trigger,on_delete=models.CASCADE,
        related_name='templates')   
    channel = models.CharField(max_length=20,choices=CHANNEL_CHOICES)
    title = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trigger.name} - {self.channel}"


class PushSubscription(models.Model):
    endpoint = models.TextField(unique=True)
    p256dh = models.TextField()
    auth = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.endpoint