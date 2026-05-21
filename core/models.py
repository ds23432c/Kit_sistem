from django.db import models


class Building(models.Model):
    name = models.CharField('Название здания', max_length=200)
    address = models.CharField('Адрес', max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Здание'
        verbose_name_plural = 'Здания'

    def __str__(self):
        return self.name


class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='floors', verbose_name='Здание')
    number = models.PositiveIntegerField('Номер этажа')
    name = models.CharField('Название', max_length=100, blank=True)
    map_data = models.JSONField('Данные карты', default=dict, blank=True)

    class Meta:
        verbose_name = 'Этаж'
        verbose_name_plural = 'Этажи'
        ordering = ['number']
        unique_together = ['building', 'number']

    def __str__(self):
        return f'Этаж {self.number} — {self.building.name}'


class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms', verbose_name='Этаж')
    number = models.CharField('Номер кабинета', max_length=20)
    name = models.CharField('Название', max_length=200)
    shape_data = models.JSONField('Данные фигуры на карте', default=dict, blank=True)
    keepers = models.ManyToManyField(
        'accounts.User', blank=True,
        related_name='rooms_kept',
        verbose_name='Заведующие',
        limit_choices_to={'role': 'keeper'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
        ordering = ['number']

    def __str__(self):
        return f'Каб. {self.number} — {self.name}'

    @property
    def status_color(self):
        items = self.equipment_items.all()
        if items.filter(condition='broken').exists():
            return 'red'
        if items.filter(condition='repair').exists():
            return 'yellow'
        if items.filter(condition='written_off').exists():
            return 'gray'
        return 'green'


class Notification(models.Model):
    TYPE_REPAIR = 'repair'
    TYPE_ANSWER = 'answer'
    TYPE_APPROVAL = 'approval'
    TYPE_OVERDUE = 'overdue'

    TYPE_CHOICES = [
        (TYPE_REPAIR, 'Новая заявка на ремонт'),
        (TYPE_ANSWER, 'Ответ на заявку'),
        (TYPE_APPROVAL, 'Запрос на изменение'),
        (TYPE_OVERDUE, 'Просрочена проверка'),
    ]

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField('Тип', max_length=20, choices=TYPE_CHOICES)
    title = models.CharField('Заголовок', max_length=200)
    message = models.TextField('Сообщение')
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField('Ссылка', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} → {self.user.username}'


class ChangeLog(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='changes')
    action = models.CharField('Действие', max_length=300)
    model_name = models.CharField('Модель', max_length=100)
    object_id = models.PositiveIntegerField('ID объекта', null=True, blank=True)
    old_value = models.JSONField('Старое значение', null=True, blank=True)
    new_value = models.JSONField('Новое значение', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лог изменений'
        verbose_name_plural = 'Лог изменений'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.action} by {self.user} at {self.created_at}'
