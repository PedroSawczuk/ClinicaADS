# Generated by Django 5.0.2 on 2024-03-06 23:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ambulatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
                ('numleitos', models.IntegerField(blank=True, null=True)),
                ('andar', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Ambulatório',
                'verbose_name_plural': 'Ambulatórios',
                'db_table': 'ambulatorio',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('crm', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
                ('especialidade', models.CharField(blank=True, max_length=100, null=True)),
                ('endereco', models.CharField(blank=True, max_length=250, null=True)),
                ('telefone', models.CharField(blank=True, max_length=15, null=True)),
                ('idade', models.IntegerField(blank=True, null=True)),
                ('salario', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
            options={
                'verbose_name': 'Médico',
                'verbose_name_plural': 'Médicos',
                'db_table': 'medico',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(blank=True, null=True)),
                ('horario', models.TimeField(blank=True, null=True)),
                ('porcent', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'verbose_name': 'Consulta',
                'verbose_name_plural': 'Consultas',
                'db_table': 'consulta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Convenio',
            fields=[
                ('codconv', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Convênio',
                'verbose_name_plural': 'Convênios',
                'db_table': 'convenio',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('endereco', models.CharField(blank=True, max_length=250, null=True)),
                ('telefone', models.CharField(blank=True, max_length=15, null=True)),
                ('cidade', models.CharField(blank=True, max_length=100, null=True)),
                ('idade', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
                'db_table': 'paciente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Atende',
            fields=[
                ('medico', models.ForeignKey(db_column='medico', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.medico')),
            ],
            options={
                'verbose_name': 'Médico Convênio',
                'verbose_name_plural': 'Médico Convênios',
                'db_table': 'atende',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Possui',
            fields=[
                ('paciente', models.OneToOneField(db_column='paciente', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.paciente')),
                ('tipo', models.CharField(blank=True, max_length=1, null=True)),
                ('vencimento', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Paciente x Convênio',
                'verbose_name_plural': 'Paciente x Convênios',
                'db_table': 'possui',
                'managed': False,
            },
        ),
    ]
