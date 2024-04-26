import csv
import logging
from pathlib import Path
from random import choice
from typing import Iterable

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.urls import reverse

from openzaak.components.catalogi.models.informatieobjecttype import (
    InformatieObjectType,
)
from openzaak.components.documenten.tests.factories import (
    EnkelvoudigInformatieObjectFactory,
)
from openzaak.components.zaken.models.zaken import Zaak
from openzaak.utils.tasks import DocumentRow, _get_total_count

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Command which creates an export CSV which could be loaded through the
    `import_documents` celery task.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "export_file",
            type=str,
            help="File which the commands writes the export data to",
        )

        parser.add_argument(
            "dummy_path",
            type=str,
            help="Dummy file used for the file path value in the export",
        )

        parser.add_argument(
            "--row_count",
            type=int,
            default=100000,
            help="The amount of CSV rows to create",
        )

        parser.add_argument(
            "--batch_size", type=int, default=1000,
        )

    def handle(self, *args, **options):
        export_file = options["export_file"]
        total = options["row_count"]
        batch_size = options["batch_size"]
        dummy_path = options["dummy_path"]

        site = Site.objects.get_current()
        zaken = Zaak.objects.values_list("uuid", flat=True)
        informatieobject_typen = InformatieObjectType.objects.values_list(
            "uuid", flat=True
        )

        headers = (
            "identificatie",
            "bronorganisatie",
            "creatiedatum",
            "titel",
            "vertrouwelijkheidaanduiding",
            "auteur",
            "status",
            "formaat",
            "taal",
            "bestandsnaam",
            "bestandsomvang",
            "bestandspad",
            "link",
            "beschrijving",
            "indicatieGebruiksrecht",
            "verschijningsvorm",
            "ondertekening.soort",
            "ondertekening.datum",
            "integriteit.algoritme",
            "integriteit.waarde",
            "integriteit.datum",
            "informatieobjecttype",
            "zaakId",
            "trefwoorden",
        )

        batch = []
        processed = 0

        while processed != total:
            batch_number = int(processed / batch_size) + 1

            if not batch or processed % batch_size == 0:
                logger.debug("Generating new batch")

                batch = self._get_batch(
                    batch_size, zaken, informatieobject_typen, site.domain, dummy_path
                )

            file_exists = Path(export_file).exists()
            has_data = bool(_get_total_count(export_file)) if file_exists else False

            if file_exists and has_data:
                mode = "a"
            elif file_exists:
                mode = "w"
            else:
                mode = "w+"

            logger.debug(f"Writing to export file with filemode {mode}")
            logger.debug(f"Writing batch number {batch_number} to report file")

            with open(export_file, mode) as _export_file:
                csv_writer = csv.writer(_export_file, delimiter=",", quotechar='"')

                if mode in ("w", "w+"):
                    csv_writer.writerow(headers)

                for row in batch:
                    data = row.as_original()
                    csv_writer.writerow(data.values())

            logger.info(f"Batch {batch_number} done")

            processed += len(batch)

            logger.info(
                f"{int((total / batch_size) - (processed / batch_size))} batches remaining"
            )

    def _get_batch(
        self,
        batch_size: int,
        zaken: Iterable[str],
        informatieobject_typen: Iterable[str],
        site_domain: str,
        dummy_path: str,
    ) -> list[DocumentRow]:

        document_data = []

        for _ in range(batch_size):
            zaak_uuid = choice(zaken)
            informatie_object_uuid = choice(informatieobject_typen)

            zaak_path = reverse("zaak-detail", kwargs=dict(uuid=zaak_uuid, version=1))
            zaak_url = f"https://{site_domain}{zaak_path}"

            informatie_object_path = reverse(
                "informatieobjecttype-detail",
                kwargs=dict(uuid=informatie_object_uuid, version=1),
            )
            informatie_object_url = f"https://{site_domain}{informatie_object_path}"

            instance = EnkelvoudigInformatieObjectFactory.build(
                informatieobjecttype__uuid=informatie_object_uuid,
                ondertekening_soort="foo",
                ondertekening_datum="2024-04-26",
                integriteit_algoritme="crc_16",
                integriteit_waarde="foo",
                integriteit_datum="2024-04-26",
            )

            indicatie_gebruiksrecht = (
                "true" if instance.indicatie_gebruiksrecht else "false"
            )

            row = DocumentRow(
                instance.identificatie,
                instance.bronorganisatie,
                instance.creatiedatum,
                instance.titel,
                instance.vertrouwelijkheidaanduiding,
                instance.auteur,
                instance.status,
                instance.formaat,
                instance.taal,
                instance.bestandsnaam,
                instance.bestandsomvang,
                dummy_path,
                instance.link,
                instance.beschrijving,
                indicatie_gebruiksrecht,
                instance.verschijningsvorm or "",
                instance.ondertekening["soort"],
                instance.ondertekening["datum"],
                instance.integriteit["algoritme"],
                instance.integriteit["waarde"],
                instance.integriteit["datum"],
                informatie_object_url,
                zaak_url,
                '"foobar,foobar"',
            )

            document_data.append(row)

        return document_data
