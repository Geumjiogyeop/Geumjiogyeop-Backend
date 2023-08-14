# Generated by Django 4.2.4 on 2023-08-13 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todays', '0002_remove_images_today_id_images_today_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='today',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='TodayLiked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('today', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todays.today')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]