import os
from datetime import datetime
from .models import NotificationSetting, NotificationLog, ChannelType
from .services import send_email_notification, send_whatsapp_notification

def render_template(template_str, context):
    rendered = template_str or ""
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    return rendered

def dispatch_trigger(user, trigger_event, extra_context=None):
    """
    Evaluates active channels for a trigger event and executes deliveries.
    """
    context = {
        "name": user.get_full_name() or user.username,
        "username": user.username,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "site": "NotifyHub"
    }
    if extra_context:
        context.update(extra_context)

    settings = NotificationSetting.objects.filter(trigger=trigger_event, is_active=True)

    for setting in settings:
        rendered_body = render_template(setting.template_body, context)
        rendered_subject = render_template(setting.template_subject, context)

        status = 'failed'
        response_text = ''
        recipient = ''

        if setting.channel == ChannelType.EMAIL:
            recipient = user.email
            if recipient:
                success, response_text = send_email_notification(recipient, rendered_subject, rendered_body)
                status = 'success' if success else 'failed'
            else:
                response_text = "No email address found on user."

        elif setting.channel == ChannelType.WHATSAPP:
            # 1. User attribute -> 2. Profile attribute -> 3. .env fallback
            recipient = (
                getattr(user, 'phone_number', None)
                or getattr(getattr(user, 'profile', None), 'phone_number', None)
                or os.getenv("WHATSAPP_RECIPIENT_NUMBER", "")
            )
            if recipient:
                success, response_text = send_whatsapp_notification(recipient, rendered_body)
                status = 'success' if success else 'failed'
            else:
                response_text = "No recipient phone number found."

        # Record to audit log
        NotificationLog.objects.create(
            user=user,
            trigger=trigger_event,
            channel=setting.channel,
            recipient=recipient or 'N/A',
            subject=rendered_subject,
            body=rendered_body,
            status=status,
            response_payload=response_text
        )