# Generated by Django 5.0.4 on 2024-04-29 12:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_alter_accesskey_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesskey',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 26, 12, 38, 54, 799608, tzinfo=datetime.timezone.utc)),
        ),
    ]
