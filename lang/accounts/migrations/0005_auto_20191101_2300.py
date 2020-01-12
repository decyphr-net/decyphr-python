# Generated by Django 2.2 on 2019-11-01 23:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_auto_20191021_0147"),
    ]

    operations = [
        migrations.AlterModelOptions(name="userprofile", options={},),
        migrations.AlterModelManagers(name="userprofile", managers=[],),
        migrations.RemoveField(model_name="userprofile", name="date_joined",),
        migrations.RemoveField(model_name="userprofile", name="first_name",),
        migrations.RemoveField(model_name="userprofile", name="groups",),
        migrations.RemoveField(model_name="userprofile", name="is_superuser",),
        migrations.RemoveField(model_name="userprofile", name="last_name",),
        migrations.RemoveField(model_name="userprofile", name="user_permissions",),
        migrations.AddField(
            model_name="userprofile",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userprofile",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="email",
            field=models.EmailField(db_index=True, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="username",
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
    ]
