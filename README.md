# Cyber Crime Management System (CCMS) - Django (Development scaffold)

This is a minimal, ready-to-run Django scaffold for the CCMS project described in the prompt.
It includes users registration/login, case reporting with optional image, tracking, and admin integration.

## Quick start (development)
1. Create virtualenv & activate:
   - Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations & create superuser:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Run development server:
   ```bash
   python manage.py runserver
   ```
5. Open http://127.0.0.1:8000/

## Notes
- MEDIA files are stored in `media/`. In development, Django serves them when DEBUG=True.
- To run tests: `python manage.py test`
