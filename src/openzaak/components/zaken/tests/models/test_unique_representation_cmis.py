# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2020 Dimpact
from django.test import override_settings

from zgw_consumers.constants import APITypes
from zgw_consumers.models import Service

from openzaak.components.documenten.tests.factories import (
    EnkelvoudigInformatieObjectFactory,
)
from openzaak.tests.utils import APICMISTestCase, require_cmis

from ..factories import ZaakInformatieObjectFactory


@require_cmis
@override_settings(CMIS_ENABLED=True)
class UniqueRepresentationCMISTestCase(APICMISTestCase):
    def test_zaakinformatieobject(self):
        Service.objects.create(
            api_root="http://testserver/documenten/api/v1/", api_type=APITypes.drc
        )
        Service.objects.create(
            api_root="http://testserver/catalogi/api/v1/", api_type=APITypes.ztc
        )
        Service.objects.create(
            api_root="http://testserver/zaken/api/v1/", api_type=APITypes.zrc
        )
        eio = EnkelvoudigInformatieObjectFactory.create(identificatie="12345")
        eio_url = eio.get_url()

        zio = ZaakInformatieObjectFactory(
            zaak__bronorganisatie=730924658,
            zaak__identificatie="5d940d52-ff5e-4b18-a769-977af9130c04",
            informatieobject=eio_url,
        )

        self.assertEqual(
            zio.unique_representation(),
            "(730924658 - 5d940d52-ff5e-4b18-a769-977af9130c04) - 12345",
        )
