from django.db import models


class Storage(models.Model):
    key = models.IntegerField(name='key', verbose_name='Ключ')
    value = models.CharField(max_length=255, name='value', verbose_name='Значение')

    def __str__(self):
        return str(self.key)

    class Meta:
        verbose_name = 'Хранилище'
        verbose_name_plural = 'Хранилища'
