
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

## 🐳 Running the Project (Dev)

```bash
# Build and run containers
docker compose up --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Import members from CSV
docker compose exec web python manage.py import_members /app/data/members.csv
```

## ✉️ Email Sending

Emails are rendered using templates with context-substitution and can include:

- Business name
- Custom signature (with image attachment)
- PDF certificate as attachment

**Important:** During development, certs are saved to `output_certs/` for preview.

## 🖼️ Certificate Generation

Certificates are rendered by overlaying member data (e.g., business name) on a background image and saving as PDF.

Configure the template image in:
```
/certificate_templates/
```

## 🔐 Environment Variables

Set these in `.env` or your `settings.py`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
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
