from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import os
import re
from pathlib import Path

import db

app = Flask(__name__)
app.secret_key = 'puffnfleur-secret-key-2024'

# Initialize the SQLite database (creates tables if they don't exist yet)
db.init_db()

EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def login_required(view_func):
    """Restrict a route to logged-in users only."""
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access that page.', 'error')
            return redirect(url_for('login', next=request.path))
        return view_func(*args, **kwargs)
    return wrapped

# Packages data
PACKAGES = [
    {
        'id': 'A',
        'name': 'Basic Package',
        'price': 350,
        'delivery': True,
        'image': 'package-a.jpg',
        'features': [
            'One Backdrop: color of your choice',
            'Balloon garland with up to 3 colors',
            'Customized Signage',
            'Bear or 3ft-4ft Character Cutouts',
            'With or Without Cake stand',
            'Baby Box'
        ]
    },
    {
        'id': 'B',
        'name': 'Standard Package',
        'price': 500,
        'delivery': True,
        'image': 'package-b.jpg',
        'features': [
            'Two Backdrop: color of your choice',
            'Balloon garland with up to 3 colors',
            'Customized Signage',
            'Bear or 3ft-4ft Character Cutouts',
            'With or Without Cake Stand',
            'Baby Box'
        ]
    },
    {
        'id': 'C',
        'name': 'Deluxe Package',
        'price': 800,
        'delivery': True,
        'image': 'package-c.jpg',
        'features': [
            '3 Premium Backdrop: color of your choice',
            'Balloon garland with up to 4 colors',
            'Customized Signage',
            'Bear or 3ft-4ft Character Cutouts',
            'Cake Stand',
            'Baby Box',
            '#1 Marquee Standee'
        ]
    }
]

# Testimonials data
TESTIMONIALS = [
    {
        'name': 'Sarah M.',
        'event': 'Birthday Party',
        'text': 'Puff n\' Fleur transformed our daughter\'s party into a magical experience. The attention to detail was incredible!',
        'rating': 5
    },
    {
        'name': 'Jessica K.',
        'event': 'Baby Shower',
        'text': 'Absolutely loved the floral arrangements. They were elegant, beautiful, and perfectly tailored to our vision.',
        'rating': 5
    },
    {
        'name': 'Michael T.',
        'event': 'Corporate Event',
        'text': 'Professional service from start to finish. Highly recommended for any event needs!',
        'rating': 5
    }
]

# Ensure bookings CSV exists
BOOKINGS_FILE = 'bookings.csv'

def ensure_bookings_file():
    """Create bookings.csv with headers if it doesn't exist."""
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Timestamp', 'Full Name', 'Email', 'Phone', 'Event Type', 
                'Preferred Package', 'Event Date', 'Event Location', 'Additional Notes'
            ])

ensure_bookings_file()


@app.context_processor
def inject_user():
    """Make the logged-in user's info available to every template."""
    return {
        'current_user_name': session.get('user_name'),
        'current_user_id': session.get('user_id')
    }


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register page - creates a new user record in the database."""
    if request.method == 'GET':
        return render_template('auth.html', active_tab='register')

    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    # Required field validation
    if not all([full_name, email, password, confirm_password]):
        flash('Please fill in all required fields.', 'error')
        return render_template('auth.html', active_tab='register', reg_full_name=full_name, reg_email=email)

    if not EMAIL_REGEX.match(email):
        flash('Please enter a valid email address.', 'error')
        return render_template('auth.html', active_tab='register', reg_full_name=full_name, reg_email=email)

    if len(password) < 6:
        flash('Password must be at least 6 characters long.', 'error')
        return render_template('auth.html', active_tab='register', reg_full_name=full_name, reg_email=email)

    if password != confirm_password:
        flash('Passwords do not match.', 'error')
        return render_template('auth.html', active_tab='register', reg_full_name=full_name, reg_email=email)

    if db.get_user_by_email(email) is not None:
        flash('An account with that email already exists. Please log in instead.', 'error')
        return render_template('auth.html', active_tab='login', login_email=email)

    password_hash = generate_password_hash(password)
    user_id = db.create_user(full_name, email, password_hash)

    # Log the new user in right away
    session['user_id'] = user_id
    session['user_name'] = full_name

    flash('Account created successfully! Welcome to Puff n\' Fleur.', 'success')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page - checks credentials against the users table."""
    if request.method == 'GET':
        return render_template('auth.html', active_tab='login')

    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    if not all([email, password]):
        flash('Please enter both email and password.', 'error')
        return render_template('auth.html', active_tab='login', login_email=email)

    user = db.get_user_by_email(email)
    if user is None or not check_password_hash(user['password_hash'], password):
        flash('Invalid email or password.', 'error')
        return render_template('auth.html', active_tab='login', login_email=email)

    session['user_id'] = user['id']
    session['user_name'] = user['full_name']

    flash(f'Welcome back, {user["full_name"]}!', 'success')
    next_page = request.args.get('next')
    return redirect(next_page or url_for('index'))


