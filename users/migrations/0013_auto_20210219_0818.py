# Generated by Django 3.1.6 on 2021-02-19 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_remove_user_scope'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='amount',
            new_name='price',
        ),
    ]
