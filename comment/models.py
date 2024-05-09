from django.db import models


class CommentModel(models.Model):
    comment_id = models.CharField(max_length=128)
    content = models.TextField(max_length=2048)
    poi_id = models.CharField(max_length=128)
    comment_type = models.PositiveSmallIntegerField()
    order_score = models.PositiveSmallIntegerField()
    food_score = models.PositiveSmallIntegerField()
    delivery_score = models.PositiveSmallIntegerField()
    taste_score = models.PositiveSmallIntegerField()
    quality_score = models.PositiveSmallIntegerField()
    packaging_score = models.PositiveSmallIntegerField()
    order_details = models.TextField(max_length=4096)
    create_time = models.DateField()

    class Meta:
        db_table = 'comment'
