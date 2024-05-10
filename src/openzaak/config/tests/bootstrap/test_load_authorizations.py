# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2024 Dimpact

import tempfile
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase, override_settings

import yaml
from vng_api_common.authorizations.models import Applicatie, Autorisatie
from vng_api_common.constants import ComponentTypes, VertrouwelijkheidsAanduiding
from vng_api_common.models import JWTSecret

from openzaak.components.autorisaties.models import AutorisatieSpec
from openzaak.components.autorisaties.tests.factories import (
    ApplicatieFactory,
    AutorisatieFactory,
    AutorisatieSpecFactory,
)
from openzaak.components.besluiten.api.scopes import SCOPE_BESLUITEN_ALLES_LEZEN
from openzaak.components.zaken.api.scopes import (
    SCOPE_ZAKEN_ALLES_LEZEN,
    SCOPE_ZAKEN_CREATE,
)
from openzaak.config.bootstrap.authorizations import AuthorizationConfigurationStep

ZAAKTYPE1 = "https://acc.openzaak.nl/zaaktypen/1"
ZAAKTYPE2 = "https://external.acc.openzaak.nl/zaaktypen/2"
ZAAKTYPE3 = "https://acc.openzaak.nl/zaaktypen/3"
ZAAKTYPE4 = "https://acc.openzaak.nl/zaaktypen/4"


