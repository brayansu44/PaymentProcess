# Generated by Django 4.1 on 2023-01-27 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_payment_comission_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='comission_value',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
