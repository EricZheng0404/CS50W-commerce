# Generated by Django 4.1.1 on 2022-10-12 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_alter_listing_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="listing",
            name="category",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="listing",
            name="image",
            field=models.ImageField(upload_to="auctions/files/images"),
        ),
    ]
