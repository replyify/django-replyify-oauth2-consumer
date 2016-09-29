# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(max_length=50)),
                ('access_token', models.CharField(max_length=50)),
                ('refresh_token', models.CharField(max_length=50)),
                ('expires', models.DateTimeField(default=django.utils.timezone.now)),
                ('scope', models.CharField(max_length=50)),
                ('token_type', models.CharField(max_length=50)),
            ],
        ),
    ]
