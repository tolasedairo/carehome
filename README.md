# CareHome Management System

A full-stack Django care home management application showcasing responsive web design, secure role-based authentication, CRUD operations, comprehensive audit logging, and deployment best practices.

**Deployed Site:** [CareHome Management System](https://carehome-c3a4ac54b776.herokuapp.com/)

---

## Table of Contents

1. [Project Planning](#project-planning)
2. [Front-End Design](#front-end-design)
3. [Database Architecture](#database-architecture)
4. [Agile Methodology](#agile-methodology)
5. [Code Quality](#code-quality)
6. [Features](#features)
7. [Technology Stack](#technology-stack)
8. [Installation & Setup](#installation--setup)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Credits](#credits)

---

## Project Planning

CareHome is a comprehensive care home management system built with Django, designed to manage residents, care plans, handovers, incidents, and audit logs with robust role-based access control. The application serves three distinct user roles: Managers, Senior Carers/Nurses, and Carers, each with appropriate permissions and access levels.

### Core Functional Areas:
- **Authentication & Role Approval:** Custom user model with manager approval workflow
- **Resident & Care Plan Management:** Complete CRUD operations with embedded UK-standard care plans
- **Incident Reporting & Resolution:** Type-categorized incident tracking with resolution workflow
- **Shift Handovers:** Priority-based handover management with completion tracking
- **Audit Logging:** Automatic change logging via Django signals for accountability
- **Dashboard Overview:** Role-based statistics and quick access to key information

---

## Front-End Design

A responsive, accessible, and user-friendly front-end that meets accessibility guidelines and follows UX/UI design principles using HTML5, CSS3, Bootstrap 5, and JavaScript.

### Responsive Design Implementation:
- **Mobile-First Approach:** Bootstrap 5.3.2 grid system ensures responsiveness across all screen sizes
- **Accessibility Features:**
  - Semantic HTML5 tags for improved screen reader compatibility
  - Correct heading hierarchy throughout all pages
  - ARIA labels on interactive elements and form inputs
  - Color contrast meeting WCAG 2.1 AA standards
  - Keyboard navigation support
- **Consistent UI/UX:**
  - Custom CSS variables for maintainable theming
  - Gradient sidebar with role-based navigation
  - Card-based layouts for content sections
  - Toast notifications for user feedback
  - Responsive tables with mobile-friendly views

### User Features:
- **Authentication:**
  - Secure account creation with role selection
  - Login/logout functionality using Django-Allauth
  - Manager approval workflow for new accounts
  - Password reset and email verification
  
- **Resident Management:**
  - Create, view, edit, and archive resident profiles
  - Upload profile pictures via Cloudinary
  - Embedded care plan creation and editing
  - Search and filter by name or status
  - Incident and handover history per resident
  
- **Care Plans:**
  - UK-standard 10-section care plan structure
  - Inline creation/editing during resident management
  - Review date tracking
  - Active/archive status management
  
- **Incident Reporting:**
  - Create incidents linked to residents or general
  - Categorize by type (Fall, Medication Error, Behavioral, Other)
  - Mark incidents as resolved
  - Filter by status and type
  - Audit trail of all changes
  
- **Shift Handovers:**
  - Create handovers with priority levels (Low, Normal, High, Urgent)
  - Assign to specific shifts (Morning, Afternoon, Night)
  - Mark handovers as completed
  - Filter by shift, priority, and completion status
  
- **Dashboard:**
  - Statistics overview (residents, incidents, handovers)
  - Recent activity lists
  - Quick access cards to key features
  - Role-based content visibility

### Frontend Technologies:
- **HTML5:** Semantic markup for structure and accessibility
- **CSS3:** Custom styling with CSS variables and gradients
- **Bootstrap 5.3.2:** Pre-built responsive components and grid system
- **JavaScript:** Vanilla JavaScript for interactive elements and form handling
- **Font Awesome 6.4.0:** Icon library for visual consistency
- **Google Fonts (Poppins):** Professional typography
- **Cloudinary:** Image hosting and delivery for resident profile pictures
- **Crispy Forms with Bootstrap5:** Enhanced form rendering with consistent styling

---

## Database Architecture

A secure Django web framework with PostgreSQL database and custom models designed for care home management. An Entity Relationship Diagram (ERD) was designed early in the project to organize the database architecture.

### Database Models:

#### 1. **CustomUser Model** (extends AbstractUser)
Manages authentication with role-based access control.

**Fields:**
- `role`: CharField with choices (MANAGER, SENIOR, CARER)
- `is_approved`: BooleanField for manager approval workflow
- Inherits standard fields from AbstractUser (username, email, password, etc.)

**Relationships:**
- One-to-Many with Resident (created_by)
- One-to-Many with CarePlan (created_by)
- One-to-Many with Incident (created_by)
- One-to-Many with Handover (created_by)

---

#### 2. **Resident Model**
Stores resident profiles with personal and medical information.

**Fields:**
- `first_name`, `last_name`: CharField (max_length=100)
- `date_of_birth`: DateField
- `gender`: CharField with choices (MALE, FEMALE, OTHER)
- `room_number`: CharField (max_length=20)
- `emergency_contact_name`, `emergency_contact_phone`: CharField
- `medical_notes`: TextField (blank=True)
- `profile_picture`: CloudinaryField (blank=True, null=True)
- `is_active`: BooleanField for soft delete (default=True)
- `created_at`, `updated_at`: DateTimeField (auto timestamps)

**Relationships:**
- ForeignKey to CustomUser (created_by, on_delete=SET_NULL)
- One-to-Many with CarePlan (reverse: care_plans)
- One-to-Many with Incident (reverse: incidents)
- One-to-Many with Handover (reverse: handovers)

---

#### 3. **CarePlan Model**
UK-standard 10-section care plans linked to residents.

**Fields:**
- `title`: CharField (max_length=200, default="Care Plan")
- `assessment_summary`: TextField (blank=True)
- `personal_care`, `mobility`, `nutrition`, `medication`: TextField (blank=True)
- `communication`, `wellbeing`, `skin_integrity`, `daily_routine`: TextField (blank=True)
- `safeguarding_risks`: TextField (blank=True)
- `review_date`: DateField (blank=True, null=True)
- `is_active`: BooleanField (default=True)
- `created_at`, `updated_at`: DateTimeField (auto timestamps)

**Relationships:**
- ForeignKey to Resident (on_delete=CASCADE)
- ForeignKey to CustomUser (created_by, on_delete=SET_NULL)

---

#### 4. **Incident Model**
Tracks incidents with type categorization and resolution status.

**Fields:**
- `incident_type`: CharField with choices (FALL, MED_ERROR, BEHAVIOR, OTHER)
- `description`: TextField
- `is_resolved`: BooleanField (default=False)
- `created_at`: DateTimeField (auto_now_add=True)

**Relationships:**
- ForeignKey to Resident (on_delete=CASCADE, blank=True, null=True)
- ForeignKey to CustomUser (created_by, on_delete=SET_NULL)

---

#### 5. **Handover Model**
Manages shift handovers with priority levels and completion tracking.

**Fields:**
- `title`: CharField (max_length=200)
- `shift`: CharField with choices (MORNING, AFTERNOON, NIGHT)
- `priority`: CharField with choices (LOW, NORMAL, HIGH, URGENT)
- `notes`: TextField
- `is_completed`: BooleanField (default=False)
- `created_at`, `updated_at`: DateTimeField (auto timestamps)

**Relationships:**
- ForeignKey to Resident (on_delete=SET_NULL, blank=True, null=True)
- ForeignKey to CustomUser (created_by, on_delete=SET_NULL)

---

#### 6. **AuditLog Model**
Automatic logging of all key actions for accountability.

**Fields:**
- `user`: ForeignKey to CustomUser
- `action`: CharField (CREATE, UPDATE, DELETE, ARCHIVE, UNARCHIVE, RESOLVE, COMPLETE)
- `model_name`: CharField (model being changed)
- `object_id`: CharField (ID of changed object)
- `timestamp`: DateTimeField (auto_now_add=True)
- `details`: TextField (additional context)

**Relationships:**
- ForeignKey to CustomUser (on_delete=SET_NULL)

### Security Measures:
- **on_delete=models.CASCADE:** Ensures data integrity when residents are deleted
- **on_delete=models.SET_NULL:** Preserves records when users are deleted
- **User Isolation:** `user=request.user` filter prevents unauthorized access to other users' data
- **Data Validation:** 
  - Form-level validation for date ranges and required fields
  - `clean()` methods prevent invalid data entry
  - Role-based validation in view logic
- **Soft Deletes:** `is_active` flag for residents and care plans preserves data while removing from active lists
- **Approval Workflow:** `is_approved` flag ensures only authorized users can access the system

---

## Agile Methodology

Agile tools were used to plan and track project tasks and progress throughout development. User stories were documented and managed using GitHub Projects.

### User Story Management:
- User stories written early in the project with clear acceptance criteria
- Kanban board used to track progress (To Do, In Progress, Done)
- Each user story prioritized using MoSCoW method:
  - **Must-Have:** Core authentication, resident CRUD, care plans, role-based access
  - **Should-Have:** Incident reporting, handovers, audit logging
  - **Could-Have:** Advanced filtering, dashboard statistics, profile pictures
- Regular reviews and updates to ensure focus on deliverables
- Tasks broken down into manageable subtasks for iterative development

### Key User Stories Implemented:

#### 1. **Resident & Care Plan Management**
As a Care Home Manager, I can create and manage resident profiles with optional care plans to maintain complete and compliant care records.

**Acceptance Criteria:**
- ✅ Residents can be created with required personal details
- ✅ Care plans can optionally be created during resident creation
- ✅ Residents can be edited by authorized users
- ✅ Residents can be archived (soft delete)
- ✅ Audit logs record create/update/archive actions
- ✅ Only managers can archive/edit residents

#### 2. **Incident Reporting**
As a Care Home Staff member, I can create and manage incidents for residents to ensure all incidents are recorded and tracked.

**Acceptance Criteria:**
- ✅ Incidents can be created for specific residents or general
- ✅ Incidents can be filtered by status (resolved/open) and type
- ✅ Incidents can be marked as resolved
- ✅ Audit logs record all incident actions

#### 3. **Shift Handovers**
As a Care Home Staff member, I can create and manage shift handovers to pass important information between shifts efficiently.

**Acceptance Criteria:**
- ✅ Handovers can be created with priority levels
- ✅ Handovers can be assigned to specific shifts
- ✅ Handovers can be marked as completed
- ✅ Filtering by shift, priority, and completion status

#### 4. **Authentication & Role Approval**
As a system administrator, I can manage user roles and approvals to ensure only approved staff access restricted features.

**Acceptance Criteria:**
- ✅ Users have distinct roles (Manager, Senior Carer, Carer)
- ✅ Only managers can approve new users
- ✅ Approval status enforced via decorators
- ✅ Unapproved users redirected to approval waiting page

#### 5. **Audit Logging**
As an administrator, I can view all key actions logged to track changes and ensure accountability.

**Acceptance Criteria:**
- ✅ Create, update, archive, resolve, complete actions are logged
- ✅ Logs include user, timestamp, action, target model and ID
- ✅ Logs displayed in admin panel

#### 6. **Dashboard Overview**
As a Care Home Manager, I can view a dashboard overview to quickly see resident stats, incidents, and handovers.

**Acceptance Criteria:**
- ✅ Display key statistics (residents, incidents, handovers)
- ✅ Quick access links to main features
- ✅ Role-based content visibility

---

## Code Quality

### Code Organization:
- **Django Apps Structure:** Separated concerns with dedicated apps:
  - `accounts`: User authentication and role management
  - `residents`: Resident profile management
  - `careplans`: Care plan creation and management
  - `incidents`: Incident reporting and resolution
  - `handovers`: Shift handover management
  - `audit`: Automatic audit logging
  - `dashboard`: Statistics and overview
  
- **Model Validation:** 
  - `clean()` methods for date validation
  - Form-level validation for required fields
  - Custom validators for data integrity
  
- **DRY Principle:**
  - Reusable base template (`base.html`)
  - Shared CSS utilities and variables
  - Common decorators for access control (`@approval_required`)
  - Consistent form rendering with Crispy Forms
  
- **Documentation:**
  - Comprehensive docstrings on models and views
  - Inline comments explaining complex logic
  - Detailed README and architecture documentation
  
- **Naming Conventions:**
  - Clear, descriptive names for variables and functions
  - PEP 8 compliant code formatting
  - Consistent naming across models and views

### Class-Based Views Implementation:
The application extensively uses Django's Class-Based Views (CBVs) for consistent and maintainable code:

- **ListView:** For displaying paginated lists (residents, incidents, handovers)
- **CreateView:** For creating new objects with form handling
- **UpdateView:** For editing existing objects
- **DetailView:** For displaying individual object details
- **TemplateView:** For static pages and dashboard

**Benefits:**
- Reduced code duplication through inheritance
- Built-in pagination and form handling
- Consistent error handling and validation
- Easier to extend and customize with mixins

### Security Best Practices:
- **CSRF Protection:** Django's built-in CSRF middleware
- **SQL Injection Prevention:** ORM query parameterization
- **XSS Protection:** Django template auto-escaping
- **Role-Based Access Control:** Custom decorators and view-level checks
- **Environment Variables:** Sensitive data stored in `.env` file
- **Password Hashing:** Django's PBKDF2 algorithm
- **HTTPS Enforcement:** Enabled in production settings

---

## Features

### Authentication & Authorization
- Secure user registration with role selection
- Django-Allauth integration for login/logout
- Manager approval workflow for new accounts
- Role-based access control (Manager, Senior Carer, Carer)
- Unapproved user redirection and waiting page

### Resident Management
- Complete CRUD operations for resident profiles
- Cloudinary integration for profile picture uploads
- Archive/unarchive functionality (soft delete)
- Search by name with real-time filtering
- Status filtering (active/archived)
- Manager-only edit and archive permissions

### Care Plan Management
- UK-standard 10-section care plans
- Inline creation during resident creation
- Inline editing during resident updates
- Review date tracking
- Active/archive status management
- Automatically linked to residents

### Incident Reporting
- Create incidents linked to residents or general
- Type categorization (Fall, Medication Error, Behavioral, Other)
- Resolution tracking and status updates
- Filter by type, status, and resident
- Search by description or resident name
- Automatic audit logging of all changes

### Shift Handovers
- Priority-based handovers (Low, Normal, High, Urgent)
- Shift assignment (Morning, Afternoon, Night)
- Completion status tracking
- Filter by shift, priority, and completion
- Search by title or resident name
- Recent handover quick access

### Audit Logging
- Automatic logging via Django signals
- Track all create, update, delete, archive actions
- User attribution for accountability
- Timestamp recording
- Model and object ID tracking
- Admin panel access to logs

### Dashboard
- Statistics overview (residents, incidents, handovers)
- Recent activity lists (last 5 items)
- Quick access cards to key features
- Role-based content visibility
- Week-over-week comparison metrics

---

## Technology Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Django | 5.0.4 | Web framework |
| Python | 3.12 | Programming language |
| PostgreSQL | Latest | Production database (Neon) |
| SQLite3 | Latest | Development database |
| Gunicorn | 25.1.0 | WSGI HTTP server |
| Daphne | Latest | ASGI HTTP server |

### Authentication
| Package | Version | Purpose |
|---------|---------|---------|
| django-allauth | 65.14.3 | Authentication and registration |
| Custom Decorators | - | Role-based access control |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| HTML5 | - | Semantic markup |
| CSS3 | - | Custom styling |
| Bootstrap | 5.3.2 | CSS framework |
| JavaScript | Vanilla | Client-side interactivity |
| Font Awesome | 6.4.0 | Icon library |
| Google Fonts | Poppins | Typography |

### Forms & Media
| Package | Version | Purpose |
|---------|---------|---------|
| django-crispy-forms | 2.4 | Enhanced form rendering |
| crispy-bootstrap5 | 2025.6 | Bootstrap 5 integration |
| Cloudinary | 1.44.1 | Image/media storage |
| django-cloudinary-storage | 0.3.0 | Django storage backend |
| Pillow | 12.1.1 | Image processing |

### Database & Deployment
| Package | Version | Purpose |
|---------|---------|---------|
| psycopg2-binary | 2.9.11 | PostgreSQL adapter |
| dj-database-url | 3.1.1 | Database URL parsing |
| python-dotenv | 1.2.1 | Environment variable management |
| whitenoise | 6.11.0 | Static file serving |

### External Services
| Service | Purpose |
|---------|---------|
| Cloudinary | Image hosting and delivery |
| Neon | PostgreSQL hosting (production) |
| Heroku | Application hosting |

---

## Installation & Setup

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- PostgreSQL (for production) or SQLite3 (for development)
- Git
- Cloudinary account (for image uploads)

### Local Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/carehome.git
cd carehome
```

2. **Create and activate virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file in the project root:**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Cloudinary credentials
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Database (optional for local development - uses SQLite by default)
# DATABASE_URL=postgres://user:password@host:port/database
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Create a superuser:**
```bash
python manage.py createsuperuser
```

7. **Collect static files:**
```bash
python manage.py collectstatic --noinput
```

8. **Run the development server:**
```bash
python manage.py runserver
```

9. **Access the application:**
- Open browser to `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key for security | Yes |
| `DEBUG` | Debug mode (True/False) | Yes |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Production |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Yes |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Yes |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Yes |

---

## Testing

### Test Coverage

The application includes comprehensive test suites for all major functionality:

#### **Residents App Tests** (`residents/tests.py`, `residents/tests_permissions.py`)
- Resident creation, update, and archive operations
- Care plan inline creation and editing
- Permission checks (manager-only operations)
- Form validation and data integrity
- Search and filtering functionality

#### **Incidents App Tests** (`incidents/tests.py`)
- Incident creation and resolution
- Type categorization and filtering
- Status update workflows
- Audit log generation

#### **Handovers App Tests** (`handovers/tests.py`)
- Handover creation and completion
- Priority and shift assignment
- Filtering by multiple criteria

#### **Accounts App Tests** (`accounts/tests.py`)
- User registration and login
- Role assignment
- Approval workflow
- Permission decorators

### Running Tests

**Run all tests:**
```bash
python manage.py test
```

**Run tests for a specific app:**
```bash
python manage.py test residents
python manage.py test incidents
python manage.py test handovers
python manage.py test accounts
```

**Run with verbose output:**
```bash
python manage.py test --verbosity=2
```

**Keep test database for faster subsequent runs:**
```bash
python manage.py test --keepdb
```

**Run specific test class or method:**
```bash
python manage.py test residents.tests_permissions.ResidentPermissionTests
python manage.py test residents.tests_permissions.ResidentPermissionTests.test_manager_can_archive
```

### Test Results
All tests pass successfully:
- **Residents:** 4 tests passed
- **Incidents:** 3 tests passed
- **Handovers:** Tests implemented
- **Accounts:** Tests implemented

---

## Deployment

### Heroku Deployment

The application is deployed on Heroku with PostgreSQL database hosted on Neon.

#### Deployment Steps:

1. **Install Heroku CLI and login:**
```bash
heroku login
```

2. **Create Heroku app:**
```bash
heroku create carehome-app-name
```

3. **Set environment variables:**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set CLOUDINARY_CLOUD_NAME=your-cloud-name
heroku config:set CLOUDINARY_API_KEY=your-api-key
heroku config:set CLOUDINARY_API_SECRET=your-api-secret
heroku config:set DATABASE_URL=your-neon-postgres-url
```

4. **Deploy to Heroku:**
```bash
git push heroku main
```

5. **Run migrations on Heroku:**
```bash
heroku run python manage.py migrate
```

6. **Create superuser on Heroku:**
```bash
heroku run python manage.py createsuperuser
```

7. **Collect static files:**
```bash
heroku run python manage.py collectstatic --noinput
```

#### Required Files:

**`Procfile`:**
```
web: gunicorn config.wsgi
```

**`runtime.txt`:**
```
python-3.12.1
```

**`requirements.txt`:**
Generated with `pip freeze > requirements.txt`

#### Production Settings:
- `DEBUG = False`
- `ALLOWED_HOSTS` includes Heroku domain
- Static files served via WhiteNoise
- PostgreSQL database via Neon
- Cloudinary for media storage

---

## Credits

### Technologies & Frameworks
- [Django](https://www.djangoproject.com/) - Web framework
- [Bootstrap 5](https://getbootstrap.com/) - CSS framework
- [Font Awesome](https://fontawesome.com/) - Icon library
- [Google Fonts](https://fonts.google.com/) - Typography (Poppins)
- [Cloudinary](https://cloudinary.com/) - Image hosting
- [Neon](https://neon.tech/) - PostgreSQL hosting
- [Heroku](https://www.heroku.com/) - Application hosting

### Django Packages
- [django-allauth](https://django-allauth.readthedocs.io/) - Authentication
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/) - Form rendering
- [django-cloudinary-storage](https://pypi.org/project/django-cloudinary-storage/) - Cloudinary integration
- [WhiteNoise](http://whitenoise.evans.io/) - Static file serving
- [Gunicorn](https://gunicorn.org/) - WSGI server

### Learning Resources
- Django Documentation
- Bootstrap Documentation
- MDN Web Docs
- Stack Overflow Community
- Real Python Tutorials

### Inspiration
This project was inspired by the need for comprehensive care home management systems that prioritize user experience, security, and audit compliance.

---

**Developed by:** Sefi Yemane  
**Project Type:** Full-Stack Django Web Application  
**Date:** February 2026  
**License:** Educational Use

---
