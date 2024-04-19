# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2024 Dimpact
# Generated by Django 3.2.23 on 2024-04-29 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authorizations", "0015_auto_20220318_1608"),
        ("autorisaties", "0008_alter_autorisatiespec_component"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="autorisatiespec",
            unique_together={("applicatie", "component", "scopes")},
        ),
    ]