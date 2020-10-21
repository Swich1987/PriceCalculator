import logging
from decimal import Decimal

from django.db import migrations

DEFAULT_STATES = [
    ('Utah', 'UT'),
    ('Nevada', 'NV'),
    ('Texas', 'TX'),
    ('Alabama', 'AL'),
    ('California', 'CA')
]

DEFAULT_STATE_TAXES = [
    ('UT', Decimal(0.0685)),
    ('NV', Decimal(0.08)),
    ('TX', Decimal(0.0625)),
    ('AL', Decimal(0.04)),
    ('CA', Decimal(0.0825))
]

DEFAULT_ORDER_DISCOUNTS = [
    (Decimal(1000), Decimal(0.03)),
    (Decimal(5000), Decimal(0.05)),
    (Decimal(7000), Decimal(0.07)),
    (Decimal(10000), Decimal(0.01)),
    (Decimal(50000), Decimal(0.015))
]


def add_default_states(apps, schema_editor):
    State = apps.get_model('api', 'State')

    for name, code in DEFAULT_STATES:
        State.objects.get_or_create(name=name, code=code)


def add_default_state_taxes(apps, schema_editor):
    State = apps.get_model('api', 'State')
    StateTax = apps.get_model('api', 'StateTax')

    logging.error([state.code for state in State.objects.all()])
    for state_code, state_tax_rate in DEFAULT_STATE_TAXES:
        logging.error(f'{state_code=}')
        state = State.objects.get(code=state_code)
        StateTax.objects.get_or_create(state=state, tax_rate=state_tax_rate)


def add_default_discounts(apps, schema_editor):
    Discount = apps.get_model('api', 'Discount')

    for order_price, discount_rate in DEFAULT_ORDER_DISCOUNTS:
        Discount.objects.get_or_create(order_price=order_price, discount_rate=discount_rate)


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_states),
        migrations.RunPython(add_default_state_taxes),
        migrations.RunPython(add_default_discounts),
    ]
