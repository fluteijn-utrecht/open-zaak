# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2022 Dimpact
# Generated by Django 3.2.15 on 2022-09-02 08:41

from django.db import migrations
from django.db.models import Case, F, Value, When

from ..constants import ObjectInformatieObjectTypes


def copy_to_generic_field(apps, _):
    ObjectInformatieObject = apps.get_model("documenten", "ObjectInformatieObject")
    ObjectInformatieObject.objects.update(
        _object_url=Case(
            When(object_type=ObjectInformatieObjectTypes.zaak, then=F("_zaak_url")),
            When(
                object_type=ObjectInformatieObjectTypes.besluit, then=F("_besluit_url")
            ),
            default=Value(""),
        )
    )


def copy_from_generic_field(apps, _):
    ObjectInformatieObject = apps.get_model("documenten", "ObjectInformatieObject")
    ObjectInformatieObject.objects.update(
        _zaak_url=Case(
            When(object_type=ObjectInformatieObjectTypes.zaak, then=F("_object_url")),
            default=Value(""),
        ),
        _besluit_url=Case(
            When(
                object_type=ObjectInformatieObjectTypes.besluit, then=F("_object_url")
            ),
            default=Value(""),
        ),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("documenten", "0015_auto_20220902_0840"),
    ]

    operations = [
        migrations.RunPython(copy_to_generic_field, copy_from_generic_field),
    ]