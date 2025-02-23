# Generated by Django 5.1.6 on 2025-02-12 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsfbackend', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='name',
            new_name='category_name',
        ),
        migrations.RemoveField(
            model_name='item',
            name='description',
        ),
        migrations.AddField(
            model_name='item',
            name='exp_ans',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='que_description',
            field=models.CharField(default='default_que', max_length=500),
        ),
        migrations.AddField(
            model_name='item',
            name='que_exp_ans',
            field=models.CharField(default='default_ans', max_length=1000),
        ),
    ]
