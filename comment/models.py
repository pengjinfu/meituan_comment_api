from django.db import models


class CommentModel(models.Model):
    comment_id = models.CharField(max_length=128)
    poi_id = models.CharField(max_length=128)
    user_name = models.CharField(max_length=128)
    content = models.TextField(max_length=2048)
    order_details = models.TextField(max_length=4096)
    comment_type = models.PositiveSmallIntegerField()
    create_time = models.DateField()

    class Meta:
        db_table = 'comment'
