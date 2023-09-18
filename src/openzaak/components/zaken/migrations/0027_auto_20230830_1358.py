# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2023 Dimpact
# Generated by Django 3.2.18 on 2023-08-30 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zaken", "0026_auto_20230824_1218"),
    ]

    operations = [
        migrations.AddField(
            model_name="rol",
            name="afwijkende_naam_betrokkene",
            field=models.TextField(
                blank=True,
                help_text="De naam van de betrokkene waaronder deze in relatie tot de zaak aangesproken wil worden.",
                max_length=625,
                verbose_name="afwijkende naam betrokkene",
            ),
        ),
        migrations.AddField(
            model_name="rol",
            name="contactpersoon_rol_emailadres",
            field=models.EmailField(
                blank=True,
                help_text="Elektronich postadres waaronder de contactpersoon in de regel bereikbaar is.",
                max_length=254,
                verbose_name="email",
            ),
        ),
        migrations.AddField(
            model_name="rol",
            name="contactpersoon_rol_functie",
            field=models.CharField(
                blank=True,
                help_text="De aanduiding van de taken, rechten en plichten die de contactpersoon heeft binnen de organisatie van BETROKKENE. ",
                max_length=50,
                verbose_name="functie",
            ),
        ),
        migrations.AddField(
            model_name="rol",
            name="contactpersoon_rol_naam",
            field=models.CharField(
                blank=True,
                help_text="De opgemaakte naam van de contactpersoon namens de BETROKKENE.",
                max_length=200,
                verbose_name="naam",
            ),
        ),
        migrations.AddField(
            model_name="rol",
            name="contactpersoon_rol_telefoonnummer",
            field=models.CharField(
                blank=True,
                help_text="Telefoonnummer waaronder de contactpersoon in de regel bereikbaar is.",
                max_length=20,
                verbose_name="telefoonnummer",
            ),
        ),
        migrations.AddField(
            model_name="vestiging",
            name="kvk_nummer",
            field=models.CharField(
                blank=True,
                help_text="Een uniek nummer gekoppeld aan de onderneming.",
                max_length=8,
            ),
        ),
    ]