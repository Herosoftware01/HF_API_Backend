import json
from contextlib import nullcontext
from datetime import datetime, timezone as datetime_timezone
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import RequestFactory, SimpleTestCase, TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .models import Elastic_cutting_qty as ElasticCuttingQtyModel
from .models import elastic_cons as ElasticConsModel
from .views import (
    UserUnitPermissionView,
    assembly_process_stock_available,
    assembly_dependencies_satisfied,
    bundle_process_pairs,
    get_already_assembled_bundle_ids,
    get_eligible_assembly_bundle_ids,
    get_eligible_assembly_bundle_ids_for_processes,
    get_assembly_dependency_statuses,
    get_bundle_last_process,
    GetUnitDataAPIView,
    delete_process_dependency,
    elastic_size_details,
    elastic_previous_cutting,
    save_elastic_delivery,
    SaveAssemblySelectionView,
    save_elastic_cons,
    save_elastic_cutting_entry,
    save_process_dependency,
    split_process_descriptions,
    verify_process_dependency,
)


class AssemblyProcessSequenceTests(SimpleTestCase):
    def test_stock_requires_dependencies_complete_and_current_process_pending(self):
        dependency = {"top shoulder attach"}

        self.assertTrue(assembly_process_stock_available(
            {"top shoulder attach"},
            "Top Neck Rib Attach",
            dependency,
            set(),
        ))
        self.assertFalse(assembly_process_stock_available(
            set(),
            "Top Neck Rib Attach",
            dependency,
            set(),
        ))
        self.assertFalse(assembly_process_stock_available(
            {"top shoulder attach", "top neck rib attach"},
            "Top Neck Rib Attach",
            dependency,
            set(),
        ))

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

    @patch("production_live_scan.views.get_eligible_assembly_bundle_ids")
    def test_unverified_process_is_skipped_while_verified_process_is_validated(
        self,
        get_eligible,
    ):
        get_eligible.side_effect = [
            (True, set(), None),
            (True, {"bundle-verified"}, None),
        ]

        result = get_eligible_assembly_bundle_ids_for_processes(
            "J7123A",
            "Process without verified dependency, Verified process",
            "Top",
        )

        self.assertEqual(result, (True, {"bundle-verified"}, None))

    @patch("production_live_scan.views.dependency.objects.filter")
    def test_process_without_dependency_does_not_raise_unverified_error(
        self,
        dependency_filter,
    ):
        dependency_filter.return_value.filter.return_value.order_by.return_value.first.return_value = None

        result = get_eligible_assembly_bundle_ids(
            "J7123A",
            "Process without dependency",
            "Top",
        )

        self.assertEqual(result, (True, set(), None))

    @patch("production_live_scan.views.dependency.objects.filter")
    def test_process_with_unverified_dependency_is_skipped(
        self,
        dependency_filter,
    ):
        dependency_filter.return_value.filter.return_value.order_by.return_value.first.return_value = (
            SimpleNamespace(verify=False)
        )

        result = get_eligible_assembly_bundle_ids(
            "J7123A",
            "Unverified process",
            "Top",
        )

        self.assertEqual(result, (True, set(), None))

    @patch("production_live_scan.views.dependency.objects.filter")
    def test_dependency_statuses_report_verified_and_unverified_processes(
        self,
        dependency_filter,
    ):
        dependency_filter.return_value.filter.return_value.order_by.return_value.first.side_effect = [
            SimpleNamespace(verify=True),
            SimpleNamespace(verify=False),
        ]

        statuses = get_assembly_dependency_statuses(
            "J7123A",
            "Verified process, Unverified process",
            "Top",
        )

        self.assertEqual(
            statuses,
            [
                {"process": "Verified process", "verified": True},
                {"process": "Unverified process", "verified": False},
            ],
        )


