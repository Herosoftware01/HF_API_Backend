from django.db import migrations


def create_table(apps, schema_editor):
    Model = apps.get_model("dc_app", "Dc_Verify_Incharge")

    table_name = Model._meta.db_table

    existing_tables = schema_editor.connection.introspection.table_names()

    if table_name not in existing_tables:
        schema_editor.create_model(Model)


def delete_table(apps, schema_editor):
    Model = apps.get_model("dc_app", "Dc_Verify_Incharge")

    table_name = Model._meta.db_table

    existing_tables = schema_editor.connection.introspection.table_names()

    if table_name in existing_tables:
        schema_editor.delete_model(Model)


class Migration(migrations.Migration):

    dependencies = [
        ("dc_app", "0005_alter_dc_verify_incharge_options"),
    ]

    operations = [
        migrations.RunPython(
            create_table,
            delete_table,
        ),
    ]