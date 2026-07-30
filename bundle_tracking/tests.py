from django.test import SimpleTestCase
from django.urls import resolve
from unittest.mock import MagicMock, patch

from .views import resolve_unit_code, sub_bundle_report


class ResolveUnitCodeTests(SimpleTestCase):
    def test_accepts_numeric_unit_code(self):
        self.assertEqual(resolve_unit_code("12"), 12)

    def test_accepts_unit_name_and_resolves_to_code(self):
        unit_lookup = lambda name: {"UNIT-1": 1}.get(name.upper())
        self.assertEqual(resolve_unit_code("UNIT-1", unit_lookup=unit_lookup), 1)

    def test_rejects_unknown_unit_value(self):
        with self.assertRaises(ValueError):
            resolve_unit_code("UNKNOWN")


class BundleTrackingUrlTests(SimpleTestCase):
    def test_sub_bundle_report_accepts_unit_name(self):
        match = resolve("/bundle_tracking/sub_bundle_report/UNIT-1/")
        self.assertEqual(match.url_name, "sub_bundle_report")
        self.assertEqual(match.kwargs["unit_id"], "UNIT-1")

    @patch("bundle_tracking.views.MasUnit")
    @patch("bundle_tracking.views.Bundlereport")
    def test_sub_bundle_report_uses_numeric_unitcode_for_unit_name(self, bundle_report, mas_unit):
        bundle_report.objects.using.return_value.filter.return_value.order_by.return_value = []
        mas_unit.objects.using.return_value.filter.return_value.first.return_value = None

        response = sub_bundle_report(MagicMock(), "UNIT-1")

        self.assertEqual(response.status_code, 200)
