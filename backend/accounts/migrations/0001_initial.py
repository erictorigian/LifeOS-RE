# Generated manually to match existing accounts_user table
from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True, db_index=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('password', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('points', models.IntegerField(blank=True, default=0, null=True)),
                ('level', models.CharField(blank=True, max_length=255, null=True)),
                ('streak', models.IntegerField(blank=True, default=0, null=True)),
                ('last_login_date', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('is_master_coach', models.BooleanField(default=False)),
                ('supabase_id', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'accounts_user',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
