class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def add_stock(self, amount):
        self.stock += amount

    def reduce_stock(self, amount):
        if amount <= self.stock:
            self.stock -= amount

    def is_low_stock(self):
        return self.stock < 5


class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def find_product_by_id(self, product_id):
        for p in self.products:
            if p.product_id == product_id:
                return p
        return None

    def show_all_products(self):
        for p in self.products:
            print(f"{p.product_id} | {p.name} | Stok: {p.stock}")

    def show_low_stock_items(self):
        for p in self.products:
            if p.is_low_stock():
                print(f"⚠ {p.name} stok hampir habis ({p.stock})")
