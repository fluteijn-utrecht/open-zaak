# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2022 Dimpact
# Generated by Django 3.2.14 on 2022-08-15 14:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("documenten", "0010_auto_20220809_1215"),
    ]

    operations = [
        migrations.AddField(
            model_name="bestandsdeel",
            name="datetime_created",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="datetime created"
            ),
        ),
    ]