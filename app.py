import os
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from dotenv import load_dotenv

from models import db, User, Booking, Package

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "puffnfleur-dev-secret-change-me")

# --- Database configuration -------------------------------------------------
# Set DATABASE_URL to point at PostgreSQL or MySQL, e.g.:
#   postgresql://user:password@localhost:5432/puffnfleur
#   mysql+pymysql://user:password@localhost:3306/puffnfleur
# Falls back to a local SQLite file if DATABASE_URL isn't set, so the app
# still runs out of the box for quick testing.
db_url = os.environ.get("DATABASE_URL", "sqlite:///puffnfleur.db")
if db_url.startswith("postgres://"):  # Heroku-style URLs need the +psycopg2 dialect
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    # Seed default packages once, the first time the app runs against an
    # empty database. After that, prices/features are managed from /admin.
    if Package.query.count() == 0:
        defaults = [
            {
                "id": "A", "name": "Basic", "price": 270, "delivery": True, "image": "basic.jpg",
                "sort_order": 1,
                "features": [
                    "One Backdrop (color of your choice)",
                    "Balloon garland with up to 3 colors",
                    "Custom Happy Birthday Vinyl or LED sign",
                ],
            },
            {
                "id": "B", "name": "Standard", "price": 330, "delivery": True, "image": "standard.jfif",
                "sort_order": 2,
                "features": [
                    "Two Arch Backdrop (color of your choice)",
                    "Balloon garland with up to 3 colors",
                    "Custom Happy Birthday Vinyl or LED sign",
                ],
            },
            {
                "id": "C", "name": "Deluxe", "price": 300, "delivery": True, "image": "deluxe.png",
                "sort_order": 3,
                "features": [
                    "One Backdrop (color of your choice)",
                    "Balloon garland with up to 3 colors",
                    "Custom Happy Birthday Vinyl or LED sign",
                    "One character prop (3ft-4ft)",
                    "+$50 for additional backdrop",
                ],
            },
        ]
        for d in defaults:
            pkg = Package(id=d["id"], name=d["name"], price=d["price"],
                           delivery=d["delivery"], image=d["image"], sort_order=d["sort_order"])
            pkg.features = d["features"]
            db.session.add(pkg)
        db.session.commit()


def get_packages():
    """Returns packages from the DB as plain dicts, shaped like the old
    hardcoded PACKAGES list so existing templates keep working unchanged."""
    packages = Package.query.order_by(Package.sort_order, Package.id).all()
    return [p.to_dict() for p in packages]


def login_required_page(f):
    """Guards server-rendered pages: redirects to /admin (SPA shows login)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("admin_spa"))
        return f(*args, **kwargs)
    return decorated


def login_required_api(f):
    """Guards JSON API routes: returns 401 instead of redirecting."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Not authenticated"}), 401
        return f(*args, **kwargs)
    return decorated


TESTIMONIALS = [
    {"name": "Sarah M.", "event": "Birthday Party",
     "text": "Puff n' Fleur transformed our daughter's party into a magical experience. The attention to detail was incredible!",
     "rating": 5},
    {"name": "Jessica K.", "event": "Baby Shower",
     "text": "Absolutely loved the floral arrangements. They were elegant, beautiful, and perfectly tailored to our vision.",
     "rating": 5},
    {"name": "Michael T.", "event": "Corporate Event",
     "text": "Professional service from start to finish. Highly recommended for any event needs!",
     "rating": 5},
]


# ---------------------------------------------------------------------------
# Public marketing pages
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", packages=get_packages()[:3], testimonials=TESTIMONIALS)


@app.route("/packages")
def packages():
    return render_template("packages.html", packages=get_packages())


@app.route("/gallery")
def gallery():
    gallery_items = [
        {"id": 1, "title": "Birthday Celebration", "category": "birthdays", "image": "gallery-1.jpg"},
        {"id": 2, "title": "Baby Shower Bliss", "category": "baby-showers", "image": "gallery-2.jpg"},
        {"id": 3, "title": "Wedding Elegance", "category": "weddings", "image": "gallery-3.jpg"},
        {"id": 4, "title": "Corporate Event", "category": "corporate", "image": "gallery-4.jpg"},
        {"id": 5, "title": "Party Perfection", "category": "birthdays", "image": "gallery-5.jpg"},
        {"id": 6, "title": "Shower Magic", "category": "baby-showers", "image": "gallery-6.jpg"},
        {"id": 7, "title": "Special Occasion", "category": "other", "image": "gallery-7.jpg"},
        {"id": 8, "title": "Dream Setup", "category": "weddings", "image": "gallery-8.jpg"},
    ]
    return render_template("gallery.html", gallery_items=gallery_items)


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html", packages=get_packages())


