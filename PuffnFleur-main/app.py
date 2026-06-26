from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from datetime import datetime
import csv
import os
from pathlib import Path
from functools import wraps

app = Flask(__name__)
app.secret_key = 'puffnfleur-secret-key-2024'

# Admin credentials — change these!
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'puffnfleur2024'

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# Packages data
PACKAGES = [
    {
        'id': 'A',
        'name': 'Package A',
        'price': 270,
        'delivery': True,
        'image': 'package-a.jpg',
        'features': [
            'One Backdrop (color of your choice)',
            'Balloon garland with up to 3 colors',
            'Custom Happy Birthday Vinyl or LED sign'
        ]
    },
    {
        'id': 'B',
        'name': 'Package B',
        'price': 330,
        'delivery': True,
        'image': 'package-b.jpg',
        'features': [
            'Two Arch Backdrop (color of your choice)',
            'Balloon garland with up to 3 colors',
            'Custom Happy Birthday Vinyl or LED sign'
        ]
    },
    {
        'id': 'C',
        'name': 'Package C',
        'price': 300,
        'delivery': True,
        'image': 'package-c.jpg',
        'features': [
            'One Backdrop (color of your choice)',
            'Balloon garland with up to 3 colors',
            'Custom Happy Birthday Vinyl or LED sign',
            'One character prop (3ft–4ft)',
            '+$50 for additional backdrop'
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
        
        # Save to CSV
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

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    bookings = []
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bookings.append(row)

    # Sort newest first
    bookings.sort(key=lambda x: x.get('Timestamp', ''), reverse=True)

    # Stats
    total = len(bookings)
    event_counts = {}
    package_counts = {}
    for b in bookings:
        et = b.get('Event Type', 'Unknown')
        event_counts[et] = event_counts.get(et, 0) + 1
        pkg = b.get('Preferred Package', '') or 'Not Selected'
        package_counts[pkg] = package_counts.get(pkg, 0) + 1

    # Search/filter
    search = request.args.get('search', '').lower()
    event_filter = request.args.get('event_type', '')
    package_filter = request.args.get('package', '')

    filtered = bookings
    if search:
        filtered = [b for b in filtered if
                    search in b.get('Full Name', '').lower() or
                    search in b.get('Email', '').lower() or
                    search in b.get('Event Location', '').lower()]
    if event_filter:
        filtered = [b for b in filtered if b.get('Event Type') == event_filter]
    if package_filter:
        filtered = [b for b in filtered if b.get('Preferred Package') == package_filter]

    return render_template('admin_dashboard.html',
                           bookings=filtered,
                           total=total,
                           event_counts=event_counts,
                           package_counts=package_counts,
                           search=search,
                           event_filter=event_filter,
                           package_filter=package_filter,
                           event_types=list(event_counts.keys()),
                           package_types=list(package_counts.keys()))

@app.route('/admin/delete/<int:index>', methods=['POST'])
@login_required
def admin_delete(index):
    bookings = []
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            bookings = list(reader)

    if 0 <= index < len(bookings):
        bookings.sort(key=lambda x: x.get('Timestamp', ''), reverse=True)
        bookings.pop(index)
        bookings.sort(key=lambda x: x.get('Timestamp', ''))
        with open(BOOKINGS_FILE, 'w', newline='') as f:
            fieldnames = ['Timestamp', 'Full Name', 'Email', 'Phone', 'Event Type',
                          'Preferred Package', 'Event Date', 'Event Location', 'Additional Notes']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(bookings)
        flash('Booking deleted.', 'success')
    else:
        flash('Booking not found.', 'error')
    return redirect(url_for('admin_dashboard'))

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
