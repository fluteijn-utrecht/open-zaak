# Generated by Django 3.2.14 on 2022-08-15 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("zgw_consumers", "0015_auto_20220307_1522"),
        ("zaken", "0009_merge_20220725_1359"),
    ]

    operations = [
        migrations.AddField(
            model_name="relevantezaakrelatie",
            name="_relevant_zaak_base_url",
            field=models.ForeignKey(
                blank=True,
                help_text="Basis deel van URL-referentie naar extern ZAAK (in een andere Zaken API).",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="zgw_consumers.service",
            ),
        ),
        migrations.AddField(
            model_name="relevantezaakrelatie",
            name="_relevant_zaak_relative_url",
            field=models.CharField(
                blank=True,
                help_text="Relatief deel van URL-referentie naar extern ZAAK (in een andere Zaken API).",
                max_length=200,
                null=True,
                verbose_name="relevant zaak relative url",
            ),
        ),
        migrations.AddField(
            model_name="resultaat",
            name="_resultaattype_base_url",
            field=models.ForeignKey(
                blank=True,
                help_text="Basis deel van URL-referentie naar extern RESULTAATTYPE (in een andere Catalogi API).",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="zgw_consumers.service",
            ),
        ),
        migrations.AddField(
            model_name="resultaat",
            name="_resultaattype_relative_url",
            field=models.CharField(
                blank=True,
                help_text="Relatief deel van URL-referentie naar extern RESULTAATTYPE (in een andere Catalogi API).",
                max_length=200,
                null=True,
                verbose_name="resultaattype relative url",
            ),
        ),
        migrations.AddField(
            model_name="rol",
            name="_roltype_base_url",
            field=models.ForeignKey(
                blank=True,
                help_text="Basis deel van URL-referentie naar extern ROLTYPE (in een andere Catalogi API).",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="zgw_consumers.service",
            ),
        ),
        migrations.AddField(
            model_name="rol",
            name="_roltype_relative_url",
            field=models.CharField(
                blank=True,
                help_text="Relatief deel van URL-referentie naar extern ROLTYPE (in een andere Catalogi API).",
                max_length=200,
                null=True,
                verbose_name="roltype relative url",
            ),
        ),
        migrations.AddField(
            model_name="status",
            name="_statustype_base_url",
            field=models.ForeignKey(
                blank=True,
                help_text="Basis deel van URL-referentie naar extern STATUSTYPE (in een andere Catalogi API).",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="zgw_consumers.service",
            ),
        ),
        migrations.AddField(
            model_name="status",
            name="_statustype_relative_url",
            field=models.CharField(
                blank=True,
                help_text="Relatief deel van URL-referentie naar extern STATUSTYPE (in een andere Catalogi API).",
                max_length=200,
                null=True,
                verbose_name="statustype relative url",
            ),
        ),
        migrations.AddField(
            model_name="zaak",
            name="_zaaktype_base_url",
            field=models.ForeignKey(
                blank=True,
                help_text="Basis deel van URL-referentie naar het extern ZAAKTYPE (in een andere Catalogi API).",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="zgw_consumers.service",
            ),
        ),
        migrations.AddField(
            model_name="zaak",
            name="_zaaktype_relative_url",
            field=models.CharField(
                blank=True,
                help_text="Relatief deel van URL-referentie naar het extern ZAAKTYPE (in een andere Catalogi API).",
                max_length=200,
                null=True,
                verbose_name="zaaktype relative url",
            ),
        ),
        migrations.AddField(
            model_name="zaakbesluit",
            name="_besluit_base_url",
            field=models.ForeignKey(
                blank=True,
                help_text="Basis deel van URL-referentie naar externe BESLUIT (in een andere Besluiten API).",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="zgw_consumers.service",
            ),
        ),
        migrations.AddField(
            model_name="zaakbesluit",
            name="_besluit_relative_url",
            field=models.CharField(
                blank=True,
                help_text="Relatief deel van URL-referentie naar externe BESLUIT (in een andere Besluiten API).",
                max_length=200,
                null=True,
                verbose_name="besluit relative url",
            ),
        ),
        migrations.AddField(
            model_name="zaakeigenschap",
            name="_eigenschap_base_url",
            field=models.ForeignKey(
                blank=True,
                help_text="Basis deel van URL-referentie naar extern EIGENSCHAP (in een andere Catalogi API).",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="zgw_consumers.service",
            ),
        ),
        migrations.AddField(
            model_name="zaakeigenschap",
            name="_eigenschap_relative_url",
            field=models.CharField(
                blank=True,
                help_text="Relatief deel van URL-referentie naar extern EIGENSCHAP (in een andere Catalogi API).",
                max_length=200,
                null=True,
                verbose_name="eigenschap relative url",
            ),
        ),
        migrations.AddField(
            model_name="zaakinformatieobject",
            name="_informatieobject_base_url",
            field=models.ForeignKey(
                blank=True,
                help_text="Basis deel van URL-referentie naar de externe API",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="zgw_consumers.service",
            ),
        ),
        migrations.AddField(
            model_name="zaakinformatieobject",
            name="_informatieobject_relative_url",
            field=models.CharField(
                blank=True,
                help_text="Relatief deel van URL-referentie naar de externe API",
                max_length=500,
                null=True,
                verbose_name="informatieobject relative url",
            ),
        ),
    ]
