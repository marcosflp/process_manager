from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """
    Abstract model.
    Must be used inherited in all new models
    """
    class Meta:
        abstract = True
        ordering = ('-pk',)


class Profile(BaseModel):
    """
    Model to register new users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email}'

    def delete(self, using=None, keep_parents=False):
        self.user.delete()
        super(Profile, self).delete(using, keep_parents)


class Process(BaseModel):
    """
    Model to register new processes
    """
    title = models.CharField(max_length=128, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')

    feedback = models.TextField(verbose_name='Parecer')
    feedback_users = models.ManyToManyField(
        User,
        verbose_name='Usuários a incluir parecer',
        blank=True
    )

    created_by = models.ForeignKey(
        User,
        verbose_name='Criado por',
        related_name='processes',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.title

    @property
    def has_feedback(self):
        return self.processfeedback_set.exists()


class ProcessFeedback(BaseModel):
    """
    Model to register feedback of processes
    """
    process = models.ForeignKey(
        'core.Process',
        on_delete=models.CASCADE,
        verbose_name='Processo'
    )
    description = models.TextField(verbose_name='Parecer')

    created_by = models.ForeignKey(
        User,
        verbose_name='Criado por',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.process