class AuthorizationConfigurationTests(TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

        self.temp_dir = tempfile.TemporaryDirectory()
        self.dump_path = str(Path(self.temp_dir.name) / "auth_dump.yaml")
        self.addCleanup(self.temp_dir.cleanup)

        self.jwt_secret_oz = JWTSecret.objects.create(
            identifier="open-zaak", secret="oz-secret"
        )
        self.jwt_secret_on = JWTSecret.objects.create(
            identifier="open-notificaties", secret="on-secret"
        )
        self.applicatie_oz = ApplicatieFactory.create(client_ids=["open-zaak"])
        self.applicatie_on = ApplicatieFactory.create(client_ids=["open-notificaties"])
        self.autorisatie_oz = AutorisatieFactory.create(
            applicatie=self.applicatie_oz,
            component=ComponentTypes.zrc,
            scopes=[SCOPE_ZAKEN_CREATE, SCOPE_ZAKEN_ALLES_LEZEN],
            zaaktype=ZAAKTYPE1,
            max_vertrouwelijkheidaanduiding=VertrouwelijkheidsAanduiding.geheim,
        )
        self.autorisatiespec = AutorisatieSpecFactory.create(
            applicatie=self.applicatie_oz,
            component=ComponentTypes.brc,
            scopes=[SCOPE_BESLUITEN_ALLES_LEZEN],
            max_vertrouwelijkheidaanduiding=VertrouwelijkheidsAanduiding.geheim,
        )
        self.autorisatie_on = AutorisatieFactory.create(
            applicatie=self.applicatie_on,
            component=ComponentTypes.zrc,
            scopes=[SCOPE_ZAKEN_ALLES_LEZEN],
            zaaktype=ZAAKTYPE2,
            max_vertrouwelijkheidaanduiding=VertrouwelijkheidsAanduiding.openbaar,
        )

        call_command(
            "dump_auth_fixtures", str(Path(self.temp_dir.name) / "auth_dump.yaml")
        )

        self.jwt_secret_oz.delete()
        self.jwt_secret_on.delete()
        self.applicatie_oz.delete()
        self.applicatie_on.delete()
        self.autorisatie_oz.delete()
        self.autorisatiespec.delete()
        self.autorisatie_on.delete()

    def test_configure(self):
        with override_settings(AUTHORIZATIONS_CONFIG_FIXTURE_PATH=self.dump_path):
            AuthorizationConfigurationStep().configure()

        self.assertEqual(JWTSecret.objects.count(), 2)
        self.assertEqual(Applicatie.objects.count(), 2)
        self.assertEqual(Applicatie.objects.count(), 2)
        self.assertEqual(Autorisatie.objects.count(), 2)
        self.assertEqual(AutorisatieSpec.objects.count(), 1)

        jwt_secret_oz = JWTSecret.objects.get(identifier="open-zaak")
        self.assertEqual(jwt_secret_oz.secret, "oz-secret")

        jwt_secret_on = JWTSecret.objects.get(identifier="open-notificaties")
        self.assertEqual(jwt_secret_on.secret, "on-secret")

        applicatie_oz = Applicatie.objects.get(client_ids=["open-zaak"])

        autorisatie_oz = applicatie_oz.autorisaties.get()
        self.assertEqual(autorisatie_oz.component, ComponentTypes.zrc)
        self.assertEqual(
            autorisatie_oz.scopes,
            [str(SCOPE_ZAKEN_CREATE), str(SCOPE_ZAKEN_ALLES_LEZEN)],
        )
        self.assertEqual(autorisatie_oz.zaaktype, ZAAKTYPE1)
        self.assertEqual(
            autorisatie_oz.max_vertrouwelijkheidaanduiding,
            VertrouwelijkheidsAanduiding.geheim,
        )

        autorisatiespec_oz = applicatie_oz.autorisatie_specs.get()
        self.assertEqual(autorisatiespec_oz.component, ComponentTypes.brc)
        self.assertEqual(autorisatiespec_oz.scopes, [str(SCOPE_BESLUITEN_ALLES_LEZEN)])
        self.assertEqual(
            autorisatiespec_oz.max_vertrouwelijkheidaanduiding,
            VertrouwelijkheidsAanduiding.geheim,
        )

        applicatie_on = Applicatie.objects.get(client_ids=["open-notificaties"])

        autorisatie_on = applicatie_on.autorisaties.get()
        self.assertEqual(autorisatie_on.component, ComponentTypes.zrc)
        self.assertEqual(autorisatie_on.scopes, [str(SCOPE_ZAKEN_ALLES_LEZEN)])
        self.assertEqual(autorisatie_on.zaaktype, ZAAKTYPE2)
        self.assertEqual(
            autorisatie_on.max_vertrouwelijkheidaanduiding,
            VertrouwelijkheidsAanduiding.openbaar,
        )

    def test_configure_domain_mapping(self):
        mapping_path = Path(self.temp_dir.name) / "mapping.yaml"
        with open(mapping_path, "w") as f:
            mapping = [
                {
                    "acceptance": "https://acc.openzaak.nl",
                    "production": "https://openzaak.nl",
                },
                {
                    "acceptance": "https://external.acc.openzaak.nl",
                    "production": "https://external.openzaak.nl",
                },
            ]
            yaml.safe_dump(mapping, f)

        with override_settings(
            AUTHORIZATIONS_CONFIG_FIXTURE_PATH=self.dump_path,
            AUTHORIZATIONS_CONFIG_DOMAIN_MAPPING_PATH=mapping_path,
            ENVIRONMENT="production",
        ):
            AuthorizationConfigurationStep().configure()

        self.assertEqual(JWTSecret.objects.count(), 2)
        self.assertEqual(Applicatie.objects.count(), 2)
        self.assertEqual(Applicatie.objects.count(), 2)
        self.assertEqual(Autorisatie.objects.count(), 2)
        self.assertEqual(AutorisatieSpec.objects.count(), 1)

        jwt_secret_oz = JWTSecret.objects.get(identifier="open-zaak")
        self.assertEqual(jwt_secret_oz.secret, "oz-secret")

        jwt_secret_on = JWTSecret.objects.get(identifier="open-notificaties")
        self.assertEqual(jwt_secret_on.secret, "on-secret")

        applicatie_oz = Applicatie.objects.get(client_ids=["open-zaak"])

        autorisatie_oz = applicatie_oz.autorisaties.get()
        self.assertEqual(autorisatie_oz.component, ComponentTypes.zrc)
        self.assertEqual(
            autorisatie_oz.scopes,
            [str(SCOPE_ZAKEN_CREATE), str(SCOPE_ZAKEN_ALLES_LEZEN)],
        )
        self.assertEqual(autorisatie_oz.zaaktype, "https://openzaak.nl/zaaktypen/1")
        self.assertEqual(
            autorisatie_oz.max_vertrouwelijkheidaanduiding,
            VertrouwelijkheidsAanduiding.geheim,
        )

        autorisatiespec_oz = applicatie_oz.autorisatie_specs.get()
        self.assertEqual(autorisatiespec_oz.component, ComponentTypes.brc)
        self.assertEqual(autorisatiespec_oz.scopes, [str(SCOPE_BESLUITEN_ALLES_LEZEN)])
        self.assertEqual(
            autorisatiespec_oz.max_vertrouwelijkheidaanduiding,
            VertrouwelijkheidsAanduiding.geheim,
        )

        applicatie_on = Applicatie.objects.get(client_ids=["open-notificaties"])

        autorisatie_on = applicatie_on.autorisaties.get()
        self.assertEqual(autorisatie_on.component, ComponentTypes.zrc)
        self.assertEqual(autorisatie_on.scopes, [str(SCOPE_ZAKEN_ALLES_LEZEN)])
        self.assertEqual(
            autorisatie_on.zaaktype, "https://external.openzaak.nl/zaaktypen/2"
        )
        self.assertEqual(
            autorisatie_on.max_vertrouwelijkheidaanduiding,
            VertrouwelijkheidsAanduiding.openbaar,
        )

    def test_configure_overwrite(self):
        """
        Running `.configure` twice should overwrite any changes made to the configurated
        Applicaties, Autorisaties, AutorisatieSpecs and JWTSecrets
        """
        with override_settings(AUTHORIZATIONS_CONFIG_FIXTURE_PATH=self.dump_path):
            AuthorizationConfigurationStep().configure()

        secret_oz, secret_on = JWTSecret.objects.all()

        secret_oz.secret = "modified-secret"
        secret_oz.save()
        secret_on.secret = "modified-secret"
        secret_on.save()

        applicatie_oz, applicatie_on = Applicatie.objects.all()
        applicatie_oz.label = "Open Zaak"
        applicatie_oz.save()
        applicatie_oz.label = "Open Notificaties"
        applicatie_oz.save()

        autorisatie_oz = applicatie_oz.autorisaties.first()
        autorisatie_on = applicatie_on.autorisaties.first()

        autorisatie_oz.zaaktype = ZAAKTYPE3
        autorisatie_oz.save()
        autorisatie_on.zaaktype = ZAAKTYPE4
        autorisatie_on.save()

        autorisatiespec_oz = applicatie_oz.autorisatie_specs.first()

        autorisatiespec_oz.max_vertrouwelijkheidaanduiding = (
            VertrouwelijkheidsAanduiding.openbaar
        )
        autorisatiespec_oz.save()

        # Overwrite the changes
        with override_settings(AUTHORIZATIONS_CONFIG_FIXTURE_PATH=self.dump_path):
            AuthorizationConfigurationStep().configure()

        self.assertEqual(JWTSecret.objects.count(), 2)
        self.assertEqual(Applicatie.objects.count(), 2)
        self.assertEqual(Applicatie.objects.count(), 2)
        self.assertEqual(Autorisatie.objects.count(), 2)
        self.assertEqual(AutorisatieSpec.objects.count(), 1)

        jwt_secret_oz = JWTSecret.objects.get(identifier="open-zaak")
        self.assertEqual(jwt_secret_oz.secret, "oz-secret")

        jwt_secret_on = JWTSecret.objects.get(identifier="open-notificaties")
        self.assertEqual(jwt_secret_on.secret, "on-secret")

        applicatie_oz = Applicatie.objects.get(client_ids=["open-zaak"])

        autorisatie_oz = applicatie_oz.autorisaties.get()
        self.assertEqual(autorisatie_oz.component, ComponentTypes.zrc)
        self.assertEqual(
            autorisatie_oz.scopes,
            [str(SCOPE_ZAKEN_CREATE), str(SCOPE_ZAKEN_ALLES_LEZEN)],
        )
        self.assertEqual(autorisatie_oz.zaaktype, ZAAKTYPE1)
        self.assertEqual(
            autorisatie_oz.max_vertrouwelijkheidaanduiding,
            VertrouwelijkheidsAanduiding.geheim,
        )

        autorisatiespec_oz = applicatie_oz.autorisatie_specs.get()
        self.assertEqual(autorisatiespec_oz.component, ComponentTypes.brc)
        self.assertEqual(autorisatiespec_oz.scopes, [str(SCOPE_BESLUITEN_ALLES_LEZEN)])
        self.assertEqual(
            autorisatiespec_oz.max_vertrouwelijkheidaanduiding,
            VertrouwelijkheidsAanduiding.geheim,
        )

        applicatie_on = Applicatie.objects.get(client_ids=["open-notificaties"])

        autorisatie_on = applicatie_on.autorisaties.get()
        self.assertEqual(autorisatie_on.component, ComponentTypes.zrc)
        self.assertEqual(autorisatie_on.scopes, [str(SCOPE_ZAKEN_ALLES_LEZEN)])
        self.assertEqual(autorisatie_on.zaaktype, ZAAKTYPE2)
        self.assertEqual(
            autorisatie_on.max_vertrouwelijkheidaanduiding,
            VertrouwelijkheidsAanduiding.openbaar,
        )

    def test_is_configured(self):
        configuration = AuthorizationConfigurationStep()

        with override_settings(AUTHORIZATIONS_CONFIG_FIXTURE_PATH=self.dump_path):
            self.assertFalse(configuration.is_configured())

            configuration.configure()

        # Modifying these attribute should not affect `is_configured`
        secret_oz, secret_on = JWTSecret.objects.all()

        secret_oz.secret = "modified-secret"
        secret_oz.save()
        secret_on.secret = "modified-secret"
        secret_on.save()

        applicatie_oz, applicatie_on = Applicatie.objects.all()
        applicatie_oz.label = "Open Zaak"
        applicatie_oz.save()
        applicatie_oz.label = "Open Notificaties"
        applicatie_oz.save()

        autorisatie_oz = applicatie_oz.autorisaties.first()
        autorisatie_on = applicatie_on.autorisaties.first()

        autorisatie_oz.zaaktype = ZAAKTYPE3
        autorisatie_oz.save()
        autorisatie_on.zaaktype = ZAAKTYPE4
        autorisatie_on.save()

        autorisatiespec_oz = applicatie_oz.autorisatie_specs.first()

        autorisatiespec_oz.max_vertrouwelijkheidaanduiding = (
            VertrouwelijkheidsAanduiding.openbaar
        )
        autorisatiespec_oz.save()

        with override_settings(AUTHORIZATIONS_CONFIG_FIXTURE_PATH=self.dump_path):
            self.assertTrue(configuration.is_configured())
