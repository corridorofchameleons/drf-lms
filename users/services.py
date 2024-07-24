from config.settings import STRIPE_API_KEY
import stripe

stripe.api_key = STRIPE_API_KEY


def create_product(name):
    product = stripe.Product.create(name=name)
    return product


def create_price(price, name):
    '''
    Создает объект цены
    '''
    response = stripe.Price.create(
        currency="rub",
        unit_amount=price,
        product=create_product(name)
    )
    return response


def create_session(price, name):
    '''
    Создает сессию в страйпе
    '''
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/api/lessons/",
        line_items=[{"price": create_price(price, name), "quantity": 1}],
        mode="payment",
    )
    return session.id, session.get('url')


