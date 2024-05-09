from django.db import models


# Create your models here.
class BackstageUserModel(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        import hashlib
        md5 = hashlib.md5()
        md5.update(self.password.encode())
        self.password = md5.hexdigest()

        super(BackstageUserModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'backstage_user'
