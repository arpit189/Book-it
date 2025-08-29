# Travel Booker - Django Travel Booking Application

A production-ready Django web application for booking flights, trains, and buses with user authentication, booking management, and responsive design.

## 🚀 Features

- **User Authentication**: Registration, login, logout, and profile management
- **Travel Options**: CRUD operations for flights, trains, and buses
- **Booking System**: Book seats with availability validation and atomic transactions
- **Booking Management**: View, filter, and cancel bookings
- **Responsive Design**: Bootstrap 5 templates for mobile-friendly experience
- **Admin Interface**: Complete admin panel for travel and booking management
- **Unit Tests**: Comprehensive test coverage for core functionality
- **Production Ready**: Deployment configurations for PythonAnywhere and AWS

## 🛠️ Technology Stack

- **Backend**: Django 5.0+ (Python 3.11+)
- **Database**: MySQL (with SQLite fallback for development)
- **Frontend**: Django Templates + Bootstrap 5
- **Authentication**: Django's built-in auth system
- **Deployment**: Gunicorn + Whitenoise (static files)

## 📋 Prerequisites

- Python 3.11 or higher
- MySQL (for production) or SQLite (for development)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/travel-booker.git
cd travel-booker
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Database Setup

#### For SQLite (Development)
```bash
python manage.py migrate
```

#### For MySQL (Production)
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE travel_db;
CREATE USER 'travel_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON travel_db.* TO 'travel_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Update .env with MySQL credentials
python manage.py migrate
```

### 6. Seed Sample Data

```bash
python manage.py seed_travel_options
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run the Application

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the application.

## 🧪 Running Tests

```bash
python manage.py test
```

### Test Coverage

The test suite covers:
- User registration and authentication
- Travel option creation and display
- Booking creation with seat validation
- Booking cancellation and seat restoration
- Permission checks and security
- Form validation and error handling

## 📁 Project Structure

```
travel-booker/
├── travel_booker_project/     # Main Django project
│   ├── settings.py           # Project settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── bookings/                 # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Django forms
│   ├── urls.py              # App URL patterns
│   ├── tests.py             # Unit tests
│   └── templates/           # HTML templates
├── management/              # Management commands
│   └── commands/
│       └── seed_travel_options.py
├── static/                  # Static files
├── templates/               # Base templates
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── Procfile                # Deployment configuration
└── README.md               # This file
```

## 🌐 API Endpoints

### Public Endpoints
- `GET /` - Home page with search and travel options
- `GET /travel/` - List all travel options with filters
- `GET /travel/<id>/` - Travel option details
- `GET /accounts/register/` - User registration
- `GET /accounts/login/` - User login

### Protected Endpoints (Login Required)
- `GET /accounts/profile/` - User profile
- `GET /bookings/` - User's booking list
- `POST /bookings/create/` - Create new booking
- `POST /bookings/<id>/cancel/` - Cancel booking

### Admin Endpoints
- `GET /admin/` - Django admin interface

## 🚀 Deployment

### Option 1: PythonAnywhere

1. **Create PythonAnywhere Account**
   - Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload Your Code**
   ```bash
   # In PythonAnywhere bash console
   git clone https://github.com/yourusername/travel-booker.git
   cd travel-booker
   ```

3. **Setup Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 travel-booker
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with production settings
   ```

5. **Setup Database**
   ```bash
   # Use PythonAnywhere MySQL or SQLite
   python manage.py migrate
   python manage.py seed_travel_options
   python manage.py createsuperuser
   python manage.py collectstatic
   ```

6. **Configure WSGI File**
   - Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`
   - Add your project path and settings

7. **Reload Web App**
   - Go to Web tab and click "Reload"

### Option 2: AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB Application**
   ```bash
   eb init travel-booker
   eb create travel-booker-env
   ```

3. **Configure Environment Variables**
   ```bash
   eb setenv SECRET_KEY=your_secret_key
   eb setenv DEBUG=False
   eb setenv DATABASE_URL=mysql://user:pass@host:port/db
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

### Option 3: AWS EC2 with Gunicorn + Nginx

1. **Launch EC2 Instance**
   - Use Ubuntu 20.04 LTS
   - Configure security groups for HTTP/HTTPS

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx mysql-server
   ```

3. **Setup Application**
   ```bash
   git clone https://github.com/yourusername/travel-booker.git
   cd travel-booker
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Gunicorn**
   ```bash
   # Create systemd service
   sudo nano /etc/systemd/system/travel-booker.service
   ```

   ```ini
   [Unit]
   Description=Travel Booker Gunicorn
   After=network.target

   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/home/ubuntu/travel-booker
   Environment="PATH=/home/ubuntu/travel-booker/venv/bin"
   ExecStart=/home/ubuntu/travel-booker/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/travel-booker/travel-booker.sock travel_booker_project.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

5. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/travel-booker
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /home/ubuntu/travel-booker;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/home/ubuntu/travel-booker/travel-booker.sock;
       }
   }
   ```

6. **Enable and Start Services**
   ```bash
   sudo ln -s /etc/nginx/sites-available/travel-booker /etc/nginx/sites-enabled
   sudo systemctl start travel-booker
   sudo systemctl enable travel-booker
   sudo systemctl restart nginx
   ```

## 🔧 Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (MySQL)
MYSQL_DATABASE=travel_db
MYSQL_USER=travel_user
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🧪 Testing

Run the complete test suite:

```bash
python manage.py test
```

Run specific test modules:

```bash
python manage.py test bookings.tests
python manage.py test bookings.tests.BookingModelTest
```

## 📝 Git Workflow

### Recommended Branch Structure

```bash
main                    # Production-ready code
├── develop            # Integration branch
├── feature/user-auth  # Feature branches
├── feature/booking    # Feature branches
└── hotfix/bug-fix     # Hotfix branches
```

### Example Commits

```bash
git add .
git commit -m "feat: add user registration and authentication"
git commit -m "feat: implement travel booking system with seat validation"
git commit -m "feat: add booking cancellation functionality"
git commit -m "test: add comprehensive unit tests for booking logic"
git commit -m "style: improve responsive design with Bootstrap 5"
git commit -m "docs: update README with deployment instructions"
git commit -m "fix: resolve race condition in seat booking"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/yourusername/travel-booker/issues) page
2. Create a new issue with detailed description
3. Contact: arpit1892004@gmail.com

## 🎯 Roadmap

- [ ] Email notifications for bookings
- [ ] Payment integration (Stripe/PayPal)
- [ ] Mobile app (React Native)
- [ ] Advanced search with filters
- [ ] Booking calendar view
- [ ] Multi-language support
- [ ] API rate limiting
- [ ] Docker containerization

---

**Built with ❤️ using Django and Bootstrap 5**
