"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from tests.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product1():
    return Product("pencil", 10, "This is a pencil", 100)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(321) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(50)
        assert product.quantity == 950

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            assert product.buy(product.quantity + 1)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_check_cart_empty(self, cart):
        assert cart.products == {}

    def test_buy_empty_cart(self, cart):
        with pytest.raises(ValueError):
            cart.buy()
        # тест падает, но не пойму причину. выдает Failed: DID NOT RAISE <class 'ValueError'>

    def test_add_products(self, cart, product, product1):
        cart.add_product(product, 555)
        assert cart.products[product] == 555

        cart.add_product(product1, 20)
        assert cart.products[product1] == 20

    def test_cart_buy(self, cart, product, product1):
        cart.add_product(product, 100)
        cart.buy()
        assert product.quantity == 900

    def test_buy_products_more_than_available(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError, match=f'Товара {product.name} недостаточно на складе.'):
            cart.buy()
        # если прописать тест без match =, то он проходит
        # но с указанием текста для вывода идет ошибка
        # AssertionError: Regex pattern did not match.
        # Regex: 'Товара book недостаточно на складе'
        # Input: 'Недостаточно товара'
        # не соображу - откуда тянется это несоответсвие результатов?

    def test_remove_some_products(self, cart, product, product1):
        cart.add_product(product, 555)
        cart.add_product(product1, 20)
        assert cart.products[product] == 555
        assert cart.products[product1] == 20
        cart.remove_product(product1, 15)
        assert cart.products[product] == 555
        assert cart.products[product1] == 5

    def test_remove_all_products(self, cart, product):
        cart.add_product(product, 555)
        cart.remove_product(product, 555)
        assert product not in cart.products

    def test_remove_more_than_added(self, cart, product):
        cart.add_product(product, 555)
        with pytest.raises(ValueError):
            cart.remove_product(product, 600)
        #тоже ругается на ValueError

    def test_clear_cart(self, cart, product, product1):
        cart.add_product(product, 555)
        cart.add_product(product1, 20)
        assert cart.products[product] == 555
        assert cart.products[product1] == 20
        cart.clear()
        assert len(cart.products) == 0

    def test_total_price(self, cart, product, product1):
        cart.add_product(product, 555)
        cart.add_product(product1, 20)
        assert cart.get_total_price() == (product.price * 555) + (product1.price * 20)
        # можно ли эту проверку написать проще, чтобы не перечислять price и buy_count каждого продукта из корзины,
        # и в то же время не вписывать вручную ожидаемое числовое значение?
        # теоретически можно задать переменную expected_result и в нее поместить (product.price * 555) + (product1.price *20)
        # но это все равно кажется неверным, вдруг товаров 100+ в лучшем случае?
        # просится что-то вроде "возьми цены всех продуктов и умножай их на buy_count соответсвенно"
