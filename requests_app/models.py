from django.db import models
from django.utils import timezone


class RepairRequest(models.Model):
    STATUS_NEW = 'new'
    STATUS_ACCEPTED = 'accepted'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_ACCEPTED, 'Принята'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_DONE, 'Выполнена'),
        (STATUS_REJECTED, 'Отклонена'),
    ]

    PRIORITY_LOW = 'low'
    PRIORITY_MED = 'medium'
    PRIORITY_HIGH = 'high'

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Низкий'),
        (PRIORITY_MED, 'Средний'),
        (PRIORITY_HIGH, 'Высокий'),
    ]

    number = models.CharField('Номер заявки', max_length=20, unique=True, blank=True)
    room = models.ForeignKey('core.Room', on_delete=models.CASCADE, related_name='repair_requests', verbose_name='Кабинет')
    equipment = models.ForeignKey('equipment.Equipment', on_delete=models.SET_NULL, null=True, blank=True, related_name='repair_requests', verbose_name='Оборудование')
    description = models.TextField('Описание неисправности')
    priority = models.CharField('Приоритет', max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MED)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)

    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='requests_created', verbose_name='Заявитель')
    assigned_to = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='requests_assigned', verbose_name='Назначен технику')
    ahc_response = models.TextField('Ответ Зам. АХЧ', blank=True)

    photo = models.ImageField('Фото неисправности', upload_to='requests/', null=True, blank=True)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField('Дата решения', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка на ремонт'
        verbose_name_plural = 'Заявки на ремонт'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заявка №{self.number} — {self.room}'

    def save(self, *args, **kwargs):
        if not self.number:
            last = RepairRequest.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.number = f'REQ-{next_id:04d}'
        if self.status in [self.STATUS_DONE, self.STATUS_REJECTED] and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def status_color(self):
        colors = {
            'new': 'blue',
            'accepted': 'purple',
            'in_progress': 'yellow',
            'done': 'green',
            'rejected': 'red',
        }
        return colors.get(self.status, 'gray')


class ChangeRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'На рассмотрении'),
        (STATUS_APPROVED, 'Одобрен'),
        (STATUS_REJECTED, 'Отклонён'),
    ]

    TYPE_PLAN = 'plan'
    TYPE_EQUIPMENT = 'equipment'

    TYPE_CHOICES = [
        (TYPE_PLAN, 'Изменение плана кабинета'),
        (TYPE_EQUIPMENT, 'Изменение оборудования'),
    ]

    room = models.ForeignKey('core.Room', on_delete=models.CASCADE, related_name='change_requests')
    request_type = models.CharField('Тип запроса', max_length=20, choices=TYPE_CHOICES)
    description = models.TextField('Описание изменения')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='change_requests_created')
    reviewed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='change_requests_reviewed')
    admin_comment = models.TextField('Комментарий администратора', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Запрос на изменение'
        verbose_name_plural = 'Запросы на изменение'
        ordering = ['-created_at']

    def __str__(self):
        return f'Запрос от {self.created_by} — {self.room}'
