"""
SQLAlchemy models for Puff n' Fleur.

Tables:
- User: admin accounts (registration + login)
- Package: service packages shown on the site (name, price, features) — editable from admin
- Booking: customer booking/inquiry submissions (the CRUD resource)
"""
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Package(db.Model):
    __tablename__ = "packages"

    id = db.Column(db.String(20), primary_key=True)  # e.g. "A", "B", "C", or a slug for new ones
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    delivery = db.Column(db.Boolean, nullable=False, default=True)
    image = db.Column(db.String(200), nullable=True)
    features_json = db.Column(db.Text, nullable=False, default="[]")  # JSON list of strings
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    @property
    def features(self):
        try:
            return json.loads(self.features_json or "[]")
        except (ValueError, TypeError):
            return []

    @features.setter
    def features(self, value):
        # Accepts a list of strings, or a single string with one feature per line
        if isinstance(value, str):
            value = [line.strip() for line in value.splitlines() if line.strip()]
        self.features_json = json.dumps(list(value or []))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price),
            "delivery": self.delivery,
            "image": self.image,
            "features": self.features,
            "sort_order": self.sort_order,
        }


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    event_type = db.Column(db.String(80), nullable=False)
    preferred_package = db.Column(db.String(20), nullable=True)
    custom_package_details = db.Column(db.Text, nullable=True)  # used when preferred_package == "Custom"
    event_date = db.Column(db.String(20), nullable=False)  # stored as text (form date input)
    event_location = db.Column(db.String(200), nullable=False)
    additional_notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="new")  # new, contacted, confirmed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "event_type": self.event_type,
            "preferred_package": self.preferred_package,
            "custom_package_details": self.custom_package_details,
            "event_date": self.event_date,
            "event_location": self.event_location,
            "additional_notes": self.additional_notes,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
