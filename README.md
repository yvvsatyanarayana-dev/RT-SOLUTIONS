# RT Solutions - Professional Enterprise Application

## 🎯 Overview

A complete professional web application built with Flask, featuring:

✅ **11 Public Pages** (Home, About, Services, Pricing, Team, Features, Blog, FAQ, Testimonials, Contact, Privacy, Terms)
✅ **Professional Admin Dashboard** with client & contact management
✅ **Multi-Theme Support** (Professional White, Light, Dark)
✅ **Responsive Design** - Works on desktop, tablet, mobile
✅ **Advanced Features** - Blog with pagination, client management, contact tracking
✅ **Database Models** - Contact, Client, Admin, BlogPost, Service, Testimonial
✅ **API Endpoints** - RESTful APIs for all operations
✅ **Security** - Password hashing with bcrypt, session management
✅ **Professional UI** - Clean, modern white color theme by default

---

## 📋 Features

### Public Features
- Responsive website with 11+ pages
- Professional blue and white color scheme
- Contact form with validation
- Blog system with categories and pagination
- Testimonials section
- FAQ page
- Services and pricing pages
- Team showcase
- Privacy & Terms pages

### Admin Features
- Secure login system (username: `admin`, password: `admin123`)
- Dashboard with statistics
- Contact management (view, edit, delete)
- Client management with company details
- Add/edit clients with contract values
- Theme preferences
- Password change functionality
- 24/7 support indicator

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- pip or uv package manager

### Installation

1. **Navigate to project directory:**
```bash
cd d:\RTSOLUTIONS
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

4. **Access the application:**
- Website: http://localhost:5000
- Admin Login: http://localhost:5000/admin/login

### Demo Credentials
- Username: `admin`
- Password: `admin123`

---

## 📁 Project Structure

```
RTSOLUTIONS/
├── main.py                 # Flask application & database models
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── static/
│   └── style.css          # Professional multi-theme CSS
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── pages/
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── services.html
│   │   ├── pricing.html
│   │   ├── team.html
│   │   ├── features.html
│   │   ├── blog.html
│   │   ├── blog-detail.html
│   │   ├── faq.html
│   │   ├── testimonials.html
│   │   ├── contact.html
│   │   ├── privacy.html
│   │   └── terms.html
│   ├── admin/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── contacts.html
│   │   ├── clients.html
│   │   ├── client-form.html
│   │   └── settings.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
└── instance/              # Database storage

```

---

## 🎨 Color Theme

The application features a professional **white color theme** as default:

### Default Professional Theme
- **Primary**: #1e40af (Deep Blue)
- **Secondary**: #3b82f6 (Bright Blue)
- **Accent**: #0ea5e9 (Cyan)
- **Background**: #ffffff (White)
- **Text**: #1f2937 (Dark Gray)

### Alternative Themes
- **Light Theme**: Brighter colors, white background
- **Dark Theme**: Dark background (#111827), light text

Users can switch themes from the top navigation bar.

---

## 📊 Database Models

### Contact Model
- id, name, email, phone, company, service, message
- status (new/contacted/resolved)
- notes, created_at, updated_at

### Client Model
- id, name, email, phone, company, industry
- status (active/inactive/prospect)
- contract_value, notes, created_at, updated_at

### Admin Model
- id, username, password (hashed), email, full_name
- role, theme preference, is_active, created_at

### BlogPost Model
- id, title, slug, excerpt, content, image
- category, author, created_at, updated_at

### Service Model
- id, name, description, icon, price, features

### Testimonial Model
- id, author, company, position, content, rating, image, created_at

---

## 🔒 Security Features

✅ Password hashing with bcrypt
✅ Secure session management
✅ CSRF protection ready
✅ SQL injection prevention with SQLAlchemy ORM
✅ XSS protection with template escaping
✅ Secure API endpoints with admin_required decorator

---

## 📱 Responsive Design

The application is fully responsive and optimized for:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

---

## 🔌 API Endpoints

### Public APIs
- `POST /api/contact` - Submit contact form

### Admin APIs (Requires Login)
- `GET /api/contact/list` - Get all contacts
- `GET /admin/api/contact/<id>` - Get contact details
- `PUT /admin/api/contact/<id>` - Update contact
- `DELETE /admin/api/contact/<id>` - Delete contact
- `GET /admin/api/client/<id>` - Get client details
- `PUT /admin/api/client/<id>` - Update client
- `DELETE /admin/api/client/<id>` - Delete client
- `POST /admin/api/settings/theme` - Update theme
- `POST /admin/api/password` - Change password

---

## 🎯 Customization

### Add Blog Post
Posts are automatically created in the database on first run. To add custom posts:
1. Log in to admin
2. Database contains sample blog posts
3. Posts support markdown content

### Update Services & Testimonials
These are pre-populated on first run. To customize:
1. Edit the `init_database()` function in `main.py`
2. Or use the database directly

### Change Colors
Edit the CSS variables in `static/style.css`:
```css
:root {
  --primary-color: #1e40af;
  --secondary-color: #3b82f6;
  /* ... etc ... */
}
```

---

## 🐛 Troubleshooting

**Port already in use:**
```bash
python main.py --port 5001
```

**Database issues:**
Delete `instance/rtsolutions.db` and restart to reset database

**Missing templates:**
Ensure all files in `templates/` directory exist

**CSS not loading:**
Clear browser cache (Ctrl+Shift+Delete) and refresh

---

## 📞 Support

For issues or questions:
- Email: info@rtsolutions.com
- Contact page: http://localhost:5000/contact

---

## 📄 License

© 2026 RT Solutions. All rights reserved.

---

## 🚀 Next Steps

1. Customize branding in `base.html`
2. Update company info in template pages
3. Add more team members in `team.html`
4. Create blog posts
5. Configure email notifications (optional)
6. Deploy to production

---

**Version:** 1.0.0
**Last Updated:** April 30, 2026
