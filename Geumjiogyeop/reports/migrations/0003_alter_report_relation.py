# Generated by Django 4.2.4 on 2023-08-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_report_relation_alter_report_victim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='relation',
            field=models.CharField(choices=[('1', '본인'), ('2', '가족'), ('3', '기타')], max_length=2, verbose_name='관계'),
        ),
    ]