from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_AHC = 'ahc'
    ROLE_KEEPER = 'keeper'
    ROLE_TECHNICIAN = 'technician'
    ROLE_ACCOUNTANT = 'accountant'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Администратор'),
        (ROLE_AHC, 'Зам. по АХЧ'),
        (ROLE_KEEPER, 'Заведующий кабинетом'),
        (ROLE_TECHNICIAN, 'Технический персонал'),
        (ROLE_ACCOUNTANT, 'Бухгалтерия'),
    ]

    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default=ROLE_KEEPER)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_ahc(self):
        return self.role == self.ROLE_AHC

    @property
    def is_keeper(self):
        return self.role == self.ROLE_KEEPER

    @property
    def is_technician(self):
        return self.role == self.ROLE_TECHNICIAN

    @property
    def is_accountant(self):
        return self.role == self.ROLE_ACCOUNTANT
