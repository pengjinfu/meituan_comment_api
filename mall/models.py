from django.db import models


# Create your models here.

class MallModel(models.Model):
    poi_id = models.CharField(max_length=128, null=True, blank=True)
    poi_name = models.CharField(max_length=250, null=True, blank=True)
    account = models.CharField(max_length=128)
    password = models.CharField(max_length=64)
    cookie = models.TextField(max_length=2048)
    active_key_id = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'mall'
