import stripe
from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY

def create_stripe_product(prod):
    """Создает продукт в Stripe."""
    product = prod.course if prod.course else prod.lesson
    stripe_product = stripe.Product.create(name=product)
    return stripe_product.get("id")


def convert_rub_to_dollars(amount):
    """Конвертирует рубли в доллары"""
    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return int(amount * rate)


def create_stripe_price(amount, product_id):
    """Создает цену в Stripe."""
    return stripe.Price.create(
        currency="RUB",
        unit_amount=amount * 100,
        product_data={"name": product_id},
    )


def create_stripe_session(price):
    """Создает сессию на оплату в Stripe."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


