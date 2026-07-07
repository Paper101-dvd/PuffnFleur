"""
db.py - SQLite database layer for Puff n' Fleur

Handles connection management and schema creation for two tables:
  - users:    stores registered accounts (Login/Register page)
  - bookings: stores booking requests submitted via the Contact page
              (this is the CRUD "entity" the admin Read page displays)
"""

import sqlite3
import os
from pathlib import Path

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'puffnfleur.db')


def get_db():
    """Return a new SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    """Create tables if they do not already exist."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            event_type TEXT NOT NULL,
            preferred_package TEXT,
            event_date TEXT NOT NULL,
            event_location TEXT NOT NULL,
            additional_notes TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
        )
    ''')

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------
# User helpers
# ---------------------------------------------------------------------

def get_user_by_email(email):
    conn = get_db()
    row = conn.execute('SELECT * FROM users WHERE email = ?', (email.lower(),)).fetchone()
    conn.close()
    return row


def get_user_by_id(user_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return row


def create_user(full_name, email, password_hash):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)',
        (full_name, email.lower(), password_hash)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


# ---------------------------------------------------------------------
# Booking helpers
# ---------------------------------------------------------------------

def create_booking(data, user_id=None):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO bookings
            (user_id, full_name, email, phone, event_type, preferred_package,
             event_date, event_location, additional_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        data.get('full_name'),
        data.get('email'),
        data.get('phone'),
        data.get('event_type'),
        data.get('preferred_package'),
        data.get('event_date'),
        data.get('event_location'),
        data.get('additional_notes'),
    ))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_all_bookings():
    conn = get_db()
    rows = conn.execute('SELECT * FROM bookings ORDER BY created_at DESC').fetchall()
    conn.close()
    return rows