@app.route("/contact", methods=["POST"])
def submit_booking():
    """Public booking form -> now persists to the database instead of CSV."""
    try:
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        event_type = request.form.get("event_type", "").strip()
        preferred_package = request.form.get("preferred_package", "").strip()
        custom_package_details = request.form.get("custom_package_details", "").strip()
        event_date = request.form.get("event_date", "").strip()
        event_location = request.form.get("event_location", "").strip()
        additional_notes = request.form.get("additional_notes", "").strip()

        if not all([full_name, email, phone, event_type, event_date, event_location]):
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("contact"))

        booking = Booking(
            full_name=full_name,
            email=email,
            phone=phone,
            event_type=event_type,
            preferred_package=preferred_package or None,
            custom_package_details=custom_package_details or None,
            event_date=event_date,
            event_location=event_location,
            additional_notes=additional_notes or None,
        )
        db.session.add(booking)
        db.session.commit()

        flash("Thank you! We'll be in touch within 24-48 hours.", "success")
        return redirect(url_for("contact"))

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Booking submission error: {str(e)}")
        flash("An error occurred. Please try again.", "error")
        return redirect(url_for("contact"))


# ---------------------------------------------------------------------------
# Admin SPA shell (Vue.js) — login, registration, and bookings CRUD all live
# client-side here and talk to the JSON API below.
# ---------------------------------------------------------------------------
@app.route("/admin")
def admin_spa():
    return render_template("admin_spa.html")


# ---------------------------------------------------------------------------
# Auth API
# ---------------------------------------------------------------------------
@app.route("/api/auth/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are all required."}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters."}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "That username is already taken."}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "That email is already registered."}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id
    return jsonify({"user": user.to_dict()}), 201


@app.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password."}), 401

    session["user_id"] = user.id
    return jsonify({"user": user.to_dict()})


@app.route("/api/auth/logout", methods=["POST"])
def api_logout():
    session.pop("user_id", None)
    return jsonify({"ok": True})


@app.route("/api/auth/me")
def api_me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"user": None})
    user = db.session.get(User, user_id)
    if not user:
        session.pop("user_id", None)
        return jsonify({"user": None})
    return jsonify({"user": user.to_dict()})


# ---------------------------------------------------------------------------
# Packages CRUD API (protected) — lets admins edit prices/features, and add
# brand-new custom packages beyond the original A/B/C.
# ---------------------------------------------------------------------------
@app.route("/api/packages", methods=["GET"])
@login_required_api
def api_packages_list():
    return jsonify({"packages": get_packages()})


