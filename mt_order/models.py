from django.db import models


# Create your models here.
class MTOrderModel(models.Model):
    class Meta:
        db_table = 'mt_order'
