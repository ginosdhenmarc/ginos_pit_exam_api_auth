-----SETUP INSTRUCTIONS-----
1. Clone the repository

git clone https://github.com/ginosdhenmarc/ginos_pit_exam_api_auth.git
cd ginos_pit_exam_api_auth

2. Create and activate a virtual environment
# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate

# macOS / Linux 
python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt
pip freeze > requirements.txt

4. Configure environment variables
//In your settings.py, make sure the following are set correctly:

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@mydomain.com'

//If you want to use a real email provider (e.g. Gmail), replace with:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'

5. Run migrations
python manage.py makemigrations
python manage.py migrate

6. Run the server
python manage.py runserver
//Server runs at: http://127.0.0.1:8000/

-----API Endpoints-----
Base URL: http://127.0.0.1:8000/api/

Endpoint
- register/             POST                 
- verify/               GET
- login/                POST
- token/refresh/        POST
- users/                GET         AUTH_REQUIRED


-----EXAMPLE OF REQUESTS AND RESPONSES-----
*****USER REGISTER*****
Request:
POST /api/register/
Content-Type: application/json

Body:
{
  "username": "dhenmarc",
  "email": "dhenmarc@mydomain.com",
  "password": "StrongPass123!",
  "password2": "StrongPass123!",
  "first_name": "Dhen Marc",
  "last_name": "Ginos"
}

Response (in terminal):

Hi dhenmarc,

Please verify your email by clicking the link below:
http://127.0.0.1:8000/api/verify/?token=eyJ1c2VyX2lkIjo0f...

//You can click on the link provided to verify your email

__________________________________________________________________
*****EMAIL VERIFICATION*****
Request:
GET /api/verify/?token=<verification_token>

Response:
{
  "message": "Email successfully verified. You can now log in."
}
________________________________________________________________
*****USER LOGN*****
Request:
POST /api/login/
Content-Type: application/json

Body:
{
  "username": "dhenmarc",
  "password": "StrongPass123!"
}

Response:
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh...",
  "access": "eyJ0eXAiOiJKV1QiLCJh...",
}
________________________________________________________________
*****VIEW USER LIST (THRU AUTH)*****
Request:
GET /api/users/
Authorization: Bearer <admin_access_token>
Authorized User access token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNTQ5MzAxLCJpYXQiOjE3NjE1NDg0MDEsImp0aSI6IjgyODhmYzYwYjk5YzQ2MDk5YjQ3Y2Y0NDYyMWNkZDY5IiwidXNlcl9pZCI6IjMiLCJ1c2VybmFtZSI6IkRoZW4ifQ.TyYH-BKWBJ-gBIhEYGSoVM1SH6eSzxuliWpW1_lDXAM

Response:
[
    {
        "id": 1,
        "username": "alice",
        "email": "alice@mydomain.com",
        "is_active": true,
        "is_staff": false
    },
    {
        "id": 2,
        "username": "www",
        "email": "dhen@mydomain.com",
        "is_active": true,
        "is_staff": false
    },
    {
        "id": 3,
        "username": "Dhen",
        "email": "gindhen@gmail.com",
        "is_active": true,
        "is_staff": true
    }
]
_______________________________________________________
-----API Documentation (Swagger UI)-----
Swagger UI: http://127.0.0.1:8000/swagger/
ReDoc: http://127.0.0.1:8000/redoc/


-----USEFUL COMMANDS-----
| Command                            | Description             |
| ---------------------------------- | ----------------------- |
| `python manage.py createsuperuser` | Create an admin account |
| `python manage.py runserver`       | Run the server          |
| `python manage.py shell`           | Open Django shell       |
| `python manage.py showmigrations`  | List applied migrations |











