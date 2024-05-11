from django.db import models


class ActiveCodeModel(models.Model):
    key = models.TextField(max_length=256)
    is_activated = models.BooleanField(default=False)
    active_time = models.DateTimeField(null=True)
    expire = models.DateTimeField(null=True, blank=True)
    life = models.PositiveIntegerField(default=1)
    is_forbidden = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'active_code'
