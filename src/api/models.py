from decimal import Decimal

from django.db import models


class State(models.Model):
    name = models.TextField(unique=True)
    code = models.TextField()

    def __str__(self):
        return f'State {self.name}, code {self.code}'


class StateTax(models.Model):
    state = models.OneToOneField(State, null=False, blank=False,
                                 on_delete=models.DO_NOTHING, primary_key=True)
    tax_rate = models.DecimalField(null=False, blank=False, max_digits=16,
                                   decimal_places=4, default=Decimal(0),
                                   help_text='State tsx rate.')

    def  __str__(self):
        return f'StateTax in state {self.state.code} is {self.tax_rate * 100}%'


class Discount(models.Model):
    order_price = models.DecimalField(null=False, blank=False, max_digits=16,
                                      decimal_places=4, unique=True)
    discount_rate = models.DecimalField(null=False, blank=False, max_digits=16,
                                        decimal_places=4, default=Decimal(0),
                                        help_text='Discount rate.')

    def  __str__(self):
        return f'For {self.order_price} discount rate is ' \
               f'{self.discount_rate * 100}%'
