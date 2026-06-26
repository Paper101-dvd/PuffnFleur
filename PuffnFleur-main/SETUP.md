# SETUP INSTRUCTIONS - Puff n' Fleur

## Quick Start Guide

### Step 1: Navigate to the Project Directory
```bash
cd puffnfleur
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**OR use the automated setup script:**
- **Windows**: Double-click `setup.bat`
- **macOS/Linux**: Run `bash setup.sh`

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Open in Browser
Navigate to: **http://localhost:5000**

---

## Project Structure Overview

```
puffnfleur/
├── app.py                 ← Flask application (main entry point)
├── requirements.txt       ← Python dependencies
├── bookings.csv          ← Booking submissions (auto-generated)
├── setup.bat             ← Windows setup script
├── setup.sh              ← macOS/Linux setup script
├── .env.example          ← Environment variables template
├── .gitignore            ← Git ignore file
├── README.md             ← Full documentation
├── SETUP.md              ← This file
│
├── .vscode/
│   └── settings.json     ← VS Code configuration
│
├── static/
│   ├── css/
│   │   └── style.css     ← Main stylesheet
│   ├── js/
│   │   └── main.js       ← JavaScript interactivity
│   └── images/           ← Place images here
│
└── templates/
    ├── base.html         ← Base template
    ├── index.html        ← Home page
    ├── packages.html     ← Service packages
    ├── gallery.html      ← Event gallery
    └── contact.html      ← Contact & booking form
```

---

## Available Pages

| Page | URL | Purpose |
|------|-----|---------|
| Home | http://localhost:5000/ | Hero, intro, featured packages, testimonials |
| Packages | http://localhost:5000/packages | All packages, comparison table, add-ons |
| Gallery | http://localhost:5000/gallery | Event photos with category filters |
| Contact | http://localhost:5000/contact | Booking form, FAQ, contact info |

---

## Adding Images

1. Place your images in `static/images/`
2. Update image references in:
   - `app.py` (PACKAGES data)
   - `templates/gallery.html` (gallery items)

Example image files to add:
- `package-a.jpg`, `package-b.jpg`, `package-c.jpg` (package images)
- `gallery-1.jpg` through `gallery-8.jpg` (gallery images)

---

## Business Information (Edit These)

Edit the following files to update business details:

### Contact Information
- **File**: `templates/base.html` and `templates/contact.html`
- **Update**: Phone, email, location, social links

### Service Packages
- **File**: `app.py`
- **Update**: PACKAGES list (names, prices, features)

### Colors & Branding
- **File**: `static/css/style.css`
- **Update**: CSS variables in `:root` selector

---

## Customization Examples

### Change Primary Color
Edit `static/css/style.css`:
```css
:root {
    --color-primary: #C47A8A;  /* Change this */
}
```

### Add a New Package
Edit `app.py` in the PACKAGES list:
```python
{
    'id': 'D',
    'name': 'Package D',
    'price': 400,
    'delivery': True,
    'image': 'package-d.jpg',
    'features': [
        'Feature 1',
        'Feature 2',
        'Feature 3'
    ]
}
```

### Update Testimonials
Edit `app.py` in the TESTIMONIALS list:
```python
{
    'name': 'Your Client',
    'event': 'Event Type',
    'text': 'Your testimonial here',
    'rating': 5
}
```

---

## Form Submissions

All booking form submissions are saved to `bookings.csv` with:
- Timestamp
- Customer name, email, phone
- Event details (type, date, location)
- Package preference
- Special requests

You can open `bookings.csv` with:
- Excel
- Google Sheets
- Any text editor
- Python scripts for processing

---

## Troubleshooting

### Port 5000 Already in Use
```bash
# Use a different port
python app.py  # Add --port 5001 if supported
```

### Python Not Found
```bash
# Try using python3 instead
python3 app.py
```

### Module Not Found Error
```bash
# Make sure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

### Images Not Loading
1. Check files are in `static/images/`
2. Verify filenames match exactly
3. Check file permissions

---

## Optional: Email Notifications

To enable email notifications for new bookings:

1. Copy `.env.example` to `.env`
2. Fill in your email settings
3. Uncomment Flask-Mail code in `app.py`

---

## Deployment

For production deployment, see `README.md` for detailed instructions on hosting platforms like Heroku, PythonAnywhere, AWS, etc.

---

## Support

**Business Contact:**
- 📞 Phone: (943) 266-0114
- ✉️ Email: Puffnfleur@gmail.com
- 📍 Location: Acworth, Georgia USA
- 📷 Instagram: @Puff_n_Fleur
- 👍 Facebook: Puff n' Fleur

---

**Ready to serve your customers! 🎈**
