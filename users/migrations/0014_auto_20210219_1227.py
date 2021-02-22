# Generated by Django 3.1.6 on 2021-02-19 12:27

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20210219_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='visit_reason',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Trader', 'I am a Trader.'), ('Financial Advisor', "I'm Financial Advisor."), ('Curious', "I'm Curious."), ('Other', 'Other Reason.')], max_length=38),
        ),
    ]