class AssemblyTransferFilteringTests(SimpleTestCase):
    def test_bundle_listing_includes_destination_transfer_bundles(self):
        request = APIRequestFactory().get(
            "/get_input_scan_bundles/",
            {
                "unit": "1",
                "line": "2",
                "job_no": "J7123A",
                "process_des": "Current process",
                "top_bottom": "Shorts",
            },
        )
        input_result = {
            "bundle_id": "input-bundle",
            "mbud": "input-mbud",
            "job_no": "J7123A",
            "color": "Black",
            "bdl_no": "1",
            "size": "M",
            "tb_name": "Shorts",
            "pc": "1",
            "entry_date": None,
        }
        transferred_result = {
            "bundle_id": "transferred-bundle",
            "mbud": "transfer-mbud",
            "job_no": "J7123A",
            "color": "Black",
            "bdl_no": "2",
            "size": "M",
            "tb_name": "Shorts",
            "pc": "1",
            "entry_date": None,
        }
        input_queryset = MagicMock()
        input_queryset.values.return_value = [input_result]
        transfer_queryset = MagicMock()
        transfer_queryset.values.return_value = [transferred_result]

        with (
            patch("production_live_scan.views.unit_input.objects.filter") as input_filter,
            patch(
                "production_live_scan.views.get_eligible_assembly_bundle_ids_for_processes",
                return_value=(True, None, None),
            ),
            patch(
                "production_live_scan.views.get_assembly_dependency_statuses",
                return_value=[{"process": "Current process", "verified": True}],
            ),
            patch("production_live_scan.views.get_transfer_unit_and_line", return_value=(11, 22)),
            patch(
                "production_live_scan.views.get_already_assembled_bundle_ids",
                return_value=set(),
            ),
            patch("production_live_scan.views.bundle_transfer.objects.filter") as transfer_filter,
        ):
            input_filter.return_value.order_by.return_value.filter.return_value.filter.return_value.exclude.return_value = (
                input_queryset
            )
            transfer_filter.return_value.filter.return_value.exclude.return_value = (
                transfer_queryset
            )
            response = GetUnitDataAPIView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        transfer_filter.assert_any_call(
            unit=11,
            line=22,
            job_no__iexact="J7123A",
        )
        self.assertEqual(
            [row['bundle_id'] for row in response.data['data']],
            ["input-bundle", "transferred-bundle"],
        )
        self.assertEqual(
            response.data["dependency_statuses"],
            [{"process": "Current process", "verified": True}],
        )

    @patch("production_live_scan.views.Assembly_data.objects.filter")
    @patch("production_live_scan.views.dependency.objects.filter")
    @patch("production_live_scan.views.bundle_transfer.objects.filter")
    @patch("production_live_scan.views.get_transfer_unit_and_line", return_value=(11, None))
    def test_transferred_sequence_is_used_for_dependency_eligibility(
        self,
        transfer_location,
        transfer_filter,
        dependency_filter,
        assembly_filter,
    ):
        process_dependency = SimpleNamespace(
            verify=True,
            and_or=True,
            or_only=False,
            data_entries=MagicMock(),
        )
        process_dependency.data_entries.values_list.return_value = [
            ("Previous process", True, False),
            ("Transferred process", False, True),
        ]
        dependency_filter.return_value.filter.return_value.order_by.return_value.first.return_value = (
            process_dependency
        )
        completed_query = MagicMock()
        assembly_filter.return_value = completed_query
        completed_query.filter.return_value.filter.return_value.values_list.return_value = [
            ("bundle-1", "Previous process")
        ]
        transfer_query = MagicMock()
        transfer_filter.return_value = transfer_query
        transfer_query.filter.return_value.filter.return_value.values_list.return_value = [
            ("bundle-1", "Transferred process")
        ]

        result = get_eligible_assembly_bundle_ids(
            "J7123A",
            "Current process",
            "Shorts",
            "1",
        )

        self.assertEqual(result, (True, {"bundle-1"}, None))
        assembly_filter.assert_called_once_with(
            job_no__iexact="J7123A",
            unit_transfer=False,
        )
        completed_query.filter.assert_any_call(unit="1")
        completed_query.filter.return_value.filter.assert_called_once_with(
            tb_name__iexact="Shorts"
        )
        transfer_filter.assert_called_once_with(job_no__iexact="J7123A")
        transfer_query.filter.assert_any_call(unit=11)

    @patch("production_live_scan.views.Assembly_data.objects.filter")
    @patch("production_live_scan.views.bundle_transfer.objects.filter")
    @patch("production_live_scan.views.get_transfer_unit_and_line", return_value=(11, None))
    def test_same_sequence_validation_reads_both_tables(
        self,
        transfer_location,
        transfer_filter,
        assembly_filter,
    ):
        assembly_rows = assembly_filter.return_value
        assembly_rows.filter.return_value.values_list.return_value = ["assembly-bundle"]
        transferred_rows = transfer_filter.return_value
        transferred_rows.filter.return_value.values_list.return_value = ["transfer-bundle"]

        bundle_ids = get_already_assembled_bundle_ids(
            "J7123A",
            "1",
            "Current process",
        )

        self.assertEqual(bundle_ids, {"assembly-bundle", "transfer-bundle"})
        assembly_filter.assert_called_once_with(
            job_no__iexact="J7123A",
            unit="1",
            unit_transfer=False,
        )
        transfer_filter.assert_called_once_with(
            job_no__iexact="J7123A",
            unit=11,
        )


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


