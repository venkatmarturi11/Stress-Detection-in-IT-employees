from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegistrationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('loginid', models.CharField(unique=True, max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('mobile', models.CharField(unique=True, max_length=100)),
                ('email', models.CharField(unique=True, max_length=100)),
                ('locality', models.CharField(max_length=100, blank=True, default='')),
                ('address', models.CharField(max_length=1000, blank=True, default='')),
                ('city', models.CharField(max_length=100, blank=True, default='')),
                ('state', models.CharField(max_length=100, blank=True, default='')),
                ('status', models.CharField(max_length=100)),
                ('cdate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'UserRegistrations',
            },
        ),
        migrations.CreateModel(
            name='UserImagePredictionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('loginid', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('emotions', models.CharField(max_length=10000)),
                ('stress_level', models.CharField(default='Low', max_length=50)),
                ('confidence', models.IntegerField(default=0)),
                ('eye_strain', models.CharField(default='Normal', max_length=50)),
                ('brow_tension', models.CharField(default='Normal', max_length=50)),
                ('facial_fatigue', models.CharField(default='Normal', max_length=50)),
                ('file', models.FileField(blank=True, null=True, upload_to='files/')),
                ('cdate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'UserStressImageResults',
            },
        ),
        migrations.CreateModel(
            name='UserSurveyPredictionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.IntegerField()),
                ('designation', models.IntegerField()),
                ('company_type', models.IntegerField()),
                ('wfh_setup', models.IntegerField()),
                ('resource_allocation', models.FloatField()),
                ('mental_fatigue', models.FloatField()),
                ('stress_percentage', models.FloatField()),
                ('risk_level', models.CharField(max_length=20)),
                ('cdate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'UserSurveyPredictions',
            },
        ),
    ]
