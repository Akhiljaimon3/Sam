# Generated by Django 5.0.7 on 2024-08-05 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_alter_concession_history_discount_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='concession_discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(max_length=50)),
                ('discount_name', models.CharField(blank=True, max_length=50, null=True)),
                ('discount_amount', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='concession_history',
            name='discount_amount',
        ),
        migrations.RemoveField(
            model_name='concession_history',
            name='discount_name',
        ),
    ]
