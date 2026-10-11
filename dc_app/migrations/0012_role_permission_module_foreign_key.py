import django.db.models.deletion
from django.db import migrations, models


def restore_module_names(apps, schema_editor):
    ModuleMaster = apps.get_model("dc_app", "ModuleMaster")
    Permission = apps.get_model("dc_app", "RoleModulePermission")

    database = schema_editor.connection.alias
    permissions = Permission.objects.using(database)

    for module in ModuleMaster.objects.using(database).all().iterator():
        permissions.filter(module_id=module.module_id).update(
            module_name=module.module_name
        )


class Migration(migrations.Migration):
    dependencies = [
        ("dc_app", "0011_seed_module_master"),
    ]

    operations = [
        # This temporary nullable state lets the reverse data migration restore
        # names before the original NOT NULL constraint is reinstated.
        migrations.AlterField(
            model_name="rolemodulepermission",
            name="module_name",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterUniqueTogether(
            name="rolemodulepermission",
            unique_together=set(),
        ),
        # Pin the current database column name before changing only Django's
        # field name. Existing per-row module IDs remain untouched.
        migrations.AlterField(
            model_name="rolemodulepermission",
            name="module_id",
            field=models.CharField(
                db_column="module_id",
                max_length=100,
            ),
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RenameField(
                    model_name="rolemodulepermission",
                    old_name="module_id",
                    new_name="module",
                ),
            ],
        ),
        migrations.AlterField(
            model_name="rolemodulepermission",
            name="module",
            field=models.ForeignKey(
                db_column="module_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="role_permissions",
                to="dc_app.modulemaster",
            ),
        ),
        migrations.RunPython(
            migrations.RunPython.noop,
            restore_module_names,
        ),
        migrations.RemoveField(
            model_name="rolemodulepermission",
            name="module_name",
        ),
        migrations.AddConstraint(
            model_name="rolemodulepermission",
            constraint=models.UniqueConstraint(
                fields=("role", "module"),
                name="unique_role_module_permission",
            ),
        ),
    ]
