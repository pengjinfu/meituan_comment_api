from django.db import models


# Create your models here.
class MTOrderModel(models.Model):
    platform = models.CharField(max_length=128)
    order_seq = models.CharField(max_length=16)
    order_no = models.CharField(max_length=128)
    order_amount = models.CharField(max_length=16)
    pay_amount = models.CharField(max_length=16)
    income = models.CharField(max_length=16)
    user_type = models.CharField(max_length=128)
    user_info = models.TextField(max_length=2048)
    food_details = models.TextField(max_length=4096)
    poi_id = models.CharField(max_length=128)
    create_time = models.DateTimeField()

    class Meta:
        db_table = 'mt_order'
