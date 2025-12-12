import streamlit as st

# =============================
# OOP CLASSES
# =============================

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
        return self.products

    def show_low_stock_items(self):
        return [p for p in self.products if p.is_low_stock()]


# =============================
# STREAMLIT APP
# =============================

st.title("📦 Inventory Management System (OOP + Streamlit)")

# simpan data di session_state agar tidak hilang
if "inventory" not in st.session_state:
    st.session_state.inventory = Inventory()

menu = st.sidebar.selectbox(
    "Menu",
    ["Tambah Produk", "Lihat Semua Produk", "Update Stok", "Produk Stok Rendah"]
)

inventory = st.session_state.inventory


# =============================
# 1. TAMBAH PRODUK
# =============================
if menu == "Tambah Produk":
    st.header("➕ Tambah Produk Baru")

    product_id = st.text_input("ID Produk")
    name = st.text_input("Nama Produk")
    price = st.number_input("Harga", min_value=0)
    stock = st.number_input("Stok Awal", min_value=0)

    if st.button("Tambah"):
        if product_id and name:
            new_product = Product(product_id, name, price, stock)
            inventory.add_product(new_product)
            st.success(f"Produk '{name}' berhasil ditambahkan!")
        else:
            st.error("Mohon isi seluruh informasi produk!")


# =============================
# 2. LIHAT SEMUA PRODUK
# =============================
elif menu == "Lihat Semua Produk":
    st.header("📋 Daftar Semua Produk")

    products = inventory.show_all_products()

    if not products:
        st.info("Belum ada produk yang ditambahkan.")
    else:
        for p in products:
            st.write(f"### {p.name}")
            st.write(f"- ID: {p.product_id}")
            st.write(f"- Harga: Rp{p.price}")
            st.write(f"- Stok: {p.stock}")
            st.write("---")


# =============================
# 3. UPDATE STOK
# =============================
elif menu == "Update Stok":
    st.header("🔧 Update Stok Produk")

    product_id = st.text_input("Masukkan ID Produk")
    product = None

    if product_id:
        product = inventory.find_product_by_id(product_id)

    if product:
        st.write(f"**Nama:** {product.name}")
        st.write(f"**Stok Saat Ini:** {product.stock}")

        choice = st.radio("Pilih Aksi", ["Tambah Stok", "Kurangi Stok"])
        amount = st.number_input("Jumlah", min_value=1)

        if st.button("Update"):
            if choice == "Tambah Stok":
                product.add_stock(amount)
                st.success("Stok berhasil ditambahkan!")
            else:
                if amount <= product.stock:
                    product.reduce_stock(amount)
                    st.success("Stok berhasil dikurangi!")
                else:
                    st.error("Jumlah pengurangan melebihi stok!")
    else:
        if product_id:
            st.error("Produk tidak ditemukan.")


# =============================
# 4. PRODUK DENGAN STOK RENDAH
# =============================
elif menu == "Produk Stok Rendah":
    st.header("⚠ Produk dengan Stok Rendah (<5)")

    low_stock_items = inventory.show_low_stock_items()

    if not low_stock_items:
        st.info("Tidak ada produk yang stoknya rendah.")
    else:
        for p in low_stock_items:
            st.write(f"### {p.name}")
            st.write(f"ID: {p.product_id}")
            st.write(f"Stok: {p.stock}")
            st.write("---")
