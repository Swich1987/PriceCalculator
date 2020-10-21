import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_price', models.DecimalField(decimal_places=2, max_digits=16, unique=True)),
                ('discount_rate',
                 models.DecimalField(decimal_places=2, default=0, help_text='Discount rate in percent.', max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('code', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StateTax',
            fields=[
                ('state',
                 models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False,
                                      to='api.state')),
                ('tax_rate', models.DecimalField(decimal_places=2, default=0, help_text='State tsx rate in percent.',
                                                 max_digits=5)),
            ],
        )
    ]
