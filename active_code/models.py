from django.db import models


class ActiveCodeModel(models.Model):
    key = models.TextField(max_length=256)
    expire = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'active_code'
