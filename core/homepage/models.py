from django.db import models


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255, null=False)
    company_type = models.CharField(max_length=255, null=True)
    description = models.TextField(default='', null=True)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name