class SaveAssemblySelectionTests(SimpleTestCase):
    def test_save_copies_selected_bundles_and_marks_only_unit_transfer(self):
        request = APIRequestFactory().post(
            "/api/assembly/save/",
            {
                "selected_ids": [12],
                "unit_id": 3,
                "line_id": 8,
            },
            format="json",
        )
        bundle = SimpleNamespace(
            id=12,
            job_no="J7123A",
            tb_id=4,
            tb_name="Shorts",
            machine="M-1",
            seq="Side seam",
            bundle_id="bundle-12",
            bdl_no="12",
            mbud="mbud",
            size="M",
            size_id=5,
            color="Black",
            pc="1",
            lot="lot-1",
            emp_id="EMP123",
        )
        bundles = MagicMock()
        bundles.count.return_value = 1
        bundles.__iter__.return_value = iter([bundle])
        transfer_time = datetime(2026, 10, 7, 10, 30, tzinfo=datetime_timezone.utc)

        with (
            patch("production_live_scan.views.Unit.objects.filter") as unit_filter,
            patch("production_live_scan.views.Line.objects.filter") as line_filter,
            patch(
                "production_live_scan.views.Assembly_data.objects.select_for_update"
            ) as select_for_update,
            patch("production_live_scan.views.Assembly_data.objects.filter") as assembly_filter,
            patch("production_live_scan.views.bundle_transfer.objects.bulk_create") as bulk_create,
            patch("production_live_scan.views.transaction.atomic", return_value=nullcontext()),
            patch("production_live_scan.views.timezone.now", return_value=transfer_time),
        ):
            unit_filter.return_value.exists.return_value = True
            line_filter.return_value.exists.return_value = True
            select_for_update.return_value.filter.return_value = bundles
            assembly_filter.return_value.update.return_value = 1

            response = SaveAssemblySelectionView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        transferred = bulk_create.call_args.args[0][0]
        self.assertEqual(transferred.unit, 3)
        self.assertEqual(transferred.line, 8)
        self.assertEqual(transferred.bundle_id, "bundle-12")
        self.assertEqual(transferred.date, transfer_time)
        self.assertEqual(transferred.entry_date, transfer_time)
        self.assertEqual(transferred.emp_id, "EMP123")
        assembly_filter.return_value.update.assert_called_once_with(unit_transfer=True)


