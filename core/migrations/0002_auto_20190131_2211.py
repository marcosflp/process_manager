# Generated by Django 2.1.5 on 2019-02-01 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('feedback', models.TextField(verbose_name='Parecer')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='processes', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('feedback_users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Usuários a incluir parecer')),
            ],
            options={
                'ordering': ('-pk',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcessFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Parecer')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Process', verbose_name='Processo')),
            ],
            options={
                'ordering': ('-pk',),
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('-pk',)},
        ),
    ]
