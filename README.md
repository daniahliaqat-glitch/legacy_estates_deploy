# Legacy Estates — Real Estate Web Application

A full-featured real estate marketplace built with **Python (Django)** and **PostgreSQL**.
Supports property listings (Sale & Rent) across 4 property types — House, Apartment, Plot/Land,
and Commercial — with an Admin panel, Agent dashboards, and a public-facing site with search,
filters, and inquiry forms.

---

## 1. What's Included

- **Public site**: Homepage, property listings with search/filter/sort, property detail pages,
  agent profiles, contact page.
- **Agent Dashboard**: Agents log in to add, edit, and delete their own property listings
  (with photos and features).
- **Admin Panel** (`/admin/`): Full control — manage all properties, agents, users, inquiries,
  and contact messages. This is where the site owner manages everything.
- **No login required for Buyers/Sellers** — they simply browse and submit an inquiry form
  on any property (as requested).
- **Mobile responsive** — tested on mobile, tablet, and desktop breakpoints.
- **Demo data already loaded** — 8 sample properties, 2 sample agents, 1 admin account —
  so you can see the site fully populated immediately.

---

## 2. Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12 + Django 6.0 |
| Database | PostgreSQL (SQLite fallback available for quick local testing) |
| Frontend | Django Templates + custom CSS (no frontend framework — fast & simple to host) |
| Images | Pillow (for image uploads) |

---

## 3. Project Structure

```
legacy_estates/
├── accounts/          → Agent profiles, login, agent dashboard, property add/edit/delete
├── properties/         → Property listings, search/filter, homepage
├── inquiries/           → Contact forms & property inquiries
├── templates/           → All HTML templates
├── static/              → CSS, JS, images
├── media/                → Uploaded property photos (created at runtime)
├── legacy_estates/      → Project settings, URLs
└── manage.py
```

---

## 4. How To Run This Locally

### Step 1 — Install requirements
```bash
pip install django psycopg2-binary pillow
```

### Step 2 — Set up PostgreSQL
Create a database and user in PostgreSQL:
```sql
CREATE DATABASE legacy_estates_db;
CREATE USER legacy_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE legacy_estates_db TO legacy_user;
```

### Step 3 — Set environment variables
Create a `.env` file or export these in your terminal:
```bash
export DB_NAME=legacy_estates_db
export DB_USER=legacy_user
export DB_PASSWORD=your_password_here
export DB_HOST=localhost
export DB_PORT=5432
export DJANGO_SECRET_KEY=replace-with-a-long-random-string
export DJANGO_DEBUG=True
```

> **Quick testing without PostgreSQL?** Set `USE_POSTGRES=False` and Django will
> automatically use SQLite instead — no extra setup needed. Good for a quick demo,
> but use real PostgreSQL for the live/production site.

### Step 4 — Run migrations
```bash
python manage.py migrate
```

### Step 5 — Create your own admin account
```bash
python manage.py createsuperuser
```
(Or use the demo admin account below if you just want to explore first.)

### Step 6 — Start the server
```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000/**

---

## 5. Demo Login Credentials

These accounts already exist in the demo data so you can explore right away:

| Role | URL | Username | Password |
|---|---|---|---|
| **Admin** | `/admin/` | `admin` | `admin12345` |
| **Agent 1** | `/account/login/` | `sarah.khan` | `agent12345` |
| **Agent 2** | `/account/login/` | `james.lee` | `agent12345` |

> ⚠️ **Important:** Change these passwords before going live. These are demo
> credentials only, meant for testing.

---

## 6. How The Site Works (Quick Tour)

- **Buyers/Sellers (public visitors)**: No login. They browse `/listings/`, use the
  filters (price, city, type, bedrooms), open a property, and submit the inquiry form.
  Messages land in the Admin Panel → Inquiries.

- **Agents**: Log in at `/account/login/` → land on their Dashboard → click
  "+ Add New Listing" to create a property, or Edit/Delete their existing ones.
  Agents only see and manage **their own** listings.

- **Admin (you / site owner)**: Log in at `/admin/` with the superuser account.
  From here you can:
  - Add/edit/delete **any** property (not just one agent's)
  - Add new agents (create a User, then create an Agent profile linked to it)
  - View all inquiries and contact messages
  - Manage property features/amenities (e.g. "Swimming Pool", "Garage")
  - Mark properties as Featured (shows on homepage) or change status (Available/Pending/Sold/Rented)

---

## 7. Adding a New Agent (Admin steps)

1. Go to `/admin/auth/user/add/` → create a username + password for the agent.
2. Go to `/admin/accounts/agent/add/` → select that user, fill in phone, title, bio, etc.
3. The agent can now log in at `/account/login/` and manage their own listings.

---

## 8. Deploying to a Live Server (Production Notes)

Before going live, a developer/hosting provider should:

1. Set `DJANGO_DEBUG=False`
2. Set a strong, random `DJANGO_SECRET_KEY`
3. Set `DJANGO_ALLOWED_HOSTS` to your actual domain name
4. Use a real PostgreSQL database (not SQLite)
5. Serve static/media files properly (e.g. via Nginx, or a service like AWS S3)
6. Run behind a production server like **Gunicorn** + **Nginx** (not `manage.py runserver`,
   which is for development only)
7. Set up HTTPS (SSL certificate)

This part is normal "deployment" work — any Django developer or hosting service
(e.g. DigitalOcean, Railway, Render, PythonAnywhere) can take this project folder
and deploy it. The codebase itself is already production-structured (environment
variables, no hardcoded secrets, etc.).

---

## 9. Design Notes

- **Brand**: "Legacy Estates" — deep navy + ivory + brass/gold color palette, paired
  with a serif display font (headlines) and clean sans-serif body text, for a premium,
  trustworthy real-estate feel.
- Fully responsive: hamburger menu on mobile, stacked filters, single-column property
  grid on small screens.

---

## 10. Need Changes?

Common things you may want to adjust:
- **Colors/branding** → `static/css/base.css` (top of file, `:root` color variables)
- **Footer contact info** → `templates/base.html`
- **Homepage text** → `templates/properties/home.html`
- **Add more property features** → Admin Panel → Properties → Property Features

If you (or the client) need any new feature added later — like online payments,
WhatsApp integration, email notifications for new inquiries, or a map view — these
can be added on top of this existing structure.
