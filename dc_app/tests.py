import json

from django.test import RequestFactory, SimpleTestCase
from django.urls import resolve

from .views import knitting_del_print


class KnittingDeliveryTests(SimpleTestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_knitting_routes_support_dropdown_and_selected_dc(self):
        """Routes must support both GET endpoints: list and detail."""
        list_route = resolve("/dcapp/knitting_del_print/")
        self.assertEqual(list_route.func, knitting_del_print)
        self.assertEqual(list_route.kwargs, {})
        
        detail_route = resolve("/dcapp/knitting_del_print/156/")
        self.assertEqual(detail_route.func, knitting_del_print)
        self.assertEqual(detail_route.kwargs, {"dcno": 156})

    def test_invalid_dcno_returns_400(self):
        """Invalid dcno (non-integer) must return 400 error."""
        response = knitting_del_print(
            self.request_factory.get("/dcapp/knitting_del_print/"),
            dcno="abc",
        )
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertFalse(response_data["status"])
        self.assertIn("integer", response_data["message"])