@app.route("/api/packages", methods=["POST"])
@login_required_api
def api_packages_create():
    data = request.get_json(silent=True) or {}
    pkg_id = (data.get("id") or "").strip()
    name = (data.get("name") or "").strip()

    if not pkg_id or not name:
        return jsonify({"error": "Package id and name are required."}), 400
    if db.session.get(Package, pkg_id):
        return jsonify({"error": f"A package with id '{pkg_id}' already exists."}), 409

    try:
        price = float(data.get("price", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Price must be a number."}), 400

    max_order = db.session.query(db.func.max(Package.sort_order)).scalar() or 0
    pkg = Package(
        id=pkg_id,
        name=name,
        price=price,
        delivery=bool(data.get("delivery", True)),
        image=(data.get("image") or "").strip() or None,
        sort_order=max_order + 1,
    )
    pkg.features = data.get("features") or []
    db.session.add(pkg)
    db.session.commit()
    return jsonify({"package": pkg.to_dict()}), 201


@app.route("/api/packages/<pkg_id>", methods=["PUT"])
@login_required_api
def api_packages_update(pkg_id):
    pkg = db.session.get(Package, pkg_id)
    if not pkg:
        return jsonify({"error": "Package not found."}), 404

    data = request.get_json(silent=True) or {}
    if "name" in data:
        pkg.name = (data["name"] or "").strip() or pkg.name
    if "price" in data:
        try:
            pkg.price = float(data["price"])
        except (TypeError, ValueError):
            return jsonify({"error": "Price must be a number."}), 400
    if "delivery" in data:
        pkg.delivery = bool(data["delivery"])
    if "image" in data:
        pkg.image = (data["image"] or "").strip() or None
    if "features" in data:
        pkg.features = data["features"] or []
    if "sort_order" in data:
        try:
            pkg.sort_order = int(data["sort_order"])
        except (TypeError, ValueError):
            pass

    db.session.commit()
    return jsonify({"package": pkg.to_dict()})


@app.route("/api/packages/<pkg_id>", methods=["DELETE"])
@login_required_api
def api_packages_delete(pkg_id):
    pkg = db.session.get(Package, pkg_id)
    if not pkg:
        return jsonify({"error": "Package not found."}), 404
    db.session.delete(pkg)
    db.session.commit()
    return jsonify({"ok": True})


# ---------------------------------------------------------------------------
# Bookings CRUD API (protected)
# ---------------------------------------------------------------------------
@app.route("/api/bookings", methods=["GET"])
@login_required_api
def api_bookings_list():
    query = Booking.query

    search = request.args.get("search", "").strip().lower()
    event_filter = request.args.get("event_type", "").strip()
    package_filter = request.args.get("package", "").strip()

    bookings = query.order_by(Booking.created_at.desc()).all()

    if search:
        bookings = [
            b for b in bookings
            if search in b.full_name.lower() or search in b.email.lower() or search in b.event_location.lower()
        ]
    if event_filter:
        bookings = [b for b in bookings if b.event_type == event_filter]
    if package_filter:
        bookings = [b for b in bookings if (b.preferred_package or "") == package_filter]

    all_bookings = Booking.query.all()
    event_counts, package_counts = {}, {}
    for b in all_bookings:
        event_counts[b.event_type] = event_counts.get(b.event_type, 0) + 1
        pkg = b.preferred_package or "Not Selected"
        package_counts[pkg] = package_counts.get(pkg, 0) + 1

    return jsonify({
        "bookings": [b.to_dict() for b in bookings],
        "total": len(all_bookings),
        "event_counts": event_counts,
        "package_counts": package_counts,
    })


@app.route("/api/bookings", methods=["POST"])
@login_required_api
def api_bookings_create():
    data = request.get_json(silent=True) or {}
    required = ["full_name", "email", "phone", "event_type", "event_date", "event_location"]
    missing = [f for f in required if not (data.get(f) or "").strip()]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    booking = Booking(
        full_name=data["full_name"].strip(),
        email=data["email"].strip(),
        phone=data["phone"].strip(),
        event_type=data["event_type"].strip(),
        preferred_package=(data.get("preferred_package") or "").strip() or None,
        custom_package_details=(data.get("custom_package_details") or "").strip() or None,
        event_date=data["event_date"].strip(),
        event_location=data["event_location"].strip(),
        additional_notes=(data.get("additional_notes") or "").strip() or None,
        status=(data.get("status") or "new").strip(),
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({"booking": booking.to_dict()}), 201


@app.route("/api/bookings/<int:booking_id>", methods=["GET"])
@login_required_api
def api_bookings_get(booking_id):
    booking = db.session.get(Booking, booking_id)
    if not booking:
        return jsonify({"error": "Booking not found."}), 404
    return jsonify({"booking": booking.to_dict()})


@app.route("/api/bookings/<int:booking_id>", methods=["PUT"])
@login_required_api
def api_bookings_update(booking_id):
    booking = db.session.get(Booking, booking_id)
    if not booking:
        return jsonify({"error": "Booking not found."}), 404

    data = request.get_json(silent=True) or {}
    for field in ["full_name", "email", "phone", "event_type", "event_date",
                  "event_location", "additional_notes", "preferred_package",
                  "custom_package_details", "status"]:
        if field in data:
            value = (data[field] or "").strip()
            setattr(booking, field, value or None)

    db.session.commit()
    return jsonify({"booking": booking.to_dict()})


@app.route("/api/bookings/<int:booking_id>", methods=["DELETE"])
@login_required_api
def api_bookings_delete(booking_id):
    booking = db.session.get(Booking, booking_id)
    if not booking:
        return jsonify({"error": "Booking not found."}), 404
    db.session.delete(booking)
    db.session.commit()
    return jsonify({"ok": True})


@app.template_filter("format_phone")
def format_phone(phone):
    if not phone:
        return ""
    digits = "".join(filter(str.isdigit, phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
