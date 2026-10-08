from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production_live_scan', '0030_bundle_transfer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bundle_transfer',
            old_name='entry_mode',
            new_name='entry_date',
        ),
    ]
