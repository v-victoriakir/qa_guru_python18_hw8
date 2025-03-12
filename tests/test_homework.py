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
        assert product.check_quantity(999) is True
        assert product.check_quantity(1000) is True
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

    ## корзина пустая
    def test_check_cart_empty(self, cart):
        assert cart.products == {}

    ## добавление товара
    def test_add_products(self, cart, product, product1):
        cart.add_product(product, 555)
        assert cart.products[product] == 555

        cart.add_product(product1, 20)
        assert cart.products[product1] == 20

    ## повторное добавление "ещё товара" (уже был в корзине, добавляем)
    def test_add_same_product_several_times(self, cart, product, product1):
        cart.add_product(product, 555)
        cart.add_product(product1, 20)
        assert cart.products[product] == 555
        assert cart.products[product1] == 20
        cart.add_product(product1, 80)
        assert cart.products[product] == 555
        assert cart.products[product1] == 100

    ## удаление части добавленного товара
    def test_remove_products_partial(self, cart, product, product1):
        cart.add_product(product, 555)
        cart.add_product(product1, 20)
        cart.remove_product(product1, 15)
        assert cart.products[product] == 555
        assert cart.products[product1] == 5

    ## удаление добавленного товара
    def test_remove_the_added_product(self, cart, product):
        cart.add_product(product, 555)
        cart.remove_product(product, 555)
        assert product not in cart.products

    ## попытка удалить больше товара, чем есть в корзине
    def test_remove_more_than_added(self, cart, product):
        cart.add_product(product, 555)
        cart.remove_product(product, 600)
        assert product not in cart.products

    ## удаление товара без указания кол-ва
    def test_remove_the_added_product_quantity_not_specified(self, cart, product):
        cart.add_product(product, 555)
        cart.remove_product(product)
        assert product not in cart.products

    ## полное очищение корзины через clear
    def test_clear_cart(self, cart, product, product1):
        cart.add_product(product, 555)
        cart.add_product(product1, 20)
        cart.clear()
        assert len(cart.products) == 0

    ## подсчет стоимости корзины
    def test_total_price(self, cart, product, product1):
        cart.add_product(product, 555)
        cart.add_product(product1, 20)
        expected_result = (product.price * 555) + (product1.price * 20)
        assert cart.get_total_price() == expected_result

    ## попытка купить пустую корзину
    def test_buy_empty_cart(self, cart):
        with pytest.raises(ValueError):
            cart.buy()

    ## покупка добавленного товара
    def test_cart_buy_one_product(self, cart, product):
        cart.add_product(product, 100)
        cart.buy()
        assert product.quantity == 900

    ## покупка нескольких товаров
    def test_cart_buy_several_products(self, cart, product, product1):
        cart.add_product(product, 500)
        cart.add_product(product1, 50)
        cart.buy()
        assert product.quantity == 500
        assert product1.quantity == 50

    ## попытка покупки товаров больше, чем доступно
    def test_buy_products_more_than_available(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            cart.buy()
        assert product.quantity == 1000

    ## попытка покупки корзины с более чем одним товаром, но только одного не хватает (покупка не пройдет)
    def test_buy_cart_but_one_product_is_missing(self, cart, product, product1):
        cart.add_product(product, 999)
        cart.add_product(product1, 101)
        with pytest.raises(ValueError):
            cart.buy()
        assert product.quantity == 1000
        assert product1.quantity == 100
