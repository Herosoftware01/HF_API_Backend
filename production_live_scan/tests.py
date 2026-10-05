from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .views import (
    assembly_dependencies_satisfied,
    bundle_process_pairs,
    get_eligible_assembly_bundle_ids_for_processes,
    get_bundle_last_process,
    split_process_descriptions,
)


class AssemblyProcessSequenceTests(TestCase):
    def test_and_dependency_and_one_or_dependency_are_both_required(self):
        and_dependencies = {"top 2nd shoulder attach"}
        or_dependencies = {
            "top 1st shoulder attach",
            "top neck piping attach",
        }

        self.assertTrue(assembly_dependencies_satisfied(
            {
                "top 2nd shoulder attach",
                "top neck piping attach",
            },
            and_dependencies,
            or_dependencies,
        ))
        self.assertTrue(assembly_dependencies_satisfied(
            {
                "top 2nd shoulder attach",
                "top 1st shoulder attach",
            },
            and_dependencies,
            or_dependencies,
        ))
        self.assertFalse(assembly_dependencies_satisfied(
            {"top neck piping attach"},
            and_dependencies,
            or_dependencies,
        ))
        self.assertFalse(assembly_dependencies_satisfied(
            {"top 2nd shoulder attach"},
            and_dependencies,
            or_dependencies,
        ))

    def test_split_process_descriptions_trims_and_deduplicates(self):
        self.assertEqual(
            split_process_descriptions(
                " Shorts Side Pocket Attach, Shorts Pocket Dummy Stitch, Shorts Side Pocket Attach "
            ),
            ["Shorts Side Pocket Attach", "Shorts Pocket Dummy Stitch"],
        )

    def test_bundle_process_pairs_create_separate_entries_per_sequence(self):
        bundles = ["bundle-1", "bundle-2"]

        self.assertEqual(
            bundle_process_pairs(
                bundles,
                "Shorts FrontRise Attach, Shorts Back Rise Attach",
            ),
            [
                ("bundle-1", "Shorts FrontRise Attach"),
                ("bundle-1", "Shorts Back Rise Attach"),
                ("bundle-2", "Shorts FrontRise Attach"),
                ("bundle-2", "Shorts Back Rise Attach"),
            ],
        )

    @patch("production_live_scan.views.get_eligible_assembly_bundle_ids")
    def test_eligible_bundles_are_combined_across_processes(self, get_eligible):
        get_eligible.side_effect = [
            (True, {"bundle-1"}, None),
            (True, {"bundle-2"}, None),
        ]

        result = get_eligible_assembly_bundle_ids_for_processes(
            "J7123A",
            "Shorts Side Pocket Attach, Shorts Pocket Dummy Stitch",
            "Shorts",
        )

        self.assertEqual(result, (True, {"bundle-1", "bundle-2"}, None))
        self.assertEqual(
            [call.args[1] for call in get_eligible.call_args_list],
            ["Shorts Side Pocket Attach", "Shorts Pocket Dummy Stitch"],
        )

    @patch("production_live_scan.views.get_eligible_assembly_bundle_ids")
    def test_unrestricted_process_includes_all_bundles(self, get_eligible):
        get_eligible.side_effect = [
            (True, {"bundle-1"}, None),
            (True, None, None),
        ]

        result = get_eligible_assembly_bundle_ids_for_processes(
            "J7123A",
            "Shorts Side Pocket Attach, Shorts Pocket Dummy Stitch",
            "Shorts",
        )

        self.assertEqual(result, (True, None, None))


class BundleLastProcessTests(TestCase):
    @patch("production_live_scan.views.Assembly_data.objects.filter")
    def test_returns_latest_saved_process(self, filter_bundles):
        filter_bundles.return_value.order_by.return_value.values.return_value.first.return_value = {
            "seq": "Shorts FrontRise Attach",
            "job_no": "J7123A",
            "tb_name": "Shorts",
        }
        request = APIRequestFactory().get(
            "/bundle-last-process/",
            {"bundle_id": "1~99683~"},
        )

        response = get_bundle_last_process(request)

        self.assertEqual(
            response.data,
            {
                "available": True,
                "last_process": "Shorts FrontRise Attach",
                "job_no": "J7123A",
                "top_bottom": "Shorts",
            },
        )
        filter_bundles.assert_called_once_with(bundle_id__iexact="1~99683~")

    @patch("production_live_scan.views.Assembly_data.objects.filter")
    def test_returns_unavailable_when_no_saved_process_exists(self, filter_bundles):
        filter_bundles.return_value.order_by.return_value.values.return_value.first.return_value = None
        request = APIRequestFactory().get(
            "/bundle-last-process/",
            {"bundle_id": "1~99683~"},
        )

        response = get_bundle_last_process(request)

        self.assertEqual(
            response.data,
            {"available": False, "message": "Bundle not available"},
        )
