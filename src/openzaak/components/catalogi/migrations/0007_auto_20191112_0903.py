# Generated by Django 2.2.4 on 2019-11-12 09:03

from django.db import migrations, models
import vng_api_common.validators


class Migration(migrations.Migration):

    dependencies = [
        ("catalogi", "0006_auto_20191024_1000"),
    ]

    operations = [
        migrations.AlterField(
            model_name="zaaktype",
            name="zaaktype_identificatie",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="Unieke identificatie van het ZAAKTYPE binnen de CATALOGUS waarin het ZAAKTYPE voorkomt.",
                max_length=50,
                validators=[vng_api_common.validators.AlphanumericExcludingDiacritic()],
                verbose_name="identificatie",
            ),
        ),
    ]
