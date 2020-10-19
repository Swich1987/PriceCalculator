import json
from decimal import Decimal, getcontext
from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase, RequestFactory

from .views import calc_price_with_discount, NO_KEY_STR, KEY_MUST_BE_DECIMAL, make_error_response, \
    calc_price_with_state_tax

MODULE_PATH = 'api.views'


class EndpointTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        getcontext().prec = 2

        cls.request_factory = RequestFactory()
        return super().setUpClass()

    @staticmethod
    def func_for_test(request):
        raise NotImplementedError('Implement this function for test.')

    def _check_response(self, data, expected_json):
        request = self.request_factory.post('/path/', data=data, content_type='application/json')

        response = self.__class__.func_for_test(request)
        json_result = json.loads(response.content)

        self.assertDictEqual(json_result, expected_json)

    def _test_make_error_response(self, data, err_text):
        expected_response = make_error_response(err_text)
        expected_json = json.loads(expected_response.content)

        self._check_response(data, expected_json)

    def _test_no_param_in_request(self, data, param=''):
        self._test_make_error_response(data, NO_KEY_STR.format(param))

    def _test_wrong_decimal_param_in_request(self, data, param):
        self._test_make_error_response(data, KEY_MUST_BE_DECIMAL.format(param))


class CalcPriceWithDiscountTestCase(EndpointTestCase):
    func_for_test = calc_price_with_discount

    def test_no_price_in_request(self):
        self._test_no_param_in_request(data={}, param='price')

    def test_wrong_price_in_request(self):
        self._test_wrong_decimal_param_in_request(data={'price': 'test'}, param='price')

    def _check_calculation(self, base_price, expect_rate, mock_discount):
        data = {'price': base_price}

        mock_discount_1 = MagicMock(order_price=1000, discount_rate=Decimal(10))
        mock_discount_2 = MagicMock(order_price=2000, discount_rate=Decimal(20))
        mock_discount.objects.order_by('order_price').all.return_value = [mock_discount_1, mock_discount_2]

        expect_price = Decimal(base_price) * Decimal((1 - expect_rate / 100))
        expected_json = {'price_with_discount': str(expect_price)}

        self._check_response(data=data, expected_json=expected_json)

    @patch(f'{MODULE_PATH}.Discount')
    def test_positive_calculation(self, mock_discount):
        self._check_calculation(base_price=999, expect_rate=0, mock_discount=mock_discount)
        self._check_calculation(base_price=1000, expect_rate=10, mock_discount=mock_discount)
        self._check_calculation(base_price=1999, expect_rate=10, mock_discount=mock_discount)
        self._check_calculation(base_price=2000, expect_rate=20, mock_discount=mock_discount)


class CalcPriceWithStateTaxTestCase(EndpointTestCase):
    func_for_test = calc_price_with_state_tax

    def test_no_price_in_request(self):
        self._test_no_param_in_request(data={'state_code': 'CA'}, param='price')

    def test_no_state_code_in_request(self):
        self._test_no_param_in_request(data={'price': 1000}, param='state_code')

    def test_wrong_price_in_request(self):
        self._test_wrong_decimal_param_in_request(data={'price': 'test', 'state_code': 'CA'}, param='price')

    def _check_calculation(self, base_price, expect_rate, mock_state_tax):
        state_code = 'CA'
        data = {'price': base_price, 'state_code': state_code}

        mock_state_tax.objects.get(state_code=state_code).tax_rate = Decimal(expect_rate)

        expect_price = Decimal(base_price) * Decimal((1 - expect_rate / 100))
        expected_json = {'price_with_state_tax': str(expect_price)}

        self._check_response(data=data, expected_json=expected_json)

    @patch(f'{MODULE_PATH}.StateTax')
    def test_positive_calculation(self, mock_state_tax):
        self._check_calculation(base_price=999, expect_rate=0, mock_state_tax=mock_state_tax)
        self._check_calculation(base_price=1000, expect_rate=10, mock_state_tax=mock_state_tax)
        self._check_calculation(base_price=1999, expect_rate=10, mock_state_tax=mock_state_tax)
        self._check_calculation(base_price=2000, expect_rate=20, mock_state_tax=mock_state_tax)
