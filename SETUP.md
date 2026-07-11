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

### Step 4: Configure the Database
This project is configured for **MySQL**. The `.env` file already included in this zip points at a local MySQL database — you just need to create that database and user on your own machine.

**Install MySQL** if you don't have it:
- Windows/Mac: [MySQL Community Server](https://dev.mysql.com/downloads/mysql/) or use XAMPP/WAMP
- Linux: `sudo apt install mysql-server`

**Create the database and user** (run in a MySQL shell, e.g. `mysql -u root -p`):
```sql
CREATE DATABASE puffnfleur CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'puffnfleur_user'@'localhost' IDENTIFIED BY 'PuffnFleur2026!';
GRANT ALL PRIVILEGES ON puffnfleur.* TO 'puffnfleur_user'@'localhost';
FLUSH PRIVILEGES;
```

This matches the `DATABASE_URL` already in `.env`:
```
DATABASE_URL=mysql+pymysql://puffnfleur_user:PuffnFleur2026!@localhost:3306/puffnfleur
```
Change the username/password/host in both places if you'd rather use different credentials. Flask creates the `users` and `bookings` tables automatically the first time you run the app — no manual `CREATE TABLE` needed.

**Migrating old CSV bookings (optional):** if you have a `bookings.csv.legacy` file with old submissions, import it once with:
```bash
python migrate_csv_to_db.py bookings.csv.legacy
```

### Step 5: Run the Application
```bash
python app.py
```

### Step 6: Open in Browser
- Public site: **http://localhost:5000**
- Admin (Register / Login / Bookings CRUD): **http://localhost:5000/admin**

---

## Project Structure Overview

```
puffnfleur/
├── app.py                    ← Flask application (routes + JSON API)
├── models.py                 ← SQLAlchemy models (User, Booking)
├── migrate_csv_to_db.py      ← One-time CSV -> database import script
├── requirements.txt          ← Python dependencies
├── bookings.csv.legacy       ← Old CSV data (pre-database), for migration only
├── setup.bat                 ← Windows setup script
├── setup.sh                  ← macOS/Linux setup script
├── .env.example               ← Environment variables template (incl. DATABASE_URL)
├── .gitignore                ← Git ignore file
├── README.md                  ← Full documentation
├── SETUP.md                  ← This file
│
├── static/
│   ├── css/
│   │   ├── style.css         ← Main site stylesheet
│   │   └── admin.css         ← Admin SPA stylesheet
│   ├── js/
│   │   ├── main.js           ← Public site JavaScript
│   │   └── admin-app.js      ← Vue.js admin app (login, register, bookings CRUD)
│   └── images/               ← Place images here
│
└── templates/
    ├── base.html             ← Base template (public site)
    ├── index.html            ← Home page
    ├── packages.html         ← Service packages
    ├── gallery.html          ← Event gallery
    ├── contact.html          ← Contact & booking form
    └── admin_spa.html        ← Admin SPA shell (mounts the Vue app)
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

## Form Submissions & Admin CRUD

Booking form submissions are saved to the database (`bookings` table) with:
- Timestamp
- Customer name, email, phone
- Event details (type, date, location)
- Package preference
- Special requests
- Status (new / contacted / confirmed / cancelled)

Visit **http://localhost:5000/admin** to register an admin account, log in, and manage bookings — create new ones manually, edit existing ones (including status), search/filter, and delete. This is the CRUD page for the project.

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
