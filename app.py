from flask import Flask, render_template , request , redirect , url_for , session , flash

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = "dev-secret-key" ## for session cart

# Data dummy produk
PRODUCTS = [
    {"id": 1, "name": "Laptop Pro", "price": 1499.0},
    {"id": 2, "name": "Wireless Mouse", "price": 29.0},
    {"id": 3, "name": "Mechanical Keyboard", "price": 89.0},
    {"id": 4, "name": "USB-C Hub", "price": 39.0},
    {"id": 5, "name": "Noise Cancelling Headphones", "price": 199.0},
]

def get_cart():
    session.setdefault("cart", [])
    return session["cart"]

def cart_items():
    ids = get_cart()
    items = [p for p in PRODUCTS if p["id"] in ids]
    return items

@app.context_processor
def inject_cart_count():
    return {"cart_count": len(get_cart())}

@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS)

@app.route("/search")
def search():
    q = request.args.get("search", "").strip().lower()
    results = [p for p in PRODUCTS if q in p["name"].lower()] if q else PRODUCTS
    return render_template("search.html", products=results, q=request.args.get("search", ""))

@app.post("/add-to-cart/<int:pid>")
def add_to_cart(pid):
    cart = get_cart()
    if pid not in cart:
        cart.append(pid)
        session.modified = True
    else:
        flash("Item already in cart.")
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    items = cart_items()
    total = sum(p["price"] for p in items)
    return render_template("cart.html", items=items, total=total)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        # tangkap data form (validasi sederhana)
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        if not (name and email and address):
            # tampilkan kembali form dengan pesan error sederhana
            return render_template("checkout.html", error="All fields are required.")
        # proses “pesanan”
        session["cart"] = []
        return render_template("success.html", name=name)
    return render_template("checkout.html")

if __name__ == "__main__":
    app.run(debug=True)