from django.test import override_settings, tag
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.constants import ComponentTypes
from vng_api_common.tests import reverse

from openzaak.accounts.tests.factories import UserFactory
from openzaak.components.documenten.api.scopes import SCOPE_DOCUMENTEN_AANMAKEN
from openzaak.tests.utils import JWTAuthMixin
from openzaak.import_data.models import ImportStatusChoices, ImportTypeChoices
from openzaak.import_data.tests.factories import ImportFactory


@tag("documenten-import-status")
class ImportDocumentenStatustTests(JWTAuthMixin, APITestCase):

    def test_active_import(self):
        import_instance = ImportFactory.create(
            import_type=ImportTypeChoices.documents,
            status=ImportStatusChoices.active,
            total=500000,
            processed=250000,
            processed_successfully=125000,
            processed_invalid=125000,
        )

        url = reverse(
            "documenten-import:status", kwargs=dict(uuid=import_instance.uuid)
        )

        user = UserFactory.create(is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "total": 500000,
                "processed": 250000,
                "processedSuccessfully": 125000,
                "processedInvalid": 125000,
                "status": ImportStatusChoices.active.label,
            },
        )

    def test_error_import(self):
        import_instance = ImportFactory.create(
            import_type=ImportTypeChoices.documents,
            status=ImportStatusChoices.error,
            total=500000,
            processed=100000,
            processed_successfully=50000,
            processed_invalid=50000,
        )

        url = reverse(
            "documenten-import:status", kwargs=dict(uuid=import_instance.uuid)
        )

        user = UserFactory.create(is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "total": 500000,
                "processed": 100000,
                "processedSuccessfully": 50000,
                "processedInvalid": 50000,
                "status": ImportStatusChoices.error.label,
            },
        )

    def test_finished_import(self):
        import_instance = ImportFactory.create(
            import_type=ImportTypeChoices.documents,
            status=ImportStatusChoices.finished,
            total=500000,
            processed=250000,
            processed_successfully=125000,
            processed_invalid=125000,
        )

        url = reverse(
            "documenten-import:status", kwargs=dict(uuid=import_instance.uuid)
        )

        user = UserFactory.create(is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "total": 500000,
                "processed": 250000,
                "processedSuccessfully": 125000,
                "processedInvalid": 125000,
                "status": ImportStatusChoices.finished.label,
            },
        )

    def test_pending_import(self):
        import_instance = ImportFactory.create(
            import_type=ImportTypeChoices.documents,
            status=ImportStatusChoices.pending,
            total=500000,
            processed=0,
            processed_successfully=0,
            processed_invalid=0,
        )

        url = reverse(
            "documenten-import:status", kwargs=dict(uuid=import_instance.uuid)
        )

        user = UserFactory.create(is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "total": 500000,
                "processed": 0,
                "processedSuccessfully": 0,
                "processedInvalid": 0,
                "status": ImportStatusChoices.pending.label,
            },
        )

    def test_mismatching_import_type(self):
        import_instance = ImportFactory.create(
            import_type="foobar",
            status=ImportStatusChoices.active,
            total=500000,
            processed=250000,
            processed_successfully=125000,
            processed_invalid=125000,
        )

        url = reverse(
            "documenten-import:status", kwargs=dict(uuid=import_instance.uuid)
        )

        user = UserFactory.create(is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_regular_user(self):
        import_instance = ImportFactory.create(
            import_type=ImportTypeChoices.documents,
            status=ImportStatusChoices.active,
            total=500000,
            processed=250000,
            processed_successfully=125000,
            processed_invalid=125000,
        )

        url = reverse(
            "documenten-import:status", kwargs=dict(uuid=import_instance.uuid)
        )

        user = UserFactory.create(is_staff=False, is_superuser=False)
        self.client.force_authenticate(user=user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response_data = response.json()

        self.assertEqual(response_data["code"], "permission_denied")

    def test_admin_user(self):
        import_instance = ImportFactory.create(
            import_type=ImportTypeChoices.documents,
            status=ImportStatusChoices.active,
            total=500000,
            processed=250000,
            processed_successfully=125000,
            processed_invalid=125000,
        )

        url = reverse(
            "documenten-import:status", kwargs=dict(uuid=import_instance.uuid)
        )

        user = UserFactory.create(is_staff=True, is_superuser=False)
        self.client.force_authenticate(user=user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response_data = response.json()

        self.assertEqual(response_data["code"], "permission_denied")

    @override_settings(CMIS_ENABLED=True)
    def test_cmis_enabled(self):
        import_instance = ImportFactory.create(
            import_type=ImportTypeChoices.documents,
            status=ImportStatusChoices.active,
            total=500000,
            processed=250000,
            processed_successfully=125000,
            processed_invalid=125000,
        )

        url = reverse(
            "documenten-import:status", kwargs=dict(uuid=import_instance.uuid)
        )

        user = UserFactory.create(is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()

        self.assertEqual(response_data["code"], _("CMIS not supported"))
