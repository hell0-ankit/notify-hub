from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from notifications.models import NotificationSetting, UserDevice, NotificationLog

class Command(BaseCommand):
    help = 'Flushes old data and seeds fresh superuser, single test user, device, and triggers'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("=" * 60))
        self.stdout.write(self.style.WARNING("     FLUSHING OLD NOTIFYHUB DATA & SEEDING FRESH"))
        self.stdout.write(self.style.WARNING("=" * 60))

        # --- STEP 1: PURANA DATA DELETE KAREIN ---
        deleted_logs, _ = NotificationLog.objects.all().delete()
        deleted_settings, _ = NotificationSetting.objects.all().delete()
        deleted_devices, _ = UserDevice.objects.all().delete()
        deleted_users, _ = User.objects.all().delete()

        self.stdout.write(self.style.NOTICE(f"[Deleted] {deleted_logs} Audit Logs"))
        self.stdout.write(self.style.NOTICE(f"[Deleted] {deleted_settings} Notification Settings"))
        self.stdout.write(self.style.NOTICE(f"[Deleted] {deleted_devices} User Devices"))
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

        # --- STEP 4: FRESH DEVICE REGISTRATION ---
        device = UserDevice.objects.create(
            user=test_user,
            player_id='8f01089e-10ec-402d-9b71-724e4eb1d6ea'
        )

        # --- STEP 5: FRESH TRIGGER MATRIX ---
        triggers = ['login', 'logout', 'inactivity']
        channels = ['email', 'web_push', 'whatsapp']

        for trigger in triggers:
            for channel in channels:
                NotificationSetting.objects.create(
                    trigger=trigger,
                    channel=channel,
                    is_active=True
                )

        # --- STEP 6: VERIFIED OUTPUT PRINT ---
        self.stdout.write(self.style.SUCCESS("1. [Superuser Created]"))
        self.stdout.write(f"   • Username : {admin_user.username}")
        self.stdout.write(f"   • Email    : {admin_user.email}")
        self.stdout.write("   • Password : admin123")

        self.stdout.write(self.style.SUCCESS("\n2. [Single Test User Created]"))
        self.stdout.write(f"   • Username : {test_user.username}")
        self.stdout.write(f"   • Email    : {test_user.email}")
        self.stdout.write("   • Password : testpass123")

        self.stdout.write(self.style.SUCCESS("\n3. [Device Linked]"))
        self.stdout.write(f"   • User      : {device.user.username}")
        self.stdout.write(f"   • Player ID : {device.player_id}")

        self.stdout.write(self.style.SUCCESS("\n4. [Trigger-Channel Matrix Ready]"))
        self.stdout.write(f"   • Total Active Settings : {NotificationSetting.objects.count()} (3 Triggers x 3 Channels)")

        self.stdout.write(self.style.WARNING("\n" + "=" * 60))
        self.stdout.write(self.style.SUCCESS("   CLEAN SEEDING COMPLETED - READY FOR DISPATCH"))
        self.stdout.write(self.style.WARNING("=" * 60))