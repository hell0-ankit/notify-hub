from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notifications.models import NotificationSetting, NotificationLog

class Command(BaseCommand):
    help = 'Flushes old data and seeds fresh superuser, single test user, and triggers with default templates (Email & WhatsApp only)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("=" * 60))
        self.stdout.write(self.style.WARNING("     FLUSHING OLD NOTIFYHUB DATA & SEEDING FRESH"))
        self.stdout.write(self.style.WARNING("=" * 60))

        # --- STEP 1: PURANA DATA DELETE KAREIN ---
        deleted_logs, _ = NotificationLog.objects.all().delete()
        deleted_settings, _ = NotificationSetting.objects.all().delete()
        deleted_users, _ = User.objects.all().delete()

        self.stdout.write(self.style.NOTICE(f"[Deleted] {deleted_logs} Audit Logs"))
        self.stdout.write(self.style.NOTICE(f"[Deleted] {deleted_settings} Notification Settings"))
        self.stdout.write(self.style.NOTICE(f"[Deleted] {deleted_users} Users\n"))

        # --- STEP 2: FRESH SUPERUSER (ADMIN) ---
        admin_user = User.objects.create_superuser(
            username='admin',
            email='ankitbohra660@gmail.com',
            password='admin123'
        )

        # --- STEP 3: FRESH SINGLE TEST USER ---
        test_user = User.objects.create_user(
            username='testuser',
            email='ankit@gmail.com',
            password='testpass123',
            first_name='Ankit',
            last_name='Singh'
        )

        # --- STEP 4: TRIGGER & TEMPLATE CONFIGS ---
        templates_config = [
            # Login
            {
                'trigger': 'login',
                'channel': 'email',
                'subject': 'Security Alert: New Login to Your Account',
                'body': 'Hi {{name}}, a new login was detected on your account at {{time}} from {{site}}.'
            },
            {
                'trigger': 'login',
                'channel': 'whatsapp',
                'subject': '',
                'body': 'Hi {{name}}, new login detected on {{site}} at {{time}}.'
            },

            # Logout
            {
                'trigger': 'logout',
                'channel': 'email',
                'subject': 'Session Terminated: Logout Recorded',
                'body': 'Hi {{name}}, you have successfully logged out from {{site}} at {{time}}.'
            },
            {
                'trigger': 'logout',
                'channel': 'whatsapp',
                'subject': '',
                'body': 'Hi {{name}}, you have logged out from {{site}} at {{time}}.'
            },

            # Inactivity
            {
                'trigger': 'inactivity',
                'channel': 'email',
                'subject': 'We Miss You! Inactivity Reminder',
                'body': 'Hi {{name}}, we noticed you have been inactive on {{site}} for a while. Log in to see what is new!'
            },
            {
                'trigger': 'inactivity',
                'channel': 'whatsapp',
                'subject': '',
                'body': 'Hi {{name}}, we miss you on {{site}}! Log back in to continue where you left off.'
            },
        ]

        for config in templates_config:
            NotificationSetting.objects.create(
                trigger=config['trigger'],
                channel=config['channel'],
                template_subject=config['subject'],
                template_body=config['body'],
                is_active=True
            )

        # --- STEP 5: VERIFIED OUTPUT PRINT ---
        self.stdout.write(self.style.SUCCESS("1. [Superuser Created]"))
        self.stdout.write(f"   • Username : {admin_user.username}")
        self.stdout.write(f"   • Email    : {admin_user.email}")
        self.stdout.write("   • Password : admin123")

        self.stdout.write(self.style.SUCCESS("\n2. [Single Test User Created]"))
        self.stdout.write(f"   • Username : {test_user.username}")
        self.stdout.write(f"   • Email    : {test_user.email}")
        self.stdout.write("   • Password : testpass123")

        self.stdout.write(self.style.SUCCESS("\n3. [Trigger-Channel Matrix with Templates Ready]"))
        self.stdout.write(f"   • Total Active Settings : {NotificationSetting.objects.count()} (3 Triggers x 2 Channels)")

        self.stdout.write(self.style.WARNING("\n" + "=" * 60))
        self.stdout.write(self.style.SUCCESS("   CLEAN SEEDING COMPLETED - READY FOR DISPATCH"))
        self.stdout.write(self.style.WARNING("=" * 60))