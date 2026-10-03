from unittest.mock import patch

from django.test import TestCase

from .views import (
    get_eligible_assembly_bundle_ids_for_processes,
    split_process_descriptions,
)


class AssemblyProcessSequenceTests(TestCase):
    def test_split_process_descriptions_trims_and_deduplicates(self):
        self.assertEqual(
            split_process_descriptions(
                " Shorts Side Pocket Attach, Shorts Pocket Dummy Stitch, Shorts Side Pocket Attach "
            ),
            ["Shorts Side Pocket Attach", "Shorts Pocket Dummy Stitch"],
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
