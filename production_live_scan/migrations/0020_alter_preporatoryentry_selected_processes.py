from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("production_live_scan", "0019_preporatoryentry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="preporatoryentry",
            name="selected_processes",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
