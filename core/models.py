from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, F, Q


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

    # Set fields to use with Rule permissions

    is_admin = models.BooleanField(
        default=False,
        verbose_name='Administrador',
        help_text='Possui todas as permissões'
    )
    is_manager = models.BooleanField(
        default=False,
        verbose_name='Triador',
        help_text='Pode gerenciar processos'
    )
    is_publisher = models.BooleanField(
        default=False,
        verbose_name='Finalizador',
        help_text='Pode incluir parecer sobre um processo'
    )

    def __str__(self):
        return f'{self.user.email}'

    def delete(self, using=None, keep_parents=False):
        self.user.delete()
        super(Profile, self).delete(using, keep_parents)


class ProcessManager(models.Manager):

    def pending_processes(self):
        return self.annotate(
            total_publishes=Count('feedback_users'),
            total_feedbackprocesses=Count('processfeedback')
        ).filter(
            Q(total_feedbackprocesses=0)
            | Q(total_publishes__gt=F('total_feedbackprocesses'))
        )


class Process(BaseModel):
    """
    Model to register new processes
    """
    title = models.CharField(max_length=128, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')

    feedback_users = models.ManyToManyField(
        User,
        verbose_name='Usuários-triadores a incluir parecer',
        blank=True,
        limit_choices_to=Q(profile__is_publisher=True)
    )

    created_by = models.ForeignKey(
        User,
        verbose_name='Criado por',
        related_name='processes',
        on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProcessManager()

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Parecer: {self.description[:25]}...'


def create_profile(instance, created, **kwargs):
    """
    Create Profile if necessary
    """
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)


models.signals.post_save.connect(create_profile, sender=User)
