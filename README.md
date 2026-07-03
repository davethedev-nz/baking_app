
# 🧁 BakingProject Member Management System

This Django-based application manages members of an organization and allows administrators to generate and send PDF certificates via email.

## 🚀 Features

- Member model with business name, contact details, and status
- Admin panel for managing members
- CSV import command to batch load members
- Custom email sender with templated content
- PDF certificate generator with branding
- Email dispatch with certificate attachment
- Signature management with image upload
- Dockerized environment (PostgreSQL, Gunicorn, Nginx)

## 🛠️ Project Structure

```
BakingProject/
└── baking_app/
    ├── members/                # Django app for member management
    ├── member_management/      # Settings module
    ├── manage.py
    ├── Dockerfile
    └── docker-compose.yml
```

## 🐳 Getting Started

### Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd BakingMailer/baking_app

# Create environment file
cp dev.env .env
# Edit .env and configure your email settings and file paths

# Build and run containers
docker compose up --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser for admin access
docker compose exec web python manage.py createsuperuser

# Import members from CSV (optional)
docker compose exec web python manage.py import_members /app/members.csv
```

### Accessing the Application

- Admin Panel: `http://localhost:8000/admin`
- Login with the superuser credentials you created

### Setting Up Email Templates & Signatures

1. Log into the admin panel
2. Navigate to **Email Templates** and create a template named `Membership Certificate Email`
3. Set the template as **Active**
4. Navigate to **Email Signatures** and create a signature named `Accounts Signature`
5. Upload a signature image and set it as **Active**

### Running Certificate Generation

```bash
# Generate certificates WITHOUT sending emails (for testing)
docker compose exec web python manage.py send_baking_certs --no-send

# Generate and SEND certificates to all members
docker compose exec web python manage.py send_baking_certs
```

Certificates will be saved to `output_certs/` directory.

## ✉️ Email Sending

Emails are rendered using templates with context-substitution and can include:

- Business name
- Custom signature (with image attachment)
- PDF certificate as attachment

**Important:** During development, certs are saved to `output_certs/` for preview.

## 🖼️ Certificate Generation *** Required PNG file for cert generation

Certificates are rendered by overlaying member data (e.g., business name) on a background image and saving as PDF.

Configure the template image in:
```
/certificate_templates/
```
Then add filename to .env file

## 🖼️ Welcome Pack inclusion *** Required PDF file for attaching to email

Add Welcome pack PDF to:

```
/static/welcome_pack/
```
Then add filename to .env file

## 🔐 Environment Variables

Set these in your `.env` file (copy from `dev.env`):

```env
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True

# Certificate Configuration
CERT_IMAGE_FILE=BakingCert.png
CERT_YEAR=2026/2027

# Welcome Pack Configuration
WELCOME_PACK_FILE=WelcomePack.pdf

# Database Configuration (already set in docker-compose.yml)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

## 📦 Requirements

- Python 3.12
- Django 5.x
- Pillow
- psycopg2
- gunicorn
- docker / docker compose

## 📤 Deployment (WIP)

Production-ready Dockerfile uses Gunicorn + Nginx. Volumes are configured for:

- Uploaded files
- Output certificates

AWS Fargate or ECS support planned.

## 📄 License

MIT

---

## ✨ Author

Dave Chapman
