import json
from datetime import date, datetime
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import UnitListAPIView, get_shift, qc_hourly_signature


class GetShiftTests(SimpleTestCase):
    def test_get_shift_accepts_naive_datetime(self):
        naive_dt = datetime(2026, 7, 17, 9, 30, 0)

        self.assertEqual(get_shift(naive_dt), "I")


class QcHourlySignatureTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch("qcapp.views.qc_hourly_approval")
    def test_get_uses_today_when_date_missing(self, mock_model):
        mock_model.objects.filter.return_value.order_by.return_value = []

        request = self.factory.get("/qcapp/qc_hourly_signature/", {"unit": "U1"})
        response = qc_hourly_signature(request)

        self.assertEqual(response.status_code, 200)
        kwargs = mock_model.objects.filter.call_args.kwargs
        self.assertEqual(kwargs["date"], str(date.today()))

    @patch("qcapp.views.qc_hourly_approval")
    def test_post_defaults_hour_to_one_when_missing(self, mock_model):
        mock_model.objects.get_or_create.return_value = (mock_model(), False)
        mock_model.return_value.id = 1

        request = self.factory.post(
            "/qcapp/qc_hourly_signature/",
            data=json.dumps({"unit": 1, "line": 2, "role": "UNIT", "user": 10}),
            content_type="application/json",
        )
        response = qc_hourly_signature(request)

        self.assertEqual(response.status_code, 200)
        call_kwargs = mock_model.objects.get_or_create.call_args.kwargs
        self.assertEqual(call_kwargs["approval_hour"], 1)


class EmployeeAllocationUnitPermissionTests(SimpleTestCase):
    def test_units_are_limited_to_authenticated_users_employee_allocation_grants(self):
        request = APIRequestFactory().get(
            "/qcapp/api/units/",
            {"app": "employee_allocation"},
        )
        force_authenticate(
            request,
            user=type("AuthenticatedUser", (), {"pk": 42, "is_authenticated": True})(),
        )

        with (
            patch("qcapp.views.user_unit_permission.objects.filter") as permissions,
            patch("qcapp.views.Unit.objects.filter") as units,
            patch("qcapp.views.UnitSerializer") as serializer,
        ):
            permitted_unit_ids = [3, 5]
            permissions.return_value.values_list.return_value = permitted_unit_ids
            serializer.return_value.data = [{"id": 3}, {"id": 5}]

            response = UnitListAPIView.as_view()(request)

        self.assertEqual(response.data, [{"id": 3}, {"id": 5}])
        permissions.assert_called_once_with(user_id=42, app="employee_allocation")
        units.assert_called_once_with(id__in=permitted_unit_ids)
