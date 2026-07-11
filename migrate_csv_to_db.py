"""
One-time migration: load rows from the old bookings.csv into the database.

Usage:
    python migrate_csv_to_db.py [path/to/bookings.csv]

Run this once after switching to the database backend, if you have
existing booking data in bookings.csv you want to keep.
"""
import csv
import sys

from app import app
from models import db, Booking


def migrate(csv_path="bookings.csv"):
    with app.app_context():
        db.create_all()
        added = 0
        with open(csv_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                booking = Booking(
                    full_name=row.get("Full Name", "").strip(),
                    email=row.get("Email", "").strip(),
                    phone=row.get("Phone", "").strip(),
                    event_type=row.get("Event Type", "").strip(),
                    preferred_package=(row.get("Preferred Package") or "").strip() or None,
                    event_date=row.get("Event Date", "").strip(),
                    event_location=row.get("Event Location", "").strip(),
                    additional_notes=(row.get("Additional Notes") or "").strip() or None,
                )
                db.session.add(booking)
                added += 1
        db.session.commit()
        print(f"Migrated {added} bookings from {csv_path} into the database.")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "bookings.csv"
    migrate(path)
