import streamlit as st

class Product:
    def __init__(self, name: str, price: float):
        self._name = None
        self._price = None
        self.name = name
        self.price = price

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Nama produk harus berupa string tidak kosong.")
        self._name = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not (isinstance(value, (int, float)) and value >= 0):
            raise ValueError("Harga harus angka >= 0.")
        self._price = float(value)

    def subtotal(self, qty: int):
        return self.price * qty


class Cart:
    def __init__(self):
        # items: list of dict {'product': Product, 'qty': int}
        self.items = []

    def add_item(self, product: Product, qty: int):
        # jika produk sudah ada, tambahkan qty
        for it in self.items:
            if it["product"].name == product.name:
                it["qty"] += qty
                return
        self.items.append({"product": product, "qty": qty})

    def update_item(self, product_name: str, qty: int):
        for it in self.items:
            if it["product"].name == product_name:
                if qty <= 0:
                    self.items.remove(it)
                else:
                    it["qty"] = qty
                return

    def remove_item(self, product_name: str):
        self.items = [it for it in self.items if it["product"].name != product_name]

    def clear(self):
        self.items = []

    def total(self):
        return sum(it["product"].subtotal(it["qty"]) for it in self.items)

    def receipt_text(self):
        lines = []
        for it in self.items:
            p = it["product"]
            q = it["qty"]
            lines.append(f"{p.name} x{q} = Rp {p.subtotal(q):,.0f}")
        lines.append("-" * 30)
        lines.append(f"TOTAL = Rp {self.total():,.0f}")
        return "\n".join(lines)

class ProductRepository:
    def __init__(self, initial=None):
        self._products = initial[:] if initial else []

    def create_product(self, name: str, price: float):
        if self.get_by_name(name) is not None:
            raise ValueError("Produk dengan nama sama sudah ada.")
        p = Product(name, price)
        self._products.append(p)
        return p

    def get_all(self):
        return list(self._products)

    def get_by_name(self, name: str):
        for p in self._products:
            if p.name == name:
                return p
        return None

    def update_product(
        self, old_name: str, new_name: str = None, new_price: float = None
    ):
        p = self.get_by_name(old_name)
        if p is None:
            raise ValueError("Produk tidak ditemukan.")
        # cek jika ganti nama dan nama baru sudah ada
        if new_name and new_name != old_name and self.get_by_name(new_name):
            raise ValueError("Nama baru sudah digunakan produk lain.")
        if new_name:
            p.name = new_name
        if new_price is not None:
            p.price = new_price
        return p

    def delete_product(self, name: str):
        p = self.get_by_name(name)
        if p is None:
            raise ValueError("Produk tidak ditemukan.")
        self._products.remove(p)


# =========================
# 3) DATA AWAL
# =========================
default_catalog = [
    Product("Kopi Hitam", 15000),
    Product("Latte", 25000),
    Product("Roti Bakar", 20000),
    Product("Es Teh", 10000),
]


# =========================
# 4) STREAMLIT UI
# =========================
st.title("Kasir Sederhana (CRUD + Setter/Getter)")

# initialize repo and cart di session state
if "repo" not in st.session_state:
    st.session_state.repo = ProductRepository(initial=default_catalog)
if "cart" not in st.session_state:
    st.session_state.cart = Cart()

st.header("Katalog Produk (CRUD)")

# show current products
products = st.session_state.repo.get_all()
cols = st.columns([3, 1, 1])
with cols[0]:
    st.subheader("Daftar Produk")
    for p in products:
        st.write(f"- {p.name} — Rp {p.price:,.0f}")

# Form tambah produk (Create)
with st.form("form_add"):
    st.write("Tambah Produk Baru")
    new_name = st.text_input("Nama produk", key="add_name")
    new_price = st.number_input(
        "Harga (Rp)", min_value=0, value=1000, step=500, key="add_price"
    )
    submitted = st.form_submit_button("Tambah")
    if submitted:
        try:
            st.session_state.repo.create_product(new_name, new_price)
            st.success(f"Produk '{new_name}' ditambahkan.")
        except Exception as e:
            st.error(str(e))

st.divider()

# Form update / delete (Read + Update + Delete)
st.subheader("Edit / Hapus Produk")
product_names = [p.name for p in products]
if product_names:
    sel = st.selectbox("Pilih produk", product_names, key="sel_edit")
    p = st.session_state.repo.get_by_name(sel)
    col1, col2 = st.columns(2)
    with col1:
        upd_name = st.text_input("Nama baru", value=p.name, key="upd_name")
    with col2:
        upd_price = st.number_input(
            "Harga baru", min_value=0, value=int(p.price), step=500, key="upd_price"
        )
    if st.button("Simpan Perubahan"):
        try:
            st.session_state.repo.update_product(
                p.name, new_name=upd_name, new_price=upd_price
            )
            st.success("Produk diperbarui.")
        except Exception as e:
            st.error(str(e))
    if st.button("Hapus Produk"):
        try:
            st.session_state.repo.delete_product(p.name)
            # juga hapus dari cart jika ada
            st.session_state.cart.remove_item(p.name)
            st.warning("Produk dihapus.")
        except Exception as e:
            st.error(str(e))
else:
    st.info("Belum ada produk di katalog.")

st.divider()

# Cart UI (CRUD operasi pada cart)
st.header("Keranjang (CRUD)")

colp, colq = st.columns([2, 1])
with colp:
    pilihan = st.selectbox(
        "Pilih Produk untuk Keranjang",
        [p.name for p in st.session_state.repo.get_all()],
        key="cart_sel",
    )
with colq:
    qty = st.number_input("Jumlah", min_value=1, value=1, step=1, key="cart_qty")

if st.button("Tambah ke Keranjang"):
    prod = st.session_state.repo.get_by_name(pilihan)
    if prod:
        st.session_state.cart.add_item(prod, qty)
        st.success(f"{pilihan} x{qty} ditambahkan.")
    else:
        st.error("Produk tidak ditemukan.")

st.divider()

# tampilkan isi cart + update/remove per item
if not st.session_state.cart.items:
    st.info("Keranjang masih kosong.")
else:
    st.subheader("Isi Keranjang")
    for it in st.session_state.cart.items[:]:
        p = it["product"]
        q = it["qty"]
        cols = st.columns([3, 1, 1])
        cols[0].write(f"{p.name} — Rp {p.price:,.0f}")
        new_q = cols[1].number_input("Qty", min_value=0, value=q, key=f"qty_{p.name}")
        if cols[2].button("Perbarui", key=f"upd_{p.name}"):
            st.session_state.cart.update_item(p.name, int(new_q))
            st.experimental_rerun()
        if cols[2].button("Hapus", key=f"del_{p.name}"):
            st.session_state.cart.remove_item(p.name)
            st.experimental_rerun()

    st.metric("Total Bayar", f"Rp {st.session_state.cart.total():,.0f}")
    st.text("NOTA:")
    st.code(st.session_state.cart.receipt_text())

if st.button("Reset Keranjang"):
    st.session_state.cart.clear()
    st.warning("Keranjang direset.")
