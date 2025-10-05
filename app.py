from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Product, Location, ProductMovement
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route("/")
def index():
    return redirect(url_for("list_products"))

# PRODUCTS
@app.route("/products")
def list_products():
    products = Product.query.all()
    return render_template("products/list.html", products=products)

@app.route("/products/add", methods=["GET","POST"])
def add_product():
    if request.method == "POST":
        pid = request.form.get("product_id") or None
        name = request.form["name"]
        desc = request.form.get("description")
        p = Product(product_id=pid, name=name, description=desc)
        db.session.add(p); db.session.commit()
        flash("Product added")
        return redirect(url_for("list_products"))
    return render_template("products/edit.html", product=None)

@app.route("/products/edit/<product_id>", methods=["GET","POST"])
def edit_product(product_id):
    p = Product.query.get_or_404(product_id)
    if request.method == "POST":
        p.name = request.form["name"]
        p.description = request.form.get("description")
        db.session.commit()
        flash("Product updated")
        return redirect(url_for("list_products"))
    return render_template("products/edit.html", product=p)

@app.route("/products/delete/<product_id>", methods=["POST"])
def delete_product(product_id):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    flash("Product deleted")
    return redirect(url_for("list_products"))

# LOCATIONS
@app.route("/locations")
def list_locations():
    locations = Location.query.all()
    return render_template("locations/list.html", locations=locations)

@app.route("/locations/add", methods=["GET","POST"])
def add_location():
    if request.method == "POST":
        lid = request.form.get("location_id") or None
        name = request.form["name"]
        desc = request.form.get("description")
        loc = Location(location_id=lid, name=name, description=desc)
        db.session.add(loc); db.session.commit()
        flash("Location added")
        return redirect(url_for("list_locations"))
    return render_template("locations/edit.html", location=None)

@app.route("/locations/edit/<location_id>", methods=["GET","POST"])
def edit_location(location_id):
    loc = Location.query.get_or_404(location_id)
    if request.method == "POST":
        loc.name = request.form["name"]
        loc.description = request.form.get("description")
        db.session.commit()
        flash("Location updated")
        return redirect(url_for("list_locations"))
    return render_template("locations/edit.html", location=loc)

@app.route("/locations/delete/<location_id>", methods=["POST"])
def delete_location(location_id):
    loc = Location.query.get_or_404(location_id)
    db.session.delete(loc)
    db.session.commit()
    flash("Location deleted")
    return redirect(url_for("list_locations"))

# MOVEMENTS
@app.route("/movements")
def list_movements():
    moves = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    products = Product.query.all()
    locations = Location.query.all()
    return render_template("movements/list.html", moves=moves, products=products, locations=locations)

@app.route("/movements/add", methods=["GET","POST"])
def add_movement():
    if request.method == "POST":
        mid = request.form.get("movement_id") or None
        product_id = request.form["product_id"]
        qty = int(request.form["qty"])
        from_loc = request.form.get("from_location") or None
        to_loc = request.form.get("to_location") or None
        m = ProductMovement(movement_id=mid, from_location=from_loc, to_location=to_loc, product_id=product_id, qty=qty)
        db.session.add(m); db.session.commit()
        flash("Movement recorded")
        return redirect(url_for("list_movements"))
    products = Product.query.all()
    locations = Location.query.all()
    return render_template("movements/edit.html", products=products, locations=locations, move=None)

@app.route("/movements/delete/<movement_id>", methods=["POST"])
def delete_movement(movement_id):
    m = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(m)
    db.session.commit()
    flash("Movement deleted")
    return redirect(url_for("list_movements"))

# REPORT: balances
@app.route("/reports/balances")
def report_balances():
    # raw SQL using the logic described earlier:
    sql = """
    SELECT p.product_id, p.name as product_name,
           l.location_id, l.name as location_name,
           COALESCE(
             SUM(CASE WHEN pm.to_location = l.location_id THEN pm.qty ELSE 0 END) -
             SUM(CASE WHEN pm.from_location = l.location_id THEN pm.qty ELSE 0 END), 0
           ) AS balance
    FROM product p
    CROSS JOIN location l
    LEFT JOIN product_movement pm
      ON pm.product_id = p.product_id
      AND (pm.to_location = l.location_id OR pm.from_location = l.location_id)
    GROUP BY p.product_id, l.location_id
    ORDER BY p.product_id, l.location_id;
    """
    result = db.session.execute(text(sql))
    rows = result.fetchall()
    return render_template("reports/balances.html", rows=rows)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
# This block of code is the entry point for the Flask application. When the script is run directly, it creates the necessary database tables and starts the Flask development server with debugging enabled.
# This allows you to run the app locally for development and testing purposes.
# The create_tables function ensures that the database schema is set up before the app starts handling requests.
# The app.run(debug=True) line starts the Flask application with debugging features enabled, which is useful during development.
