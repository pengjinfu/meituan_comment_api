from django.db import models


class MallModel(models.Model):
    poi_id = models.CharField(max_length=128, null=True, blank=True)
    poi_name = models.CharField(max_length=250, null=True, blank=True)
    cookies = models.TextField(max_length=2048, null=True, blank=True)
    is_bind = models.BooleanField()

    # 0=>未登录 1=>已登录 2=>登录已过期
    status = models.PositiveSmallIntegerField()
    active_code_id = models.BigIntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    huifulv=models.CharField(max_length=128)

    class Meta:
        db_table = 'mall'