class DependencyVerificationTests(SimpleTestCase):
    def test_verification_saves_logged_in_username_and_timestamp(self):
        verifier = SimpleNamespace(
            pk=42,
            username="line-supervisor",
            is_authenticated=True,
            get_username=lambda: "line-supervisor",
        )
        dependencies = MagicMock()
        dependencies.exists.return_value = True
        dependencies.update.return_value = 2
        verified_at = datetime(2026, 10, 6, tzinfo=datetime_timezone.utc)
        request = APIRequestFactory().post(
            "/verify_process_dependency/",
            data=json.dumps({
                "username": "admin",
                "password": "admin",
                "job_no": "J7123A",
                "tb_id": 3,
            }),
            content_type="application/json",
        )
        force_authenticate(request, user=verifier)

        with (
            patch(
                "production_live_scan.views.dependency.objects.select_for_update"
            ) as select_for_update,
            patch("production_live_scan.views.transaction.atomic", return_value=nullcontext()),
            patch("production_live_scan.views.timezone.now", return_value=verified_at),
        ):
            select_for_update.return_value.filter.return_value = dependencies
            response = verify_process_dependency(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)["verify_user"],
            "line-supervisor",
        )
        dependencies.update.assert_called_once_with(
            verify=True,
            verify_user="line-supervisor",
            verify_date=verified_at,
        )

    def test_verification_requires_admin_popup_credentials(self):
        verifier = SimpleNamespace(pk=17, is_authenticated=True)
        request = APIRequestFactory().post(
            "/verify_process_dependency/",
            data=json.dumps({
                "username": "operator",
                "password": "password",
                "job_no": "J7123A",
                "tb_id": 3,
            }),
            content_type="application/json",
        )
        force_authenticate(request, user=verifier)

        response = verify_process_dependency(request)

        self.assertEqual(response.status_code, 403)


class DependencyMutationPasswordTests(SimpleTestCase):
    def test_save_accepts_action_password(self):
        request = RequestFactory().post(
            "/save_process_dependency/",
            data=json.dumps({"password": "12345", "dependencies": []}),
            content_type="application/json",
        )
        existing_group = MagicMock()
        existing_group.filter.return_value.exists.return_value = False
        existing_group.exists.return_value = False

        with (
            patch(
                "production_live_scan.views.dependency.objects.select_for_update"
            ) as select_for_update,
            patch("production_live_scan.views.transaction.atomic", return_value=nullcontext()),
        ):
            select_for_update.return_value.filter.return_value = existing_group
            response = save_process_dependency(request)

        self.assertEqual(response.status_code, 201)

    def test_save_requires_action_password(self):
        request = RequestFactory().post(
            "/save_process_dependency/",
            data=json.dumps({"password": "wrong", "dependencies": []}),
            content_type="application/json",
        )

        with patch("production_live_scan.views.dependency.objects") as dependency_objects:
            response = save_process_dependency(request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)["error"], "Invalid password")
        dependency_objects.select_for_update.assert_not_called()

    def test_delete_accepts_action_password(self):
        request = RequestFactory().post(
            "/delete_process_dependency/",
            data=json.dumps({
                "password": "12345",
                "job_no": "J7123A",
                "tb_id": 3,
            }),
            content_type="application/json",
        )
        dependencies = MagicMock()
        dependencies.exists.return_value = True
        dependencies.delete.return_value = (1, {"production_live_scan.dependency": 1})

        with (
            patch(
                "production_live_scan.views.dependency.objects.select_for_update"
            ) as select_for_update,
            patch("production_live_scan.views.transaction.atomic", return_value=nullcontext()),
        ):
            select_for_update.return_value.filter.return_value = dependencies
            response = delete_process_dependency(request)

        self.assertEqual(response.status_code, 200)
        dependencies.delete.assert_called_once()

    def test_delete_requires_action_password(self):
        request = RequestFactory().post(
            "/delete_process_dependency/",
            data=json.dumps({
                "password": "",
                "job_no": "J7123A",
                "tb_id": 3,
            }),
            content_type="application/json",
        )

        with patch("production_live_scan.views.dependency.objects") as dependency_objects:
            response = delete_process_dependency(request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)["error"], "Invalid password")
        dependency_objects.select_for_update.assert_not_called()