@app.route('/logout')
def logout():
    """Clear the session and log the user out."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/admin/bookings')
@login_required
def admin_bookings():
    """Read page - displays all booking records pulled from the database."""
    bookings = db.get_all_bookings()
    return render_template('admin_bookings.html', bookings=bookings)


@app.route('/')
def index():
    """Home page with hero, intro, packages preview, and testimonials."""
    featured_packages = PACKAGES[:3]
    testimonials = TESTIMONIALS
    return render_template('index.html', packages=featured_packages, testimonials=testimonials)

@app.route('/packages')
def packages():
    """Display all packages."""
    return render_template('packages.html', packages=PACKAGES)

@app.route('/gallery')
def gallery():
    """Display gallery with placeholder images."""
    # Placeholder gallery items
    gallery_items = [
        {'id': 1, 'title': 'Birthday Celebration', 'category': 'birthdays', 'image': 'gallery-1.jpg'},
        {'id': 2, 'title': 'Baby Shower Bliss', 'category': 'baby-showers', 'image': 'gallery-2.jpg'},
        {'id': 3, 'title': 'Wedding Elegance', 'category': 'weddings', 'image': 'gallery-3.jpg'},
        {'id': 4, 'title': 'Corporate Event', 'category': 'corporate', 'image': 'gallery-4.jpg'},
        {'id': 5, 'title': 'Party Perfection', 'category': 'birthdays', 'image': 'gallery-5.jpg'},
        {'id': 6, 'title': 'Shower Magic', 'category': 'baby-showers', 'image': 'gallery-6.jpg'},
        {'id': 7, 'title': 'Special Occasion', 'category': 'other', 'image': 'gallery-7.jpg'},
        {'id': 8, 'title': 'Dream Setup', 'category': 'weddings', 'image': 'gallery-8.jpg'},
    ]
    return render_template('gallery.html', gallery_items=gallery_items)

@app.route('/contact', methods=['GET'])
def contact():
    """Display contact/booking form."""
    return render_template('contact.html', packages=PACKAGES)

@app.route('/contact', methods=['POST'])
def submit_booking():
    """Handle booking form submission."""
    try:
        # Get form data
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        event_type = request.form.get('event_type', '').strip()
        preferred_package = request.form.get('preferred_package', '').strip()
        event_date = request.form.get('event_date', '').strip()
        event_location = request.form.get('event_location', '').strip()
        additional_notes = request.form.get('additional_notes', '').strip()
        
        # Validate required fields
        if not all([full_name, email, phone, event_type, event_date, event_location]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('contact'))
        
        # Save to the database (bookings table)
        db.create_booking({
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'event_type': event_type,
            'preferred_package': preferred_package,
            'event_date': event_date,
            'event_location': event_location,
            'additional_notes': additional_notes,
        }, user_id=session.get('user_id'))

        # Also keep a CSV copy for easy exporting
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(BOOKINGS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, full_name, email, phone, event_type,
                preferred_package, event_date, event_location, additional_notes
            ])
        
        flash('Thank you! We\'ll be in touch within 24–48 hours.', 'success')
        return redirect(url_for('contact'))
    
    except Exception as e:
        app.logger.error(f"Booking submission error: {str(e)}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('contact'))

@app.template_filter('format_phone')
def format_phone(phone):
    """Format phone number for display."""
    if not phone:
        return ''
    # Simple formatting: (XXX) XXX-XXXX
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
