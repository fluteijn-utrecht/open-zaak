# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2022 Dimpact
# Generated by Django 3.2.14 on 2022-07-27 15:16

from django.db import migrations, models
import django.db.models.deletion
import privates.fields
import privates.storages
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("documenten", "0006_alter_enkelvoudiginformatieobject__informatieobjecttype"),
    ]

    operations = [
        migrations.CreateModel(
            name="BestandsDeel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unieke resource identifier (UUID4)",
                        unique=True,
                    ),
                ),
                (
                    "volgnummer",
                    models.PositiveIntegerField(
                        help_text="Een volgnummer dat de volgorde van de bestandsdelen aangeeft."
                    ),
                ),
                (
                    "omvang",
                    models.PositiveIntegerField(
                        help_text="De grootte van dit specifieke bestandsdeel."
                    ),
                ),
                (
                    "inhoud",
                    privates.fields.PrivateMediaFileField(
                        blank=True,
                        help_text="De (binaire) bestandsinhoud van dit specifieke bestandsdeel.",
                        storage=privates.storages.PrivateMediaFileSystemStorage(),
                        upload_to="part-uploads/%Y/%m/",
                    ),
                ),
                (
                    "informatieobject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bestandsdelen",
                        to="documenten.enkelvoudiginformatieobjectcanonical",
                    ),
                ),
            ],
            options={
                "verbose_name": "bestands deel",
                "verbose_name_plural": "bestands delen",
                "unique_together": {("informatieobject", "volgnummer")},
            },
        ),
    ]
