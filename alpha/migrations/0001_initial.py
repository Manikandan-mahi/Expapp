# Generated by Django 3.2.7 on 2021-10-02 08:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exp_date', models.DateField(default=datetime.date.today)),
                ('exp_name', models.CharField(max_length=150)),
                ('exp_desc', models.CharField(max_length=300)),
                ('exp_amount', models.IntegerField()),
                ('exp_month', models.CharField(max_length=12)),
                ('exp_year', models.CharField(max_length=4)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]