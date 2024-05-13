from django.db import models


# Create your models here.

class MallModel(models.Model):
    poi_id = models.CharField(max_length=128, null=True, blank=True)
    poi_name = models.CharField(max_length=250, null=True, blank=True)
    cookies = models.TextField(max_length=2048, null=True, blank=True)
    active_code_id = models.BigIntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mall'
