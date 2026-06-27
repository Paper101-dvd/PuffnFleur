from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import csv
import os
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'puffnfleur-secret-key-2024'

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
