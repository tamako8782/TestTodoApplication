# Django + Flutter Todo Application

**Complete full-stack Todo application with Django REST API backend and Flutter mobile frontend**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Django](https://img.shields.io/badge/Django-5.2.2-green.svg)](https://djangoproject.com/)
[![Flutter](https://img.shields.io/badge/Flutter-3.32.2-blue.svg)](https://flutter.dev/)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone git@github.com:tamako8782/TestTodoApplication.git
cd TestTodoApplication
```

### 2. Setup Environment Variables
```bash
# Copy environment examples
cp .env.example .env
cp todo_flutter_app/.env.example todo_flutter_app/.env

# Edit .env files with your actual values
# - Django: SECRET_KEY, ALLOWED_HOSTS, etc.
# - Flutter: API_BASE_URL (your Django server URL)
```

### 3. Run Django Backend
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate

# Start Django server
python manage.py runserver 0.0.0.0:8000
```

### 4. Run Flutter App
```bash
cd todo_flutter_app

# Install Flutter dependencies
flutter pub get

# Run on your preferred platform
flutter run --dart-define-from-file=.env
```

## 📋 Features

### ✅ Backend (Django REST API)
- **CRUD Operations**: Create, Read, Update, Delete todos
- **Search Functionality**: Filter todos by title
- **RESTful API Design**: Consistent endpoint structure
- **Pagination Support**: Efficient data loading
- **CORS Configuration**: Cross-origin resource sharing
- **Environment-based Configuration**: Secure settings management

### ✅ Frontend (Flutter Mobile App)
- **Cross-platform Support**: iOS, Android, Web, Desktop
- **Material Design**: Modern, responsive UI
- **Dark Theme**: Beautiful dark mode interface
- **Real-time Sync**: Instant updates with backend
- **Environment Configuration**: Dynamic API endpoint
- **Error Handling**: User-friendly error messages

## 🏗️ Architecture

```
┌─────────────────┐    HTTP API     ┌─────────────────┐
│   Flutter App   │ ◄─────────────► │  Django Backend │
│                 │     JSON        │                 │
│  • iOS/Android  │                 │  • REST API     │
│  • Web/Desktop  │                 │  • SQLite DB    │
│  • Material UI  │                 │  • Admin Panel  │
└─────────────────┘                 └─────────────────┘
```

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Backend** | Django | 5.2.2 |
| **API Framework** | Django REST Framework | Latest |
| **Database** | SQLite | Built-in |
| **Frontend** | Flutter | 3.32.2 |
| **State Management** | Provider | Latest |
| **HTTP Client** | http package | Latest |
| **UI Design** | Material Design | Latest |

## 📁 Project Structure

```
TestTodoApplication/
├── 📄 README.md                     # This file
├── 📄 LICENSE                       # MIT License
├── 📄 requirements.txt              # Python dependencies
├── 📄 .env.example                  # Django environment template
├── 📄 .gitignore                    # Git ignore rules
├── 📂 doc/                          # Documentation
│   ├── 📄 README.md                 # Complete development guide
│   ├── 📄 01_flutter_setup.md       # Flutter environment setup
│   ├── 📄 02_xcode_config.md        # Xcode configuration
│   ├── 📄 03_deployment.md          # Production deployment
│   ├── 📄 04_testing.md             # Testing implementation
│   ├── 📄 05_troubleshooting.md     # Common issues & solutions
│   └── 📄 06_django_api.md          # REST API documentation
├── 📂 todoproject/                  # Django project settings
│   ├── 📄 settings.py               # Django configuration
│   ├── 📄 urls.py                   # URL routing
│   └── 📄 wsgi.py                   # WSGI configuration
├── 📂 todo/                         # Django app
│   ├── 📄 models.py                 # Data models
│   ├── 📄 api_views.py              # REST API endpoints
│   ├── 📄 serializers.py            # DRF serializers
│   ├── 📄 tests.py                  # Backend tests (19 tests)
│   └── 📂 templates/                # HTML templates
└── 📂 todo_flutter_app/             # Flutter application
    ├── 📄 pubspec.yaml              # Flutter dependencies
    ├── 📄 .env.example              # Flutter environment template
    ├── 📂 lib/                      # Dart source code
    │   ├── 📄 main.dart             # App entry point
    │   ├── 📂 models/               # Data models
    │   ├── 📂 services/             # API services
    │   ├── 📂 screens/              # UI screens
    │   └── 📂 widgets/              # Reusable components
    ├── 📂 test/                     # Flutter tests
    └── 📂 ios/android/web/...       # Platform-specific files
```

## 🚀 Getting Started Guide

### Prerequisites
- **Python 3.8+** with pip
- **Flutter SDK 3.0+**
- **Git** for version control
- **Code editor** (VS Code recommended)

### Step-by-Step Setup

1. **Environment Setup** 🔧
   - Copy `.env.example` → `.env` (both Django and Flutter)
   - Configure your database and API settings

2. **Backend Development** 🖥️
   - Start with Django REST API
   - Test endpoints at `http://localhost:8000/api/`

3. **Frontend Development** 📱
   - Configure Flutter app
   - Connect to Django API
   - Test on your preferred platform

4. **Integration Testing** 🧪
   - Run Django tests: `python manage.py test`
   - Run Flutter tests: `flutter test`

5. **Production Deployment** 🚀
   - See [deployment guide](doc/03_deployment.md)

## 📚 Documentation

| Guide | Description | Audience |
|-------|-------------|----------|
| **[Project Overview](doc/README.md)** | Complete development journey | All developers |
| **[Flutter Setup](doc/01_flutter_setup.md)** | Flutter environment & app creation | Mobile developers |
| **[Xcode Config](doc/02_xcode_config.md)** | iOS development setup | iOS developers |
| **[Deployment](doc/03_deployment.md)** | Production deployment guide | DevOps engineers |
| **[Testing](doc/04_testing.md)** | Comprehensive testing suite | QA engineers |
| **[Troubleshooting](doc/05_troubleshooting.md)** | Common issues & solutions | All developers |
| **[REST API](doc/06_django_api.md)** | API endpoints documentation | Backend developers |

## 🧪 Testing

### Backend Tests
```bash
# Run all Django tests
python manage.py test

# With coverage
pip install coverage
coverage run manage.py test
coverage report
```

### Frontend Tests
```bash
cd todo_flutter_app

# Run Flutter tests
flutter test

# Integration tests
flutter drive --target=test_driver/app.dart
```

## 🛠️ Development Workflow

1. **Feature Development**
   - Backend: Add API endpoint → Write tests → Update documentation
   - Frontend: Add UI → Connect to API → Write tests

2. **Code Quality**
   - Python: Follow PEP 8, use black formatter
   - Dart: Follow dart format conventions

3. **Version Control**
   - Feature branches: `feature/your-feature-name`
   - Commit messages: Use conventional commits

## 🔧 Configuration

### Environment Variables

**Django (`.env`)**
```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,your-server-ip
CORS_ALLOW_ALL_ORIGINS=True
```

**Flutter (`todo_flutter_app/.env`)**
```env
API_BASE_URL=http://your-server-ip:8000/api
APP_NAME=Todo Flutter App
APP_VERSION=1.0.0
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Documentation**: Check the [doc/](doc/) folder for detailed guides
- **Issues**: Create an issue for bug reports or feature requests
- **Discussions**: Use GitHub Discussions for questions

---

**Built with ❤️ using Django and Flutter** 