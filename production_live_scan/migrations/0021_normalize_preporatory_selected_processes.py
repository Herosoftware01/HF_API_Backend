import json

from django.db import migrations


def normalize_selected_processes(apps, schema_editor):
    PreporatoryEntry = apps.get_model("production_live_scan", "PreporatoryEntry")
    database = schema_editor.connection.alias

    for entry in PreporatoryEntry.objects.using(database).all().iterator():
        value = entry.selected_processes
        if not value:
            continue

        try:
            parsed = json.loads(value)
        except (TypeError, json.JSONDecodeError):
            parsed = value

        if isinstance(parsed, list):
            normalized = next(
                (part for part in parsed if isinstance(part, str)),
                "",
            )
        else:
            normalized = value

        if normalized != value:
            PreporatoryEntry.objects.using(database).filter(pk=entry.pk).update(
                selected_processes=normalized,
            )


class Migration(migrations.Migration):
    dependencies = [
        ("production_live_scan", "0020_alter_preporatoryentry_selected_processes"),
    ]

    operations = [
        migrations.RunPython(
            normalize_selected_processes,
            migrations.RunPython.noop,
        ),
    ]
