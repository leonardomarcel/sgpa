# Generated by Django 2.2.2 on 2020-03-23 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passagem', '0003_auto_20200320_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='remarcacaopassagem',
            name='data_remarcacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
