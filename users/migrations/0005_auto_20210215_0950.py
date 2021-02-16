# Generated by Django 3.1.6 on 2021-02-15 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0010_auto_20200508_1851'),
        ('users', '0004_auto_20210212_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='state',
            name='country',
        ),
        migrations.AlterModelOptions(
            name='subscriptions',
            options={'verbose_name_plural': 'Subscriptions'},
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.country', verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='user',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.region', verbose_name='State'),
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='State',
        ),
    ]