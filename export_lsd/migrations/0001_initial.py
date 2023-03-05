# Generated by Django 4.1.1 on 2022-11-16 06:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Razon Social')),
                ('cuit', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Formato931',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('fromm', models.PositiveSmallIntegerField()),
                ('long', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['fromm'],
            },
        ),
        migrations.CreateModel(
            name='TipoRegistro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Presentacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo', models.DateField()),
                ('employees', models.PositiveSmallIntegerField(default=0)),
                ('remunerativos', models.FloatField(default=0.0)),
                ('no_remunerativos', models.FloatField(default=0.0)),
                ('closed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='export_lsd.empresa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Presentaciones',
            },
        ),
        migrations.CreateModel(
            name='OrdenRegistro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('fromm', models.PositiveSmallIntegerField()),
                ('long', models.PositiveSmallIntegerField()),
                ('type', models.CharField(choices=[('AL', 'Alfabético'), ('AN', 'Alfanumérico'), ('NU', 'Numérico')],
                                          default='AN', max_length=2)),
                ('description', models.TextField(blank=True, null=True)),
                ('formatof931', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                  to='export_lsd.formato931')),
                ('tiporegistro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='export_lsd.tiporegistro')),
            ],
            options={
                'ordering': ['tiporegistro__order', 'fromm'],
            },
        ),
        migrations.CreateModel(
            name='Liquidacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nroLiq', models.PositiveSmallIntegerField(default=1)),
                ('payday', models.DateField()),
                ('employees', models.PositiveSmallIntegerField(default=0)),
                ('remunerativos', models.FloatField(default=0.0)),
                ('no_remunerativos', models.FloatField(default=0.0)),
                ('tipo_liq', models.CharField(choices=[('M', 'Mes'), ('Q', 'Quincena'), ('D', 'Días'), ('H', 'Horas')],
                                              default='M', max_length=1, verbose_name='Tipo Liq.')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('presentacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='export_lsd.presentacion')),
            ],
            options={
                'verbose_name_plural': 'Liquidaciones',
                'unique_together': {('nroLiq', 'presentacion')},
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leg', models.PositiveSmallIntegerField()),
                ('name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Nombre')),
                ('cuil', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11)])),
                ('area', models.CharField(blank=True, max_length=120, null=True, verbose_name='Área de Trabajo')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='export_lsd.empresa')),
            ],
            options={
                'ordering': ['empresa__name', 'leg'],
                'unique_together': {('leg', 'empresa')},
            },
        ),
        migrations.CreateModel(
            name='ConceptoLiquidacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concepto', models.CharField(max_length=10)),
                ('cantidad', models.PositiveSmallIntegerField(default=0)),
                ('importe', models.FloatField(default=0)),
                ('tipo', models.CharField(default='Rem', max_length=4, verbose_name='Tipo de Concepto')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='export_lsd.empleado')),
                ('liquidacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='export_lsd.liquidacion')),
            ],
            options={
                'verbose_name_plural': 'ConceptoLiquidaciones',
            },
        ),
        migrations.CreateModel(
            name='BasicExportConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nombre')),
                ('dias_base', models.PositiveSmallIntegerField(default=30, verbose_name='Días Base')),
                ('forma_pago', models.CharField(choices=[('1', 'Efectivo'), ('2', 'Cheque'), ('3', 'Acreditación')],
                                                default='1', max_length=1, verbose_name='Forma de Pago')),
                ('ccn_sueldo', models.CharField(max_length=20, verbose_name='Concepto Sueldo')),
                ('ccn_no_rem', models.CharField(blank=True, max_length=20, null=True, verbose_name='Concepto NR')),
                ('ccn_no_osysind', models.CharField(blank=True, max_length=20, null=True, verbose_name='Concepto NR OS y Sind')),
                ('ccn_no_sind', models.CharField(blank=True, max_length=20, null=True, verbose_name='Concepto NR Sind.')),
                ('ccn_sijp', models.CharField(max_length=20, verbose_name='Concepto SIJP')),
                ('ccn_inssjp', models.CharField(max_length=20, verbose_name='Concepto INSSJP')),
                ('ccn_os', models.CharField(max_length=20, verbose_name='Concepto OS')),
                ('ccn_sindicato', models.CharField(blank=True, max_length=20, null=True, verbose_name='Concepto Sindicato')),
                ('porc_sindicato', models.FloatField(default=0, verbose_name='Porcentaje Sindicato')),
                ('tipo_nr', models.CharField(choices=[('0', 'Sólo NR'), ('1', 'Base Sindicato'),
                                                      ('2', 'Base Sindicato y Obra Social')], default='2', max_length=1,
                                             verbose_name='Tipo NR')),
                ('area', models.CharField(default='Administración', max_length=120, verbose_name='Área de Trabajo')),
                ('cuit_empleador_eventuales', models.IntegerField(blank=True, null=True, verbose_name='CUIT Empresa Eventual')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'name')},
            },
        ),
    ]
