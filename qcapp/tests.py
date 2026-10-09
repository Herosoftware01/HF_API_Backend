import json
from datetime import date, datetime
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import (
    EmployeeAPIView,
    UnitListAPIView,
    get_shift,
    latest_online_allocations_by_employee,
    qc_hourly_signature,
)


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


class LatestEmployeeAllocationTests(SimpleTestCase):
    def test_latest_offline_allocation_overrides_earlier_online_status(self):
        allocations = [
            type("Allocation", (), {"emp_code": "21617", "status": False})(),
            type("Allocation", (), {"emp_code": "21617", "status": True})(),
            type("Allocation", (), {"emp_code": "11111", "status": True})(),
        ]

        latest_online = latest_online_allocations_by_employee(allocations)

        self.assertEqual(set(latest_online), {"11111"})


class EmployeeAPIViewDatabaseRoutingTests(SimpleTestCase):
    def test_contractor_records_and_master_are_read_from_separate_databases(self):
        request = APIRequestFactory().get(
            "/qcapp/api/employees/",
            {"include_online": "true", "date": "2026-10-09"},
        )
        contractor = SimpleNamespace(
            code="1234",
            name="Contractor employee",
            con_id_id=56,
        )

        with (
            patch("qcapp.views.emp_allocate.objects.filter") as allocations,
            patch("qcapp.views.Empwisesal.objects.using") as staff_source,
            patch("qcapp.views.Cont_employee.objects.using") as contractor_source,
            patch("qcapp.views.MasContract.objects.using") as contract_source,
        ):
            allocations.return_value.select_related.return_value.order_by.return_value = []
            staff_source.return_value.filter.return_value.values.return_value = []

            contractor_queryset = contractor_source.return_value.all.return_value
            contractor_queryset.values_list.return_value.distinct.return_value = [56]
            contractor_queryset.__iter__.return_value = iter([contractor])
            contract_source.return_value.filter.return_value = [
                SimpleNamespace(contract_id=56, contract_des="Contract A")
            ]

            response = EmployeeAPIView.as_view()(request)

        contractor_source.assert_called_once_with("default")
        contract_source.assert_called_once_with("main")
        contract_source.return_value.filter.assert_called_once_with(
            contract_id__in=[56]
        )
        self.assertEqual(
            response.data,
            [
                {
                    "code": "1234",
                    "name": "Contractor employee (Contract A)",
                    "dept": "Contract A",
                    "photo": None,
                    "source": "contract_employee",
                    "online_allocation": None,
                }
            ],
        )
