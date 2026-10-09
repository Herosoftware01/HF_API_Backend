from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dc_app", "0012_role_permission_module_foreign_key"),
    ]

    operations = [
        migrations.CreateModel(
            name="ViewGenStockIssue",
            fields=[
                (
                    "qrdetails",
                    models.CharField(
                        blank=True,
                        db_column="QRDetails",
                        max_length=30,
                        null=True,
                    ),
                ),
                ("companyname", models.CharField(max_length=12)),
                (
                    "address1",
                    models.CharField(
                        blank=True,
                        db_column="Address1",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "address2",
                    models.CharField(
                        blank=True,
                        db_column="Address2",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "address3",
                    models.CharField(
                        blank=True,
                        db_column="Address3",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "place",
                    models.CharField(
                        blank=True,
                        max_length=66,
                        null=True,
                    ),
                ),
                (
                    "regno",
                    models.CharField(
                        blank=True,
                        db_column="RegNo",
                        max_length=20,
                        null=True,
                    ),
                ),
                ("ph", models.CharField(max_length=17)),
                ("to_dept", models.CharField(max_length=35)),
                (
                    "no",
                    models.IntegerField(
                        db_column="No",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date", models.DateTimeField(db_column="Date")),
                ("frm_dept", models.CharField(max_length=35)),
                ("itemgrp", models.CharField(max_length=35)),
                ("itemname", models.CharField(max_length=35)),
                (
                    "quantity",
                    models.DecimalField(
                        db_column="Quantity",
                        decimal_places=4,
                        max_digits=18,
                    ),
                ),
                (
                    "name",
                    models.CharField(db_column="Name", max_length=25),
                ),
                (
                    "altquantity",
                    models.DecimalField(
                        blank=True,
                        db_column="AltQuantity",
                        decimal_places=4,
                        max_digits=18,
                        null=True,
                    ),
                ),
                (
                    "altuom",
                    models.CharField(
                        blank=True,
                        max_length=25,
                        null=True,
                    ),
                ),
                (
                    "companyid",
                    models.SmallIntegerField(db_column="CompanyID"),
                ),
                ("year", models.SmallIntegerField(db_column="Year")),
            ],
            options={
                "db_table": "view_gen_stock_Issue",
                "managed": False,
            },
        ),
    ]
