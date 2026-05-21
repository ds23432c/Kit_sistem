from django.db import models
from django.utils import timezone


class EquipmentType(models.Model):
    name = models.CharField('Вид оборудования', max_length=100)
    icon = models.CharField('Иконка (lucide)', max_length=50, default='monitor')

    class Meta:
        verbose_name = 'Вид оборудования'
        verbose_name_plural = 'Виды оборудования'

    def __str__(self):
        return self.name


class Equipment(models.Model):
    CONDITION_OK = 'ok'
    CONDITION_BROKEN = 'broken'
    CONDITION_REPAIR = 'repair'
    CONDITION_WRITTEN_OFF = 'written_off'

    CONDITION_CHOICES = [
        (CONDITION_OK, 'Исправно'),
        (CONDITION_BROKEN, 'Неисправно'),
        (CONDITION_REPAIR, 'В ремонте'),
        (CONDITION_WRITTEN_OFF, 'Списано'),
    ]

    # Основные поля
    reg_number = models.CharField('Регистрационный номер', max_length=50, unique=True)
    brand = models.CharField('Марка', max_length=100)
    model = models.CharField('Модель', max_length=100)
    specs = models.TextField('Технические характеристики', blank=True)
    quantity = models.PositiveIntegerField('Количество', default=1)
    equipment_type = models.ForeignKey(
        EquipmentType, on_delete=models.SET_NULL, null=True,
        related_name='items', verbose_name='Вид оборудования'
    )
    room = models.ForeignKey(
        'core.Room', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='equipment_items', verbose_name='Кабинет'
    )

    # Состояние
    condition = models.CharField('Состояние', max_length=20, choices=CONDITION_CHOICES, default=CONDITION_OK)
    is_present = models.BooleanField('На месте', default=True)

    # Даты
    date_added = models.DateField('Дата внесения', default=timezone.now)
    last_check_date = models.DateField('Последняя дата проверки', null=True, blank=True)
    next_check_date = models.DateField('Следующая дата проверки', null=True, blank=True)

    # Финансы
    cost = models.DecimalField('Стоимость (руб.)', max_digits=12, decimal_places=2, null=True, blank=True)

    # Медиа
    photo = models.ImageField('Фото', upload_to='equipment/', null=True, blank=True)

    # Служебные
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True,
        related_name='equipment_created', verbose_name='Добавил'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
        ordering = ['reg_number']

    def __str__(self):
        return f'{self.reg_number} — {self.brand} {self.model}'

    @property
    def is_overdue(self):
        if self.next_check_date:
            return self.next_check_date < timezone.now().date()
        return False

    @property
    def condition_badge(self):
        colors = {
            'ok': 'green',
            'broken': 'red',
            'repair': 'yellow',
            'written_off': 'gray',
        }
        return colors.get(self.condition, 'gray')


class EquipmentPhoto(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField('Фото', upload_to='equipment/gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Фото оборудования'
        verbose_name_plural = 'Фото оборудования'


class WriteOffRequest(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='writeoffs')
    reason = models.TextField('Причина списания')
    confirmed_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True,
        related_name='writeoffs_confirmed'
    )
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True,
        related_name='writeoffs_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    confirmation_word = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Акт списания'
        verbose_name_plural = 'Акты списания'
