import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import RequestFactory, SimpleTestCase

from .views import trs_workentry


class WorkentryUpdateTests(SimpleTestCase):
    def test_post_to_record_url_updates_and_returns_success(self):
        workentry = SimpleNamespace(
            id=169,
            username="Nandha Gopal",
            project="Project",
            category="Category",
            subcat="Subcategory",
            task_id_id=None,
            description="Old description",
            endstatus=None,
            status=False,
            startdatetime=None,
            enddatetime=None,
            entrydate=None,
            duration=None,
            durationminutes=None,
            image=None,
            save=Mock(),
        )
        request = RequestFactory().post(
            "/software_cost/trs_workentry/169/",
            data=json.dumps({
                "description": "Updated description",
                "status": "true",
            }),
            content_type="application/json",
        )

        with patch("software_cost.views.Workentry.objects.get", return_value=workentry):
            response = trs_workentry(request, id=169)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "status": True,
                "message": "Record updated successfully",
                "id": 169,
            },
        )
        self.assertEqual(workentry.description, "Updated description")
        self.assertTrue(workentry.status)
        workentry.save.assert_called_once_with()
