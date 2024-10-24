# Generated by Django 2.2.2 on 2020-03-16 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import passagem.model.anexo_processo_solicitacao_passagem
import passagem.model.solicitacao_passagem
import util.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basico', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aeroporto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome do Aeroporto')),
                ('iata', models.CharField(blank=True, max_length=5, null=True, verbose_name='Código IATA')),
                ('icao', models.CharField(blank=True, max_length=5, null=True, verbose_name='Código ICAO')),
                ('site', models.CharField(blank=True, max_length=255, null=True, verbose_name='Página Web')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=16, null=True, verbose_name='Latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=16, null=True, verbose_name='Latitude')),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basico.Municipio')),
            ],
            options={
                'verbose_name': 'Aeroporto',
                'verbose_name_plural': 'Aeroportos',
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Agencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cnpj', models.CharField(max_length=18)),
                ('inscricao_estadual', models.CharField(max_length=100)),
                ('nome_fantasia', models.CharField(max_length=100)),
                ('contrato', models.CharField(max_length=100)),
                ('fone', models.CharField(max_length=15)),
                ('fax', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('homepage', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='AnexoProcessoSolicitacaoPassagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(blank=True, null=True, upload_to=passagem.model.anexo_processo_solicitacao_passagem.anexo_processo)),
                ('nome', util.fields.CharUpperField(blank=True, max_length=200, null=True, verbose_name='Nome')),
                ('tamanho', util.fields.CharUpperField(blank=True, max_length=200, null=True, verbose_name='Tamanho')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Companhia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('iata', models.CharField(max_length=5)),
                ('icao', models.CharField(blank=True, max_length=5, null=True)),
                ('fone1', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone')),
                ('fone', models.CharField(blank=True, max_length=15, null=True)),
                ('fax', models.CharField(blank=True, max_length=13, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('tipo', models.CharField(blank=True, max_length=30, null=True)),
                ('site', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Motivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Passageiro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', util.fields.CharUpperField(max_length=100, verbose_name='Nome')),
                ('cpf', models.CharField(max_length=14, unique=True, verbose_name='CPF')),
                ('data_nascimento', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Passageiro',
                'verbose_name_plural': 'Passageiros',
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='PassageiroPassagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_bilhete', models.CharField(blank=True, max_length=50, null=True)),
                ('num_voo', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(choices=[('AG', 'AGUARDANDO AUTORIZACAO'), ('AUT', 'AUTORIZADA'), ('C', 'COMPRADA')], max_length=100)),
                ('tarifa', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('valor', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('valor_embarque', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('taxa_servico', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('companhia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passagem.Companhia')),
                ('passageiro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passagem.Passageiro')),
            ],
            options={
                'verbose_name': 'passageiro_passagem',
                'verbose_name_plural': 'passageiro_passagem',
            },
        ),
        migrations.CreateModel(
            name='Passagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_viagem', models.DateTimeField()),
                ('tipo', models.CharField(choices=[('I', 'IDA'), ('V', 'VOLTA')], max_length=100)),
                ('urgente', models.BooleanField(blank=True, default=False, null=True)),
                ('justificativa_urgencia', models.TextField(blank=True, null=True, verbose_name='Justificativa da Urgência')),
                ('agencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passagem.Agencia')),
                ('passageiros', models.ManyToManyField(blank=True, null=True, through='passagem.PassageiroPassagem', to='passagem.Passageiro')),
            ],
            options={
                'verbose_name': 'Passagem',
                'verbose_name_plural': 'Passagens',
                'ordering': ('data_viagem',),
            },
        ),
        migrations.CreateModel(
            name='SolicitacaoPassagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=10, null=True)),
                ('cadastro_concluido', models.BooleanField(default=False)),
                ('data', models.DateField(blank=True, null=True)),
                ('viagem_servico', models.CharField(choices=[('S', 'SIM'), ('N', 'NÃO')], max_length=100)),
                ('descricao_evento', models.TextField(blank=True, null=True, verbose_name='Descrição do Evento')),
                ('anexo_evento', models.FileField(blank=True, null=True, upload_to=passagem.model.solicitacao_passagem.anexo_evento)),
                ('anexo_diario', models.FileField(blank=True, null=True, upload_to=passagem.model.solicitacao_passagem.anexo_diario)),
                ('nota_empenho', models.FileField(blank=True, null=True, upload_to='')),
                ('fonte_recurso', models.TextField(blank=True, null=True)),
                ('unidade_gestora', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('ABERTA', 'ABERTA'), ('COM PENDENCIA', 'COM PENDENCIA'), ('AUTORIZADA', 'AUTORIZADA')], max_length=100)),
                ('anexos_processo', models.ManyToManyField(blank=True, null=True, to='passagem.AnexoProcessoSolicitacaoPassagem')),
                ('motivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passagem.Motivo')),
                ('orgao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basico.Orgao')),
                ('passagens', models.ManyToManyField(to='passagem.Passagem')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trecho',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
                ('passagens', models.ManyToManyField(to='passagem.Passagem')),
                ('solicitacao_passagem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passagem.SolicitacaoPassagem')),
            ],
            options={
                'verbose_name': 'Trecho',
                'verbose_name_plural': 'Techos',
            },
        ),
        migrations.CreateModel(
            name='Rota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rota_destino', to='passagem.Aeroporto')),
                ('origem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rota_origem', to='passagem.Aeroporto')),
            ],
            options={
                'verbose_name': 'Rota',
                'verbose_name_plural': 'Rotas',
            },
        ),
        migrations.AddField(
            model_name='passagem',
            name='rota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passagem.Rota'),
        ),
        migrations.AddField(
            model_name='passageiropassagem',
            name='passagem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passagem.Passagem'),
        ),
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('solicitacao_passagem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passagem.SolicitacaoPassagem')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cotacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_voo', models.CharField(max_length=20, verbose_name='Número do Voo')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='Valor da passagem')),
                ('data', models.DateTimeField(verbose_name='Data da IDA')),
                ('companhia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companhia_ida', to='passagem.Companhia')),
                ('passagem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passagem.Passagem')),
            ],
        ),
        migrations.CreateModel(
            name='Autorizacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('observacao', models.TextField(blank=True, null=True, verbose_name='Observação')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AcompanhamentoSolicitacaoPassagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(blank=True, null=True)),
                ('descricao', models.TextField(verbose_name='Descrição do Evento')),
                ('status', models.CharField(choices=[('COM PENDENCIA', 'COM PENDENCIA'), ('AUTORIZADA', 'AUTORIZADA')], max_length=40)),
                ('solicitacao_passagem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passagem.SolicitacaoPassagem')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('exercicio', models.CharField(choices=[('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023')], max_length=4)),
                ('inicio', models.DateField(verbose_name='Inicio')),
                ('termino', models.DateField(verbose_name='Termino')),
                ('orgao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basico.Orgao')),
                ('usuario_criacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cota',
                'verbose_name_plural': 'Cotas',
                'unique_together': {('orgao', 'exercicio')},
            },
        ),
    ]
