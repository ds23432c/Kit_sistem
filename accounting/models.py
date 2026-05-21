from django.db import models


class AccountingReport(models.Model):
    title = models.CharField('Название отчёта', max_length=200)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    filters = models.JSONField('Параметры фильтрации', default=dict, blank=True)
    file = models.FileField('Файл отчёта', upload_to='reports/', null=True, blank=True)

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
