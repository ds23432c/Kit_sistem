from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Загружает тестовые данные в правильном порядке (идемпотентно)'

    def handle(self, *args, **options):
        User = get_user_model()

        # Уже есть данные — не трогаем
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Данные уже загружены, пропускаем.'))
            return

        self.stdout.write('Загружаем фикстуры...')
        fixtures = [
            '01_users',
            '02_building_floors_rooms',
            '03_equipment_types',
            '04_equipment',
            '05_requests',
            '06_writeoffs_logs_notifications',
        ]
        for f in fixtures:
            try:
                call_command('loaddata', f, verbosity=0)
                self.stdout.write(self.style.SUCCESS(f'  ✓ {f}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ {f}: {e}'))

        self.stdout.write(self.style.SUCCESS('\nГотово! Данные загружены.'))
        self.stdout.write('Логины: admin/ahc/keeper1/keeper2/keeper3/tech1/tech2/buh1')
        self.stdout.write('Пароль для всех: admin123')
