from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from core.models import Building, ChangeLog, Floor, Notification, Room
from equipment.models import Equipment, EquipmentPhoto, EquipmentType, WriteOffRequest
from requests_app.models import ChangeRequest, RepairRequest


class Command(BaseCommand):
    help = 'Загружает тестовые данные в правильном порядке'

    fixtures = [
        str(settings.BASE_DIR / 'fixtures' / '01_users.json'),
        str(settings.BASE_DIR / 'fixtures' / '02_building_floors_rooms.json'),
        str(settings.BASE_DIR / 'fixtures' / '03_equipment_types.json'),
        str(settings.BASE_DIR / 'fixtures' / '04_equipment.json'),
        str(settings.BASE_DIR / 'fixtures' / '05_requests.json'),
        str(settings.BASE_DIR / 'fixtures' / '06_writeoffs_logs_notifications.json'),
    ]

    expected_counts = {
        User: 8,
        Building: 1,
        Floor: 3,
        Room: 10,
        EquipmentType: 12,
        Equipment: 25,
        RepairRequest: 10,
        ChangeRequest: 3,
        WriteOffRequest: 1,
        ChangeLog: 8,
        Notification: 6,
    }

    def handle(self, *args, **options):
        if self.is_seed_complete():
            self.stdout.write(self.style.SUCCESS('Данные уже загружены, пропускаем.'))
            return

        if self.has_partial_seed():
            self.stdout.write(self.style.WARNING('Обнаружена частично загруженная БД, очищаю тестовые данные и загружаю заново.'))

        with transaction.atomic():
            self.clear_seed_data()
            self.load_seed_data()

        if not self.is_seed_complete():
            raise RuntimeError('Фикстуры загружены не полностью: после загрузки не совпали ожидаемые количества записей.')

        self.stdout.write(self.style.SUCCESS('\nГотово! Данные загружены.'))
        self.stdout.write('Логины: admin/ahc/keeper1/keeper2/keeper3/tech1/tech2/buh1')
        self.stdout.write('Пароль для всех: admin123')

    def is_seed_complete(self):
        return all(model.objects.count() == expected for model, expected in self.expected_counts.items())

    def has_partial_seed(self):
        return any(model.objects.count() > 0 for model in self.expected_counts)

    def clear_seed_data(self):
        for model in [
            ChangeRequest,
            RepairRequest,
            WriteOffRequest,
            EquipmentPhoto,
            Equipment,
            EquipmentType,
            Notification,
            ChangeLog,
            Room,
            Floor,
            Building,
            User,
        ]:
            model.objects.all().delete()

    def load_seed_data(self):
        self.stdout.write('Загружаем фикстуры...')
        for fixture in self.fixtures:
            call_command('loaddata', fixture, verbosity=0)
            self.stdout.write(self.style.SUCCESS(f'  ✓ {fixture}'))
