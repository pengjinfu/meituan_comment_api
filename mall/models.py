from django.db import models


# Create your models here.

class MallModel(models.Model):
    poi_id = models.CharField(max_length=128)
    poi_name = models.CharField(max_length=250)
    account = models.CharField(max_length=128)
    password = models.CharField(max_length=64)
    cookie = models.TextField(max_length=2048)

    class Meta:
        db_table = 'mall'
