# Generated by Django 3.1.6 on 2021-02-11 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Name')),
                ('last_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Surname')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=200, null=True, verbose_name='Gender')),
                ('bod', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('strip_id', models.CharField(blank=True, max_length=255, null=True)),
                ('visit_reason', models.CharField(blank=True, choices=[('Trader', 'I am a Trader.'), ('Financial Advisor', "I'm Financial Advisor."), ('Curious', "I'm Curious."), ('Other', 'Other Reason.')], max_length=250, null=True, verbose_name='Visit Reason')),
                ('profil_pic', models.ImageField(blank=True, help_text='User profile picture', null=True, upload_to='profile_pic/')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active.Unselect this instead of deleting accounts.', verbose_name='Active')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether this user should be treated as staff.', verbose_name='Staff')),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('country', models.CharField(blank=True, max_length=150, null=True, verbose_name='City')),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('name', models.CharField(blank=True, max_length=225, null=True, verbose_name='Plan Name')),
                ('amount', models.PositiveIntegerField(blank=True, null=True, verbose_name='Plan Price')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Plan Description')),
            ],
            options={
                'verbose_name_plural': 'Plans',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('stripe_id', models.CharField(blank=True, max_length=225, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('status', models.CharField(choices=[('Current', 'Current'), ('Canceled', 'Canceled')], default='Current', max_length=100)),
                ('valid_till', models.DateField(blank=True, null=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.plan', verbose_name='Plan')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.transaction', verbose_name='Transaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified At')),
                ('state', models.CharField(blank=True, max_length=150, null=True, verbose_name='City')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.country')),
            ],
            options={
                'verbose_name_plural': 'States',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.country', verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.state', verbose_name='State'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]