class UserUnitPermissionTests(SimpleTestCase):
    def test_machine_transfer_permissions_are_saved(self):
        request = RequestFactory().post(
            "/user-unit-permission/",
            data=json.dumps({
                "user_id": 7,
                "app": "machine_transfer",
                "unit_ids": [1, 2],
            }),
            content_type="application/json",
        )

        with (
            patch("production_live_scan.views.User.objects.filter") as users,
            patch("production_live_scan.views.Unit.objects.filter") as units,
            patch(
                "production_live_scan.views.user_unit_permission.objects.filter"
            ) as existing_permissions,
            patch(
                "production_live_scan.views.user_unit_permission.objects.bulk_create"
            ) as bulk_create,
            patch("production_live_scan.views.transaction.atomic", return_value=nullcontext()),
        ):
            users.return_value.first.return_value = SimpleNamespace(id=7)
            units.return_value.values_list.return_value = [1, 2]

            response = UserUnitPermissionView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["app"], "machine_transfer")
        self.assertEqual(json.loads(response.content)["unit_ids"], [1, 2])
        self.assertTrue(all(
            permission.app == "machine_transfer"
            for permission in bulk_create.call_args.args[0]
        ))
        existing_permissions.assert_called_once_with(user_id=7, app="machine_transfer")


class ElasticConsumptionTests(SimpleTestCase):
    def test_size_details_prefers_saved_consumption(self):
        order_query = MagicMock()
        order_query.values.return_value.annotate.return_value.order_by.return_value = [
            {"siz": "M", "qty": 10}
        ]
        saved_query = MagicMock()
        saved_query.order_by.return_value.filter.return_value.first.return_value = (
            SimpleNamespace(cons=Decimal("3.25"))
        )
        cutting_query = MagicMock()
        cutting_query.order_by.return_value.first.return_value = None

        request = APIRequestFactory().get(
            "/elastic/sizes/",
            {
                "ordno": "ORD-1",
                "jobno": "ORD-1",
                "topbottom": "TOP",
                "colour": "BLACK",
            },
        )
        with (
            patch("production_live_scan.views.ViewOrdersummary") as orders,
            patch("production_live_scan.views.elastic_cons") as saved,
            patch("production_live_scan.views.ViewElasticCons") as source,
            patch("production_live_scan.views.ViewCuttingQtyDetails") as cutting,
        ):
            orders.objects.using.return_value.filter.return_value = order_query
            saved.objects.filter.return_value = saved_query
            cutting.objects.using.return_value.filter.return_value = cutting_query

            response = elastic_size_details(request)

        self.assertEqual(response.data[0]["len_cms"], "3.25")
        self.assertEqual(response.data[0]["cons_source"], "elastic_cons")
        source.objects.using.assert_not_called()

    def test_size_details_falls_back_to_view_when_no_saved_value(self):
        order_query = MagicMock()
        order_query.values.return_value.annotate.return_value.order_by.return_value = [
            {"siz": "M", "qty": 10}
        ]
        saved_query = MagicMock()
        saved_ordered_query = saved_query.order_by.return_value
        saved_ordered_query.filter.return_value.first.return_value = None
        saved_ordered_query.first.return_value = None
        source_query = MagicMock()
        source_query.order_by.return_value.first.return_value = (
            SimpleNamespace(cons=Decimal("2.50"))
        )
        cutting_query = MagicMock()
        cutting_query.order_by.return_value.first.return_value = None

        request = APIRequestFactory().get(
            "/elastic/sizes/",
            {"ordno": "ORD-1", "topbottom": "TOP", "colour": "BLACK"},
        )
        with (
            patch("production_live_scan.views.ViewOrdersummary") as orders,
            patch("production_live_scan.views.elastic_cons") as saved,
            patch("production_live_scan.views.ViewElasticCons") as source,
            patch("production_live_scan.views.ViewCuttingQtyDetails") as cutting,
        ):
            orders.objects.using.return_value.filter.return_value = order_query
            saved.objects.filter.return_value = saved_query
            source.objects.using.return_value.filter.return_value = source_query
            cutting.objects.using.return_value.filter.return_value = cutting_query

            response = elastic_size_details(request)

        self.assertEqual(response.data[0]["len_cms"], "2.50")
        self.assertEqual(response.data[0]["cons_source"], "view_elastic_cons")
        source.objects.using.assert_called_once_with("demo")

    def test_save_creates_values_for_unset_sizes(self):
        request = APIRequestFactory().post(
            "/elastic/cons/save/",
            {
                "jobno": "ORD-1",
                "topbottom": "TOP",
                "colour": "BLACK",
                "sizes": [
                    {"size": "M", "len_cms": "3.25"},
                    {"size": "L", "len_cms": "3.50"},
                ],
            },
            format="json",
        )
        with (
            patch("production_live_scan.views.elastic_cons") as saved,
            patch(
                "production_live_scan.views.transaction.atomic",
                return_value=nullcontext(),
            ),
        ):
            saved._meta = ElasticConsModel._meta
            matching_rows = saved.objects.filter.return_value
            matching_rows.exists.return_value = False

            response = save_elastic_cons(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["saved_count"], 2)
        self.assertEqual(response.data["saved_sizes"], ["M", "L"])
        self.assertEqual(saved.objects.create.call_count, 2)
        self.assertEqual(
            saved.objects.create.call_args_list[0].kwargs,
            {
                "jobno": "ORD-1",
                "sizedescr": "M",
                "cons": Decimal("3.25"),
                "topbott": "TOP",
                "color": "BLACK",
            },
        )

    def test_save_updates_existing_values(self):
        request = APIRequestFactory().post(
            "/elastic/cons/save/",
            {
                "jobno": "ORD-1",
                "topbottom": "TOP",
                "colour": "BLACK",
                "sizes": [{"size": "M", "len_cms": "3.25"}],
            },
            format="json",
        )
        with (
            patch("production_live_scan.views.elastic_cons") as saved,
            patch(
                "production_live_scan.views.transaction.atomic",
                return_value=nullcontext(),
            ),
        ):
            saved._meta = ElasticConsModel._meta
            saved.objects.filter.return_value.exists.return_value = True

            response = save_elastic_cons(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["saved_count"], 1)
        saved.objects.filter.return_value.update.assert_called_once_with(cons=Decimal("3.25"))
        saved.objects.create.assert_not_called()


