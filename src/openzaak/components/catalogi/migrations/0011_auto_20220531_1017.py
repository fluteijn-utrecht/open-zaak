# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2022 Dimpact
# Generated by Django 3.2.13 on 2022-05-31 10:17

from zgw_consumers.models import Service
from django.db import migrations
from openzaak.utils.cache import DjangoRequestsCache, requests_cache_enabled


@requests_cache_enabled(
    "zaaktypen_procestypen_jaar_sync", backend=DjangoRequestsCache()
)
def set_selectieklasse_procestype_default_year(apps, _):
    ZaakType = apps.get_model("catalogi.ZaakType")

    for zaaktype in ZaakType.objects.all():
        if zaaktype.selectielijst_procestype:
            # Derive the `selectielijst_procestype_jaar`, even if it was already set
            # previously, because migration `0006_auto_20200817_1037` always sets it to
            # 2017 (which could be incorrect)
            client = Service.get_client(zaaktype.selectielijst_procestype)
            response = client.retrieve(
                "selectielijst_procestype", url=zaaktype.selectielijst_procestype
            )
            zaaktype.selectielijst_procestype_jaar = response["jaar"]
            zaaktype.save()


class Migration(migrations.Migration):

    dependencies = [
        ("catalogi", "0010_auto_20210628_0848"),
    ]

    operations = [
        migrations.RunPython(
            set_selectieklasse_procestype_default_year, migrations.RunPython.noop
        )
    ]