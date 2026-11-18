
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production_live_scan', '0041_alter_elastic_cons_options'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                    CREATE TABLE [dbo].[elastic_cons] (
                        [id] BIGINT IDENTITY(1,1) NOT NULL PRIMARY KEY,
                        [jobno] NVARCHAR(50) NOT NULL,
                        [sizedescr] NVARCHAR(50) NOT NULL,
                        [cons] DECIMAL(18,2) NOT NULL,
                        [topbott] NVARCHAR(50) NOT NULL,
                        [color] NVARCHAR(1800) NULL
                    );
                    """,
                    reverse_sql="DROP TABLE [dbo].[elastic_cons];",
                ),
            ],
            state_operations=[],
        ),
    ]
