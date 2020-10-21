import json
from decimal import Decimal, InvalidOperation
from http import HTTPStatus

from django.http import JsonResponse

from .models import Discount, StateTax

NO_KEY_STR = 'No "{}" key.'
KEY_MUST_BE_DECIMAL = '"{}" must be decimal number.'


def make_error_response(message):
    return JsonResponse({"message": message}, status=HTTPStatus.BAD_REQUEST)


def quantize_decimal(dec: Decimal) -> Decimal:
    return dec.quantize(Decimal('0.01'))


def state_codes_list(request):
    states_with_tax = StateTax.objects.values_list("state__code", flat=True)
    return JsonResponse({"states": list(states_with_tax)})


def calc_price_with_discount(request):
    body = json.loads(request.body)

    try:
        base_price = Decimal(body['price'])
    except KeyError:
        return make_error_response(NO_KEY_STR.format("price"))
    except InvalidOperation:
        return make_error_response(KEY_MUST_BE_DECIMAL.format("price"))

    discount_rate = Decimal(0)

    for discount in Discount.objects.order_by('order_price').all():
        if discount.order_price > base_price:
            break

        discount_rate = discount.discount_rate

    price_with_discount = base_price * (1 - discount_rate)

    return JsonResponse({"price_with_discount": quantize_decimal(price_with_discount)})


def calc_price_with_state_tax(request):
    body = json.loads(request.body)

    try:
        base_price = Decimal(body['price'])
        state_code = body['state_code']

    except KeyError as err:
        return make_error_response(NO_KEY_STR.format(err.args[0]))

    except InvalidOperation:
        return make_error_response(KEY_MUST_BE_DECIMAL.format("price"))

    tax_rate = StateTax.objects.get(state__code=state_code).tax_rate
    price_with_state_tax = base_price * (1 - tax_rate)

    return JsonResponse({"price_with_state_tax": quantize_decimal(price_with_state_tax)})
