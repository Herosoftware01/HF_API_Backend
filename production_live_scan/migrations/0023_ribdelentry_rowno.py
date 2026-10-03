from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("production_live_scan", "0022_viewribdelpreparatory_ribdelentry"),
    ]

    operations = [
        migrations.AddField(
            model_name="ribdelentry",
            name="rowno",
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
