import os
import requests

def send_email_notification(to_email, subject, body):
    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev")

    if not api_key:
        return False, "RESEND_API_KEY is missing."

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": from_email,
        "to": [to_email],
        "subject": subject or "Account Security Alert",
        "html": f"<p>{body}</p>"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code in [200, 201], response.text
    except Exception as e:
        return False, str(e)

def send_whatsapp_notification(to_phone, body):
    token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    phone_id = os.getenv("PHONE_NUMBER_ID")

    # Fallback to env variable agar to_phone blank ho
    target_phone = to_phone or os.getenv("WHATSAPP_RECIPIENT_NUMBER", "")
    if not target_phone:
        return False, "Recipient phone number missing."

    if not token or not phone_id:
        return False, "WhatsApp credentials missing."

    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    clean_phone = target_phone.replace("+", "").replace(" ", "").strip()
    
    # Meta hello_world template payload (Instant delivery bypass)
    payload = {
        "messaging_product": "whatsapp",
        "to": clean_phone,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code in [200, 201], response.text
    except Exception as e:
        return False, str(e)