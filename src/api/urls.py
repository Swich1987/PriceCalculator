from django.urls import path

from .views import calc_price_with_discount, calc_price_with_state_tax, state_codes_list

urlpatterns = [
    path('state_code_list', state_codes_list, name='state-codes-list'),
    path('price_with_discount', calc_price_with_discount,
         name='calc-price-with_discount'),
    path('price_with_state_tax', calc_price_with_state_tax,
         name='calc-price-with-state-tax')
]
