from decimal import Decimal
from django.shortcuts import get_object_or_404
from main.models import Product


class Cart:

    def __init__(self, request): 
        self.session = request.session # хз куда писать, сессия - это куки 1:52:23
        cart = self.session.get('cart') # пытаемся достать ключ cart
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, size,  quantity = 1, override_quantity = False):
        product_id = str(product.id)
        size_name = str(size)

        cart_key = f"{product_id}_{size_name}" # чтобы товары разных размеров отличались, ибо у product_id одинаковый

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'quantity': 0,
                'price': str(product.price),
                'product_id': product_id,
                'size': size_name,
            }

        if override_quantity:
            self.cart['cart_key']['quantity'] = override_quantity
        else:
            self.cart['cart_key']['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True # сигнал джанго, что session мы изменили, и нужно сохранить

    def remove(self, product, size):
        product_id = str(product.id)
        size_name = str(size)
        cart_key = f"{product_id}_{size_name}" 

        if cart_key in self.cart:
            del self.cart['cart_key']
            self.save()

    
    def update_quantity(self, product, size, quantity):
        if quantity <= 0:
            self.remove(product, size)
        else:
            self.add(self, product, size,  quantity, override_quantity = True)

    
    def __iter__(self):
        product_ids = [item['product_id'] for item in self.cart.values()] # массив с айдишниками
        products = Product.objects.filter(id__in=product_ids) # фильтруем по айдишникам, собирая массив продуктов
        cart = self.cart.copy()

        for product in products:
            for cart_key, cart_item in cart.items():
                if cart_item['product_id'] == str(product.id):
                    cart_item['product'] = product
                    cart_item['total_price'] = Decimal(cart_item['price']) * cart_item['quantity']
                    yield cart_item # возвращаем??? cart_item

    def __len__(self):
        lenght = sum(item['quantity'] for item in self.cart.values())
        return lenght
    
    def get_total_price(self):
        total = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        return total
    
    def clear(self):
        del self.session['cart'] # удаляем куки, которые связанны по ключу cart
        self.save()
    

    def get_cart_items(self): # для оплаты товаров нужно будет
        items = []
        for item in self:
            items.append({
                'product': item['product'],
                'quantity': item['quantity'],
                'size': item['size'],
                'price': Decimal(item['price']),
                'total_price': item['total_price'],
                'cart_key': f'{item['product_id']}_{item['size']}'
            })
        return items