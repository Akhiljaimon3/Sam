# Generated by Django 5.0.7 on 2024-08-02 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_booking_history_bookdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concession_history',
            name='discount_amount',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='concession_history',
            name='discount_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
