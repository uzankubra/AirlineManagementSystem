from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='flight',
            constraint=models.CheckConstraint(condition=models.Q(('departure_time__lt', models.F('arrival_time'))), name='check_departure_before_arrival'),
        ),
        migrations.AddConstraint(
            model_name='flight',
            constraint=models.UniqueConstraint(fields=('airplane', 'departure_time', 'arrival_time'), name='unique_airplane_schedule'),
        ),
    ]
