from django.db import models


class ActiveCodeModel(models.Model):
    key = models.TextField(max_length=256)
    active_time = models.DateTimeField(null=True)
    expire = models.DateTimeField(null=True, blank=True)
    life = models.PositiveIntegerField(default=1)
    is_forbidden = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    activation_ip = models.CharField(max_length=64, null=True)

    # 卡密状态: 0=>未激活 1=>已激活 2=>已过期
    status = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'active_code'
