# Generated by Django 4.1 on 2023-01-27 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_alter_payment_comission_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='card_number',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='comission_value',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]