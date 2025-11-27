class Produk:
    def __init__(self, produk_id, nama, harga, stok):
        self.produk_id = produk_id
        self.nama = nama
        self.harga = harga
        self.stok = stok 

    def add_stok(self, amount):
        self.stok += amount

    def reduce_stok(self, amount):
        if amount <= self.stok:
            self.stok -= amount

    def is_low_stok(self):
        return self.stok < 5


class Inventory:
    def __init__(self):
        self.produk = []

    def add_produk(self, produk):
        self.produk.append(produk)

    def find_produk_by_id(self, produk_id):
        for p in self.produk:
            if p.produk_id == produk_id:
                return p
        return None

    def show_all_produk(self):
        for p in self.produk:
            print(f"{p.produk_id} | {p.nama} | Stok: {p.stok}")

    def show_low_stok_items(self):
        for p in self.produk:
            if p.is_low_stok():
                print(f"⚠ {p.nama} stok hampir habis ({p.stok})")