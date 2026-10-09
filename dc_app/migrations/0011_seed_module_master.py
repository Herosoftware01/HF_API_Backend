from django.db import migrations, models


MODULES = [
    (
        "cut_to_unit",
        "Cut to Unit Delivery",
        "/dc_print/cut_to_unit_delivery",
    ),
    (
        "cutting_sec_fabric",
        "Cutting Section Fabric",
        "/dc_print/cutting_sec_fabric",
    ),
    (
        "knitting_delivery",
        "Knitting Delivery",
        "/dc_print/knitting_delivery",
    ),
    (
        "bit_delivery",
        "Bit Delivery Challan",
        "/dc_print/bitdel_print",
    ),
    (
        "yarn_process",
        "Yarn Process Challan",
        "/dc_print/yarnprocess_del",
    ),
    (
        "acc_production",
        "Accessory Production",
        "/dc_print/acc_prod_delivery",
    ),
    (
        "acc_process",
        "Accessory Process",
        "/dc_print/acc_proc_delivery",
    ),
    (
        "acc_inhouse",
        "Accessory Inhouse Delivery",
        "/dc_print/acc_inhouse_delivery",
    ),
    (
        "fabric_process",
        "Fabric Process Delivery",
        "/dc_print/fabric_process_del",
    ),
    (
        "mistake_cut",
        "Mistake Cut Delivery",
        "/dc_print/mistake_cut_del",
    ),
    (
        "rib_cut",
        "Rib Cut Delivery",
        "/dc_print/rib_cut_del",
    ),
    (
        "godown_fabric",
        "Godown Fabric Delivery",
        "/dc_print/godown_fabric_del",
    ),
    (
        "replacement_del",
        "Replacement Delivery",
        "/dc_print/rep_del",
    ),
    (
        "unit_pcs",
        "Unit Pcs Delivery",
        "/dc_print/unit_pc_del",
    ),
    (
        "general_transaction_delivery",
        "General Delivery Type 1",
        "/dc_print/general_del",
    ),
    (
        "general_stock_issue",
        "General Stock Issue",
        "/dc_print/general_store",
    ),
]

LEGACY_IDS = {
    "general": "general_transaction_delivery",
    "general_delivery": "general_transaction_delivery",
    "general_delivery_type1": "general_transaction_delivery",
}


def seed_modules(apps, schema_editor):
    ModuleMaster = apps.get_model("dc_app", "ModuleMaster")
    Permission = apps.get_model("dc_app", "RoleModulePermission")

    database = schema_editor.connection.alias
    modules = ModuleMaster.objects.using(database)
    permissions = Permission.objects.using(database)

    module_names = {
        module_id: module_name
        for module_id, module_name, path in MODULES
    }

    for order, (module_id, module_name, path) in enumerate(
        MODULES,
        start=1,
    ):
        modules.update_or_create(
            module_id=module_id,
            defaults={
                "module_name": module_name,
                "description": "",
                "path": path,
                "display_order": order,
                "is_active": True,
            },
        )

    # Normalize legacy permission IDs.
    for legacy_id, canonical_id in LEGACY_IDS.items():
        legacy_rows = list(
            permissions.filter(module_id=legacy_id)
        )

        for legacy_row in legacy_rows:
            canonical_row = permissions.filter(
                role=legacy_row.role,
                module_id=canonical_id,
            ).first()

            if canonical_row:
                canonical_row.is_enabled = (
                    canonical_row.is_enabled
                    or legacy_row.is_enabled
                )
                canonical_row.module_name = module_names[canonical_id]
                canonical_row.save(
                    update_fields=(
                        "is_enabled",
                        "module_name",
                        "updated_at",
                    )
                )
                legacy_row.delete()
            else:
                legacy_row.module_id = canonical_id
                legacy_row.module_name = module_names[canonical_id]
                legacy_row.save(
                    update_fields=(
                        "module_id",
                        "module_name",
                        "updated_at",
                    )
                )

    # Correct stale names such as "General Stock Ddelivery".
    for module_id, module_name, path in MODULES:
        permissions.filter(module_id=module_id).update(
            module_name=module_name
        )

    # Preserve unexpected historical IDs as inactive master modules.
    historical_rows = permissions.values(
        "module_id",
        "module_name",
    ).distinct()

    next_order = len(MODULES) + 1000

    for row in historical_rows:
        module_id = row["module_id"]

        if not module_id:
            raise RuntimeError(
                "Blank module_id found in role_module_permissions"
            )

        if modules.filter(module_id=module_id).exists():
            continue

        modules.create(
            module_id=module_id,
            module_name=row["module_name"] or module_id,
            description="Imported from historical permission data.",
            path="",
            display_order=next_order,
            is_active=False,
        )
        next_order += 1


class Migration(migrations.Migration):
    dependencies = [
        ("dc_app", "0010_merge_20261007_1619"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModuleMaster",
            fields=[
                (
                    "module_id",
                    models.CharField(
                        max_length=100,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("module_name", models.CharField(max_length=255)),
                (
                    "description",
                    models.TextField(blank=True, default=""),
                ),
                (
                    "path",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                    ),
                ),
                ("display_order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "dc_module_master",
                "ordering": ("display_order", "module_name"),
                "indexes": [
                    models.Index(
                        fields=["is_active", "display_order"],
                        name="module_active_order_idx",
                    )
                ],
            },
        ),
        migrations.RunPython(
            seed_modules,
            migrations.RunPython.noop,
        ),
    ]
