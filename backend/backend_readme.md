# NotifyHub - Backend REST API

A scalable notification engine built with **Django** and **Django REST Framework (DRF)**. NotifyHub powers dynamic multi-channel notification dispatching, message template management, channel preference matrices, and delivery audit logging across **Email** and **WhatsApp**.

---

##  Key Capabilities

- **Multi-Channel Dispatch Engine:** Decoupled service layer routing alerts through active channels:
  -  **Email Service:** Powered by [Resend API](https://resend.com/) for reliable transactional delivery.
  - **WhatsApp Service:** Powered by [Meta Graph Cloud API](https://developers.facebook.com/) sending templated/interactive messages.
- **Dynamic Context Interpolation:** Auto-renders dynamic variables like `{{name}}`, `{{time}}`, and `{{site}}` into subject and message body templates.
- **Trigger-Channel Matrix:** Allows toggling specific channels on or off per system event (`Login`, `Logout`, `Inactivity`).
- **Delivery Audit Logging:** Tracks each dispatch attempt with status (`SENT`, `FAILED`), error details, payload metadata, and timestamps.
- **Production-Ready Static Handling:** Pre-configured with **WhiteNoise** for serving Django Admin CSS/JS assets seamlessly in cloud environments.

---

##  Tech Stack

- **Core Framework:** Python 3.10+ & Django 4+ / 5+
- **API Engine:** Django REST Framework (DRF)
- **CORS Management:** `django-cors-headers`
- **Static Asset Serving:** WhiteNoise
- **External Providers:**
  - Resend (`resend` SDK / HTTP requests)
  - Meta Graph API (`requests`)
- **Hosting & Deployment:** Render (Web Service)

---

##  Repository Structure

```text
backend/
├── core/                       # Django project root configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── production.py           # Production settings (CORS, Staticfiles, Security)
│   ├── settings.py             # Base settings & environment bindings
│   ├── urls.py                 # Main URL routing & admin endpoints
│   └── wsgi.py
├── notifications/              # Main notification application
│   ├── management/
│   │   └── commands/
│   │       └── setup_initial_data.py  # Seed script for initial settings & templates
│   ├── migrations/             # Database schema migrations
│   ├── __init__.py
│   ├── admin.py                # Django admin registration for models
│   ├── apps.py
│   ├── dispatch_trigger.py     # Trigger orchestration & contextual variable resolution
│   ├── models.py               # NotificationSetting & NotificationLog schemas
│   ├── serializers.py          # DRF model serializers
│   ├── services.py             # Resend & WhatsApp API integration functions
│   ├── tests.py
│   ├── urls.py                 # API route registrations
│   └── views.py                # ViewSets for Settings, Logs, and Dispatch
├── staticfiles/                # Collected static assets (WhiteNoise)
├── db.sqlite3                  # Local database instance
├── manage.py                   # Django CLI tool
├── requirements.txt            # Python dependencies
└── .env                        # Secret environment variables (local)
```

---

## ⚙️ Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
# Django Core Settings
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:5173,https://notify-hub-lac.vercel.app

# Email Configuration (Resend)
RESEND_API_KEY=re_your_resend_api_key
FROM_EMAIL=onboarding@resend.dev

# WhatsApp Configuration (Meta Cloud API)
WHATSAPP_ACCESS_TOKEN=your_meta_system_user_or_temporary_token
PHONE_NUMBER_ID=your_15_digit_phone_number_id
WHATSAPP_RECIPIENT_NUMBER=919876543210
```

---

##  Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- `pip` package manager
- Virtual environment (`venv`)

### 2. Setup Virtual Environment & Dependencies

```bash
cd backend
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Migration & Initial Data Seeding

Run migrations and initialize the notification triggers and default channel templates:

```bash
python manage.py migrate
python manage.py setup_initial_data
```

### 4. Create Superuser (For Django Admin)

```bash
python manage.py createsuperuser
```

### 5. Launch Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.  
Access the Django Admin panel at `http://127.0.0.1:8000/admin/`.

---

## 🔌 API Endpoints Reference

Base Path: `/api/notifications/`

| HTTP Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/settings/` | Lists all trigger-channel setting pairs and templates |
| `POST` | `/settings/toggle/` | Toggles channel active state (`trigger`, `channel`, `is_active`) |
| `PATCH` | `/settings/<id>/` | Updates custom subject line and message body template |
| `POST` | `/dispatch/` | Fires event trigger (`event_trigger: "login" \| "logout" \| "inactivity"`) |
| `GET` | `/logs/` | Fetches audit trail of all dispatched notifications |

---

##  Production Deployment (Render)

When deploying to [Render](https://render.com/) as a Web Service:

1. **Root Directory:** Set to `backend` (if inside a monorepo).
2. **Environment:** `Python 3`
3. **Build Command:**
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py setup_initial_data
   ```
4. **Start Command:**
   ```bash
   gunicorn core.wsgi:application
   ```
5. **Environment Variables:** Add all variables defined in the `.env` section to the Render Dashboard.