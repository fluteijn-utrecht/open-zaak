# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2023 Dimpact
# Generated by Django 3.2.18 on 2023-09-27 14:38

from django.db import migrations, models
import django.db.models.deletion
import openzaak.components.catalogi.models.validators
import vng_api_common.fields
import vng_api_common.validators


class Migration(migrations.Migration):

    dependencies = [
        ("catalogi", "0018_fill_zaaktype_verantwoordelijke"),
    ]

    operations = [
        migrations.AddField(
            model_name="zaaktype",
            name="broncatalogus_domein",
            field=models.CharField(
                blank=True,
                help_text="Het domein van de CATALOGUS waaraan het ZAAKTYPE is ontleend.",
                max_length=5,
                validators=[
                    openzaak.components.catalogi.models.validators.validate_uppercase
                ],
                verbose_name="broncatalogus domein",
            ),
        ),
        migrations.AddField(
            model_name="zaaktype",
            name="broncatalogus_rsin",
            field=vng_api_common.fields.RSINField(
                blank=True,
                help_text="Het RSIN van de INGESCHREVEN NIET-NATUURLIJK PERSOON die beheerder is van de CATALOGUS waaraan het ZAAKTYPE is ontleend.",
                max_length=9,
                verbose_name="broncatalogus rsin",
            ),
        ),
        migrations.AddField(
            model_name="zaaktype",
            name="broncatalogus_url",
            field=models.URLField(
                blank=True,
                help_text="URL-referentie naar broncatalogus",
                verbose_name="broncatalogus url",
            ),
        ),
        migrations.AddField(
            model_name="zaaktype",
            name="bronzaaktype_identificatie",
            field=models.CharField(
                blank=True,
                help_text="De Zaaktype-identificatie van het bronzaaktype binnen de CATALOGUS.",
                max_length=50,
                validators=[vng_api_common.validators.AlphanumericExcludingDiacritic()],
                verbose_name="bronzaaktype identificatie",
            ),
        ),
        migrations.AddField(
            model_name="zaaktype",
            name="bronzaaktype_omschrijving",
            field=models.CharField(
                blank=True,
                help_text="De Zaaktype-omschrijving van het bronzaaktype, zoals gehanteerd in de Broncatalogus.",
                max_length=80,
                verbose_name="bronzaaktype omschrijving",
            ),
        ),
        migrations.AddField(
            model_name="zaaktype",
            name="bronzaaktype_url",
            field=models.URLField(
                blank=True,
                help_text="URL-referentie naar bronzaaktype",
                verbose_name="bronzaaktype url",
            ),
        ),
        migrations.AddField(
            model_name="zaakobjecttype",
            name="statustype",
            field=models.ForeignKey(
                blank=True,
                help_text="URL-referentie naar het STATUSTYPE",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="zaakobjecttypen",
                to="catalogi.statustype",
            ),
        ),
        migrations.RemoveField(model_name="statustype", name="zaakobjecttype",),
    ]
