# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2023 Dimpact
# Generated by Django 3.2.18 on 2023-08-07 09:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import openzaak.components.documenten.caching
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("documenten", "0027_auto_20230417_1415"),
    ]

    operations = [
        migrations.CreateModel(
            name="Verzending",
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
                    "betrokkene",
                    models.URLField(
                        help_text="URL-referentie naar de betrokkene waarvan het informatieobject is ontvangen of waaraan dit is verzonden.",
                        verbose_name="betrokkene",
                    ),
                ),
                (
                    "aard_relatie",
                    models.CharField(
                        choices=[
                            ("afzender", "Afzender"),
                            ("geadresseerde", "Geadresseerde"),
                        ],
                        help_text="Omschrijving van de aard van de relatie van de BETROKKENE tot het INFORMATIEOBJECT.",
                        max_length=255,
                        verbose_name="aard relatie",
                    ),
                ),
                (
                    "telefoonnummer",
                    models.CharField(
                        blank=True,
                        help_text="telefoonnummer van de ontvanger of afzender.",
                        max_length=15,
                        verbose_name="telefoonnummer",
                    ),
                ),
                (
                    "faxnummer",
                    models.CharField(
                        blank=True,
                        help_text="faxnummer van de ontvanger of afzender.",
                        max_length=15,
                        verbose_name="faxnummer",
                    ),
                ),
                (
                    "emailadres",
                    models.EmailField(
                        blank=True,
                        help_text="emailadres van de ontvanger of afzender.",
                        max_length=100,
                        verbose_name="emailadres",
                    ),
                ),
                (
                    "mijn_overheid",
                    models.BooleanField(
                        default=False,
                        help_text="is het informatieobject verzonden via mijnOverheid naar de ontvanger.",
                        verbose_name="mijn overheid",
                    ),
                ),
                (
                    "toelichting",
                    models.CharField(
                        blank=True,
                        help_text="Verduidelijking van de afzender- of geadresseerde-relatie.",
                        max_length=200,
                        verbose_name="toelichting",
                    ),
                ),
                (
                    "ontvangstdatum",
                    models.DateField(
                        blank=True,
                        help_text="De datum waarop het INFORMATIEOBJECT ontvangen is. Verplicht te registreren voor INFORMATIEOBJECTen die van buiten de zaakbehandelende organisatie(s) ontvangen zijn. Ontvangst en verzending is voorbehouden aan documenten die van of naar andere personen ontvangen of verzonden zijn waarbij die personen niet deel uit maken van de behandeling van de zaak waarin het document een rol speelt. Vervangt het gelijknamige attribuut uit Informatieobject. Verplicht gevuld wanneer aardRelatie de waarde 'afzender' heeft.",
                        null=True,
                        verbose_name="ontvangstdatum",
                    ),
                ),
                (
                    "verzenddatum",
                    models.DateField(
                        blank=True,
                        help_text="De datum waarop het INFORMATIEOBJECT verzonden is, zoals deze op het INFORMATIEOBJECT vermeld is. Dit geldt voor zowel inkomende als uitgaande INFORMATIEOBJECTen. Eenzelfde informatieobject kan niet tegelijk inkomend en uitgaand zijn. Ontvangst en verzending is voorbehouden aan documenten die van of naar andere personen ontvangen of verzonden zijn waarbij die personen niet deel uit maken van de behandeling van de zaak waarin het document een rol speelt. Vervangt het gelijknamige attribuut uit Informatieobject. Verplicht gevuld wanneer aardRelatie de waarde 'geadresseerde' heeft.",
                        null=True,
                        verbose_name="verzenddatum",
                    ),
                ),
                (
                    "contact_persoon",
                    models.URLField(
                        help_text="URL-referentie naar de persoon die als aanspreekpunt fungeert voor de BETROKKENE inzake het ontvangen of verzonden INFORMATIEOBJECT.",
                        max_length=1000,
                        verbose_name="contactpersoon",
                    ),
                ),
                (
                    "contactpersoonnaam",
                    models.CharField(
                        blank=True,
                        help_text="De opgemaakte naam van de persoon die als aanspreekpunt fungeert voorde BETROKKENE inzake het ontvangen of verzonden INFORMATIEOBJECT.",
                        max_length=40,
                        verbose_name="contactpersoonnaam",
                    ),
                ),
                (
                    "binnenlands_correspondentieadres_huisletter",
                    models.CharField(
                        blank=True,
                        help_text="Een door of namens het bevoegd gemeentelijk orgaan ten aanzien van een adresseerbaar object toegekende toevoeging aan een huisnummer in de vorm van een alfanumeriek teken.",
                        max_length=1,
                        verbose_name="huisletter",
                    ),
                ),
                (
                    "binnenlands_correspondentieadres_huisnummer",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Een door of namens het bevoegd gemeentelijk orgaan ten aanzien van een adresseerbaar object toegekende nummering.",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(99999),
                        ],
                        verbose_name="huisnummer",
                    ),
                ),
                (
                    "binnenlands_correspondentieadres_huisnummer_toevoeging",
                    models.CharField(
                        blank=True,
                        help_text="Een door of namens het bevoegd gemeentelijk orgaan ten aanzien van een adresseerbaar object toegekende nadere toevoeging aan een huisnummer of een combinatie van huisnummer en huisletter.",
                        max_length=4,
                        verbose_name="huisnummer toevoeging",
                    ),
                ),
                (
                    "binnenlands_correspondentieadres_naam_openbare_ruimte",
                    models.CharField(
                        blank=True,
                        help_text="Een door het bevoegde gemeentelijke orgaan aan een GEMEENTELIJKE  OPENBARE RUIMTE toegekende benaming.",
                        max_length=80,
                        verbose_name="naam openbare ruimte",
                    ),
                ),
                (
                    "binnenlands_correspondentieadres_postcode",
                    models.CharField(
                        blank=True,
                        help_text="De door TNT Post vastgestelde code behorende bij een bepaalde combinatie van een naam van een woonplaats, naam van een openbare ruimte en een huisnummer.",
                        max_length=6,
                        verbose_name="postcode",
                    ),
                ),
                (
                    "binnenlands_correspondentieadres_woonplaats",
                    models.CharField(
                        blank=True,
                        help_text="De door het bevoegde gemeentelijke orgaan aan een WOONPLAATS toegekende benaming.",
                        max_length=80,
                        verbose_name="woonplaatsnaam",
                    ),
                ),
                (
                    "buitenlands_correspondentieadres_adres_buitenland_1",
                    models.CharField(
                        blank=True,
                        help_text="Het eerste deel dat behoort bij het afwijkend buitenlandse correspondentieadres van de betrokkene in zijn/haar rol bij de zaak.",
                        max_length=35,
                        verbose_name="adres buitenland 1",
                    ),
                ),
                (
                    "buitenlands_correspondentieadres_adres_buitenland_2",
                    models.CharField(
                        blank=True,
                        help_text="Het tweede deel dat behoort bij het afwijkend buitenlandse correspondentieadres van de betrokkene in zijn/haar rol bij de zaak.",
                        max_length=35,
                        verbose_name="adres buitenland 2",
                    ),
                ),
                (
                    "buitenlands_correspondentieadres_adres_buitenland_3",
                    models.CharField(
                        blank=True,
                        help_text="Het derde deel dat behoort bij het afwijkend buitenlandse correspondentieadres van de betrokkene in zijn/haar rol bij de zaak.",
                        max_length=35,
                        verbose_name="adres buitenland 3",
                    ),
                ),
                (
                    "buitenlands_correspondentieadres_land_postadres",
                    models.URLField(
                        blank=True,
                        help_text="Het LAND dat behoort bij het afwijkend buitenlandse correspondentieadres van de betrokkene in zijn/haar rol bij de zaak.",
                        verbose_name="land postadres",
                    ),
                ),
                (
                    "buitenlands_correspondentiepostadres_postbus_of_antwoord_nummer",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="De numerieke aanduiding zoals deze door de Nederlandse PTT is vastgesteld voor postbusadressen en antwoordnummeradressen.",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(9999),
                        ],
                        verbose_name="postbus-of antwoordnummer",
                    ),
                ),
                (
                    "buitenlands_correspondentiepostadres_postadres_postcode",
                    models.CharField(
                        blank=True,
                        help_text="De officiële Nederlandse PTT codering, bestaande uit een numerieke woonplaatscode en een alfabetische lettercode.",
                        max_length=6,
                        verbose_name="postadres postcode",
                    ),
                ),
                (
                    "buitenlands_correspondentiepostadres_postadrestype",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("antwoordnummer", "Antwoordnummer"),
                            ("postbusnummer", "Postbusnummer"),
                        ],
                        help_text="Aanduiding van het soort postadres.",
                        max_length=255,
                        verbose_name="postadrestype",
                    ),
                ),
                (
                    "buitenlands_correspondentiepostadres_woonplaats",
                    models.CharField(
                        blank=True,
                        help_text="De door het bevoegde gemeentelijke orgaan aan een WOONPLAATS toegekende benaming.",
                        max_length=80,
                        verbose_name="woonplaatsnaam",
                    ),
                ),
                (
                    "informatieobject",
                    models.ForeignKey(
                        help_text="URL-referentie naar het informatieobject dat is ontvangen of verzonden.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="verzendingen",
                        to="documenten.enkelvoudiginformatieobjectcanonical",
                        verbose_name="informatieobject",
                    ),
                ),
            ],
            options={
                "verbose_name": "Verzending",
                "verbose_name_plural": "Verzendingen",
            },
            bases=(openzaak.components.documenten.caching.CMISETagMixin, models.Model),
        ),
    ]
