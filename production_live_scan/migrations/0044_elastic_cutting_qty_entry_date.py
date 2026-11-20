from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production_live_scan', '0043_elastic_cutting_qty_elastic_cutting_qty_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elastic_cutting_qty',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
