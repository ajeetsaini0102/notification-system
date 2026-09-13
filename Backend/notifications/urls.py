from rest_framework.routers import DefaultRouter
from .views import (
    TriggerViewSet,
    NotificationTemplateViewSet,
    test_login_notification,
    test_template_notification,
    whatsapp_webhook,
    save_push_subscription,
    test_logout_notification,
)
from django.urls import path
from notifications.views import*

router = DefaultRouter()

router.register('triggers', TriggerViewSet)
router.register('templates', NotificationTemplateViewSet)

urlpatterns = router.urls + [
    path('test-login/',test_login_notification,name='test-login'),
    path("webhook/", whatsapp_webhook, name="whatsapp-webhook"),
    path("push/subscribe/", save_push_subscription, name="push-subscribe"),
    path('templates/<int:template_id>/test/',test_template_notification,
    name='test-template'),
    path('test-logout/',test_logout_notification,name='test-logout'),
]