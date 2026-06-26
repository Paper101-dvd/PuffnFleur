# Puff n' Fleur - Balloon Styling & Event Planning

**Where Balloons Meet Blooms** 🎈

A beautiful Flask web application for a professional balloon styling and event planning business based in Acworth, Georgia, USA.

## 🌸 About

Puff n' Fleur is a modern, responsive website that allows visitors to:
- Browse service packages and pricing
- Explore a gallery of past events
- Submit booking and inquiry requests
- Contact the business directly

## 📋 Features

- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Modern Aesthetic**: Soft, elegant, feminine design with custom brand colors
- **Service Packages**: Display of 3 curated packages (A, B, C) with full feature lists
- **Gallery**: Filterable image gallery with categories (Birthdays, Baby Showers, Weddings, Corporate, Other)
- **Booking System**: Complete inquiry form that saves submissions to CSV
- **Contact Info**: Multiple contact methods (Phone, Email, Social Media, WhatsApp)
- **FAQ Section**: Common questions answered on the contact page
- **Floating Action Buttons**: Quick access to WhatsApp and phone call
- **Back-to-Top Button**: Easy navigation for users on long pages
- **SEO Meta Tags**: Optimized for search engines

## 🎨 Brand Colors

- **Background**: #FDE8EF (soft blush pink)
- **Primary Accent**: #C47A8A (dusty rose)
- **Secondary Accent**: #A8C5A0 (sage green)
- **Text**: #2C2C2C (charcoal)
- **White**: #FFFFFF

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**:
   ```bash
   cd puffnfleur
   ```

2. **Create a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open in browser**:
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
puffnfleur/
├── venv/                    # Python virtual environment
├── app.py                   # Flask app entry point and routes
├── requirements.txt         # Python dependencies
├── bookings.csv            # Booking submissions (auto-generated)
├── .vscode/
│   └── settings.json       # VS Code settings
├── static/
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   ├── js/
│   │   └── main.js         # JavaScript interactivity
│   └── images/             # Image assets
├── templates/
│   ├── base.html           # Base template (extends to all pages)
│   ├── index.html          # Home page
│   ├── packages.html       # Service packages page
│   ├── gallery.html        # Gallery page
│   └── contact.html        # Contact & booking page
└── README.md               # This file
```

## 📄 Pages

### Home (/)
- Hero section with tagline and CTA
- Business introduction
- Featured packages preview
- Client testimonials
- Call-to-action section

### Packages (/packages)
- All 3 packages displayed as elegant cards
- Package comparison table
- Custom options and add-ons
- "Inquire Now" buttons linking to contact form

### Gallery (/gallery)
- Masonry grid layout (responsive)
- Filterable by event type:
  - All
  - Birthdays
  - Baby Showers
  - Weddings
  - Corporate
  - Other
- Hover effects and image overlays

### Contact & Booking (/contact)
- Inquiry form with fields:
  - Full Name (required)
  - Email Address (required)
  - Phone Number (required)
  - Event Type (required)
  - Preferred Package (optional)
  - Event Date (required)
  - Event Location (required)
  - Additional Notes (optional)
- Form validation (client-side and server-side)
- Success/error messages
- Contact information and social links
- FAQ accordion section

## 🛠️ Flask Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/packages` | GET | Service packages |
| `/gallery` | GET | Event gallery |
| `/contact` | GET | Booking form display |
| `/contact` | POST | Handle form submission, save to CSV |

## 💾 Booking Data

Booking form submissions are automatically saved to `bookings.csv` with the following fields:
- Timestamp
- Full Name
- Email
- Phone
- Event Type
- Preferred Package
- Event Date
- Event Location
- Additional Notes

## 🎯 Business Information

**Puff n' Fleur**
- **Phone**: (943) 266-0114
- **Email**: Puffnfleur@gmail.com
- **Location**: Acworth, Georgia USA
- **Instagram**: @Puff_n_Fleur
- **Facebook**: Puff n' Fleur

## 📦 Service Packages

### Package A – $270 + Delivery
- One Backdrop (color of your choice)
- Balloon garland with up to 3 colors
- Custom Happy Birthday Vinyl or LED sign

### Package B – $330 + Delivery
- Two Arch Backdrop (color of your choice)
- Balloon garland with up to 3 colors
- Custom Happy Birthday Vinyl or LED sign

### Package C – $300 + Delivery
- One Backdrop (color of your choice)
- Balloon garland with up to 3 colors
- Custom Happy Birthday Vinyl or LED sign
- One character prop (3ft–4ft)
- +$50 for additional backdrop

## 🔧 Configuration

### Python Environment
The `.vscode/settings.json` file is already configured to:
- Use the virtual environment Python interpreter
- Format code on save
- Enable Python linting

### Environment Variables (Optional)
Create a `.env` file for Flask-Mail configuration if you want to send email notifications:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

## 🚢 Deployment

To deploy this application:

1. **Generate requirements.txt**:
   ```bash
   pip freeze > requirements.txt
   ```

2. **Set Flask environment**:
   ```bash
   # Windows
   set FLASK_ENV=production
   set FLASK_DEBUG=0

   # macOS/Linux
   export FLASK_ENV=production
   export FLASK_DEBUG=0
   ```

3. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

4. **Popular hosting options**:
   - Heroku
   - PythonAnywhere
   - AWS EC2
   - DigitalOcean
   - Render
   - Railway

## 📝 Customization

### Adding Images
Place image files in `static/images/`:
- Replace placeholder image references (e.g., `package-a.jpg`, `gallery-1.jpg`)
- Images are automatically displayed in their respective sections

### Updating Business Info
Edit contact details directly in:
- `templates/base.html` (footer)
- `templates/contact.html` (contact info section)
- Or update the phone/email in `app.py`

### Modifying Colors
Edit the CSS color variables in `static/css/style.css`:
```css
:root {
    --color-bg: #FDE8EF;
    --color-primary: #C47A8A;
    --color-secondary: #A8C5A0;
    --color-text: #2C2C2C;
    /* ... */
}
```

### Adding New Packages
Edit `PACKAGES` list in `app.py` to add more service packages

## 🐛 Troubleshooting

### Virtual environment not activating
- Ensure you're in the correct project directory
- Try using the full path: `.\venv\Scripts\activate` (Windows)

### Port 5000 already in use
- Use a different port: `python app.py --port 5001`
- Or kill the process using port 5000

### Form submissions not saving
- Check that `bookings.csv` is writable
- Verify the `static/` and `templates/` directories exist

### Images not loading
- Verify image files are in `static/images/`
- Check the exact filename matches in the HTML/Python code

## 📚 Technologies Used

- **Backend**: Flask 2.3.3 (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Fonts**: Google Fonts (Cormorant Garamond, Lato, Dancing Script, Playfair Display)
- **Data Storage**: CSV (for booking submissions)
- **Styling**: Custom CSS with responsive design

## 📞 Support

For issues or questions about the website, contact:
- **Phone**: (943) 266-0114
- **Email**: Puffnfleur@gmail.com
- **Instagram**: @Puff_n_Fleur

## 📜 License

This project is proprietary to Puff n' Fleur. All rights reserved.

---

**Last Updated**: June 2024
**Version**: 1.0

🎈 *Where Balloons Meet Blooms* 🌸