class ElasticCuttingEntrySaveTests(SimpleTestCase):
    def setUp(self):
        self.payload = {
            "date": "2026-11-17",
            "order_no": "ORD-1",
            "topbottom": "TOP",
            "color": "BLACK",
            "elastic_description": "Waist Elastic",
            "inward_mtrs": "100",
            "actual_consumption": "0.20",
            "wastage": "0.13",
            "sizes": [{
                "size": "M",
                "len_cm": "3.25",
                "order_qty": "20",
                "pcs_cut": "15",
                "prev_cut_qty": "",
                "elastic_cutting_qty": "10",
                "bundles": [
                    {"bdl_no": 1, "bdl_qty": 4},
                    {"bdl_no": 2, "bdl_qty": 6},
                ],
            }, {
                "size": "L",
                "len_cm": "2",
                "order_qty": "15",
                "pcs_cut": "10",
                "prev_cut_qty": "",
                "elastic_cutting_qty": "",
                "bundles": [],
            }],
        }

    def test_saves_header_and_one_detail_per_bundle(self):
        request = APIRequestFactory().post(
            "/elastic/save/", self.payload, format="json"
        )
        with (
            patch("production_live_scan.views.Elastic_cutting_qty.objects.create") as header_create,
            patch("production_live_scan.views.Elastic_cutting_qty_details.objects.bulk_create") as details_create,
            patch("production_live_scan.views.transaction.atomic", return_value=nullcontext()),
        ):
            header_create.return_value = ElasticCuttingQtyModel(entry_no=42)
            response = save_elastic_cutting_entry(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["entry_no"], 42)
        self.assertEqual(header_create.call_args.kwargs["total_cutting_qty"], "10")
        self.assertEqual(header_create.call_args.kwargs["estimate_mtrs"], "0.33")
        saved_details = details_create.call_args.args[0]
        self.assertEqual(len(saved_details), 2)
        self.assertEqual(
            [(row.bdl_no, row.bdl_qty, row.elastic_cutting_qty) for row in saved_details],
            [("1", "4", "4"), ("2", "6", "6")],
        )

    def test_rejects_bundle_total_that_differs_from_current_cut_qty(self):
        self.payload["sizes"][0]["bundles"] = [{"bdl_no": 1, "bdl_qty": 9}]
        request = APIRequestFactory().post(
            "/elastic/save/", self.payload, format="json"
        )
        with (
            patch("production_live_scan.views.Elastic_cutting_qty.objects.create") as header_create,
            patch("production_live_scan.views.Elastic_cutting_qty_details.objects.bulk_create") as details_create,
        ):
            response = save_elastic_cutting_entry(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("must total 10 pcs", response.data["error"])
        header_create.assert_not_called()
        details_create.assert_not_called()

    def test_rejects_save_when_no_current_cut_qty_is_entered(self):
        self.payload["sizes"][0]["elastic_cutting_qty"] = ""
        self.payload["sizes"][0]["bundles"] = []
        request = APIRequestFactory().post(
            "/elastic/save/", self.payload, format="json"
        )
        with (
            patch("production_live_scan.views.Elastic_cutting_qty.objects.create") as header_create,
            patch("production_live_scan.views.Elastic_cutting_qty_details.objects.bulk_create") as details_create,
        ):
            response = save_elastic_cutting_entry(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Elastic Current Cut Qty", response.data["error"])
        header_create.assert_not_called()
        details_create.assert_not_called()

    def test_rejects_elastic_cut_qty_above_order_and_cut_limit(self):
        self.payload["sizes"][0]["elastic_cutting_qty"] = "21"
        self.payload["sizes"][0]["bundles"] = [{"bdl_no": 1, "bdl_qty": 21}]
        request = APIRequestFactory().post(
            "/elastic/save/", self.payload, format="json"
        )
        with patch("production_live_scan.views.Elastic_cutting_qty.objects.create") as header_create:
            response = save_elastic_cutting_entry(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("quantity limit", response.data["error"])
        header_create.assert_not_called()

    def test_rejects_actual_consumption_outside_estimate_tolerance(self):
        self.payload["actual_consumption"] = "10"
        self.payload["wastage"] = "0"
        request = APIRequestFactory().post(
            "/elastic/save/", self.payload, format="json"
        )
        with patch("production_live_scan.views.Elastic_cutting_qty.objects.create") as header_create:
            response = save_elastic_cutting_entry(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Actual Consumption must be between", response.data["error"])
        header_create.assert_not_called()

    def test_wastage_is_not_part_of_actual_consumption_tolerance(self):
        self.payload["actual_consumption"] = "0.33"
        self.payload["wastage"] = "100"
        request = APIRequestFactory().post(
            "/elastic/save/", self.payload, format="json"
        )
        with (
            patch("production_live_scan.views.Elastic_cutting_qty.objects.create") as header_create,
            patch("production_live_scan.views.Elastic_cutting_qty_details.objects.bulk_create"),
            patch("production_live_scan.views.transaction.atomic", return_value=nullcontext()),
        ):
            header_create.return_value = ElasticCuttingQtyModel(entry_no=43)
            response = save_elastic_cutting_entry(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(header_create.call_args.kwargs["wastage"], "100")


class ElasticDeliverySaveTests(SimpleTestCase):
    def test_saves_delivery_and_links_scanned_bundle_to_delivery_detail(self):
        request = APIRequestFactory().post(
            "/api/delivery/save/",
            {
                "job_no": "ORD-1",
                "topbottom": "TOP",
                "colour": "BLACK",
                "unit": "UNIT-1",
                "details": [{
                    "size": "M",
                    "unit_ord_qty": 20,
                    "unit_cut_qty": 15,
                    "cur_del_qty": 4,
                    "total_bdl": 1,
                    "bdl_ids": [101],
                }],
            },
            format="json",
        )
        bundle = SimpleNamespace(bdl_id=101, size="M", elastic_cutting_qty="4")
        with (
            patch("production_live_scan.views.ElasticDelivery") as delivery_model,
            patch("production_live_scan.views.ElasticDeliveryDetails") as detail_model,
            patch("production_live_scan.views.Elastic_cutting_qty_details") as bundle_model,
            patch("production_live_scan.views.transaction.atomic", return_value=nullcontext()),
        ):
            delivery_model.objects.create.return_value = SimpleNamespace(id=12)
            detail_model.objects.create.return_value = SimpleNamespace(id=34)
            locked_bundles = bundle_model.objects.select_for_update.return_value.filter.return_value
            locked_bundles.__iter__.return_value = iter([bundle])

            response = save_elastic_delivery(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["delivery_id"], 12)
        self.assertEqual(response.data["detail_ids"], [34])
        self.assertEqual(
            detail_model.objects.create.call_args.kwargs,
            {
                "delivery_id": delivery_model.objects.create.return_value,
                "unit_ord_qty": 20,
                "unit_cut_qty": 15,
                "size": "M",
                "cur_del_qty": 4,
                "total_bdl": 1,
            },
        )
        bundle_model.objects.filter.return_value.update.assert_called_once_with(
            delivery=True,
            delivery_id=34,
        )

    def test_rejects_bundle_that_does_not_match_delivery_size(self):
        request = APIRequestFactory().post(
            "/api/delivery/save/",
            {
                "job_no": "ORD-1",
                "topbottom": "TOP",
                "colour": "BLACK",
                "unit": "UNIT-1",
                "details": [{
                    "size": "M",
                    "unit_ord_qty": 20,
                    "unit_cut_qty": 15,
                    "cur_del_qty": 4,
                    "total_bdl": 1,
                    "bdl_ids": [101],
                }],
            },
            format="json",
        )
        bundle = SimpleNamespace(bdl_id=101, size="L", elastic_cutting_qty="4")
        with (
            patch("production_live_scan.views.ElasticDelivery.objects.create") as delivery_create,
            patch("production_live_scan.views.ElasticDeliveryDetails.objects.create") as detail_create,
            patch("production_live_scan.views.Elastic_cutting_qty_details") as bundle_model,
            patch("production_live_scan.views.transaction.atomic", return_value=nullcontext()),
        ):
            locked_bundles = bundle_model.objects.select_for_update.return_value.filter.return_value
            locked_bundles.__iter__.return_value = iter([bundle])

            response = save_elastic_delivery(request)

        self.assertEqual(response.status_code, 400)
        delivery_create.assert_not_called()
        detail_create.assert_not_called()


class ElasticPreviousCuttingTests(SimpleTestCase):
    def test_returns_zero_previous_values_when_no_history_exists(self):
        request = APIRequestFactory().get(
            "/elastic/previous/",
            {"order_no": "ORD-1", "topbottom": "TOP", "color": "BLACK"},
        )
        entries_query = MagicMock()
        entries_query.order_by.return_value = []
        with (
            patch("production_live_scan.views.Elastic_cutting_qty.objects.filter", return_value=entries_query),
            patch("production_live_scan.views.Elastic_cutting_qty_details.objects.filter") as details,
        ):
            response = elastic_previous_cutting(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "previous_cutting_mtrs": "0",
            "previous_wastage_mtrs": "0",
            "prev_cut_qty_by_size": {},
        })
        details.assert_not_called()

    def test_returns_prior_estimates_wastage_and_size_cut_totals(self):
        request = APIRequestFactory().get(
            "/elastic/previous/",
            {
                "order_no": "ORD-1",
                "topbottom": "TOP",
                "color": "BLACK",
                "elastic_description": "Waist Elastic",
            },
        )
        entries_query = MagicMock()
        entries_query.filter.return_value.order_by.return_value = [
            SimpleNamespace(entry_no=1, estimate_mtrs="1.25", wastage="0.10"),
            SimpleNamespace(entry_no=2, estimate_mtrs="0.75", wastage="0.05"),
        ]
        with (
            patch("production_live_scan.views.Elastic_cutting_qty.objects.filter", return_value=entries_query),
            patch("production_live_scan.views.Elastic_cutting_qty_details.objects.filter") as details,
        ):
            details.return_value.values_list.return_value = [
                ("M", "4"),
                ("M", "6"),
                ("L", "3"),
            ]
            response = elastic_previous_cutting(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["previous_cutting_mtrs"], "2")
        self.assertEqual(response.data["previous_wastage_mtrs"], "0.15")
        self.assertEqual(response.data["prev_cut_qty_by_size"], {"m": "10", "l": "3"})
