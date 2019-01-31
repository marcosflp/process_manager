from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return f'{self.user.email}'
