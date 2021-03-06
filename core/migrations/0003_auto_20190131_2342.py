# Generated by Django 2.1.5 on 2019-02-01 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190131_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_admin',
            field=models.BooleanField(default=False, help_text='Possui todas as permissões', verbose_name='Administrador'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_manager',
            field=models.BooleanField(default=False, help_text='Pode gerenciar processos', verbose_name='Triador'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_publisher',
            field=models.BooleanField(default=False, help_text='Pode incluir parecer sobre um processo', verbose_name='Finalizador'),
        ),
    ]
