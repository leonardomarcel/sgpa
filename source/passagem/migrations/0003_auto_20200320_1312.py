# Generated by Django 2.2.2 on 2020-03-20 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('passagem', '0002_remarcacaopassagem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remarcacaopassagem',
            name='passagem',
        ),
        migrations.AddField(
            model_name='remarcacaopassagem',
            name='num_bilhete',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='remarcacaopassagem',
            name='num_voo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='remarcacaopassagem',
            name='passageiro_passagem',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='passagem.PassageiroPassagem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='remarcacaopassagem',
            name='taxa_servico',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='remarcacaopassagem',
            name='valor_embarque',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]