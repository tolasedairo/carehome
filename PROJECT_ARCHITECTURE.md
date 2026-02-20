# CareHome Management System - Project Architecture

**Date**: February 20, 2026  
**Framework**: Django 6.0.2  
**Python Version**: 3.12  
**Database**: PostgreSQL (Neon)

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Application Architecture](#application-architecture)
5. [Data Models](#data-models)
6. [URL Routing](#url-routing)
7. [Views & Logic](#views--logic)
8. [Authentication & Authorization](#authentication--authorization)
9. [Signals & Audit Logging](#signals--audit-logging)
10. [Frontend Architecture](#frontend-architecture)
11. [Configuration](#configuration)
12. [Deployment](#deployment)

---

## Project Overview

CareHome is a comprehensive care home management system built with Django, designed to manage residents, care plans, handovers, incidents, and audit logs with role-based access control.

### Key Features
- **Resident Management**: CRUD operations with embedded care plans
- **Care Plans**: UK-standard 10-section care plans with archive/unarchive
- **Shift Handovers**: Priority-based handover management with completion tracking
- **Incident Reporting**: Incident tracking with type categorization and resolution workflow
- **Audit Logging**: Automatic change logging via Django signals
- **Role-Based Access**: Manager, Senior Carer, and Carer role permissions
- **Approval System**: New user approval workflow for managers
- **Responsive Design**: Bootstrap 5.3.2 with mobile-first approach

---

## Technology Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Django | 6.0.2 | Web framework |
| Python | 3.12 | Runtime environment |
| PostgreSQL | Latest | Database (Neon) |
| Gunicorn | Latest | WSGI server |
| Daphne | Latest | ASGI server |

### Authentication & Authorization
| Package | Version | Purpose |
|---------|---------|---------|
| django-allauth | Latest | Authentication |
| Custom Decorators | - | Role-based access |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Bootstrap | 5.3.2 | CSS framework |
| Font Awesome | 6.4.0 | Icons |
| Poppins Font | Latest | Typography |
| JavaScript | Vanilla | Client-side logic |

### External Services
| Service | Purpose |
|---------|---------|
| Cloudinary | Image/media storage |
| Neon | PostgreSQL hosting |

### Environment Variables
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`
- `DATABASE_URL` (Neon PostgreSQL)
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`

---

## Project Structure

```
carehome/
├── config/                          # Django project settings
│   ├── __init__.py
│   ├── settings.py                 # Configuration (INSTALLED_APPS, MIDDLEWARE, etc.)
│   ├── urls.py                     # Root URL router
│   ├── asgi.py                     # ASGI entry point
│   ├── wsgi.py                     # WSGI entry point
│   └── __pycache__/
│
├── accounts/                        # User authentication & management
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                   # CustomUser model
│   ├── views.py                    # Auth views (login, signup, approval)
│   ├── forms.py                    # User forms
│   ├── admin.py                    # Django admin config
│   ├── apps.py                     # App config
│   ├── urls.py                     # Auth routes
│   ├── tests.py                    # Unit tests
│   └── templates/auth/
│       ├── login.html
│       ├── signup.html
│       └── approval.html
│
├── residents/                       # Resident management
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                   # Resident model
│   ├── views.py                    # CRUD views
│   ├── forms.py                    # ResidentForm with embedded CarePlan
│   ├── signals.py                  # Auto audit logging
│   ├── admin.py                    # Django admin
│   ├── apps.py                     # App config
│   ├── urls.py                     # Resident routes
│   ├── tests.py                    # Tests
│   └── templates/residents/
│       ├── resident_list.html
│       ├── resident_detail.html
│       ├── resident_form.html
│       └── resident_archive.html
│
├── careplans/                       # Care plan management
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                   # CarePlan model (10 sections)
│   ├── views.py                    # CRUD views
│   ├── forms.py                    # CarePlanForm
│   ├── signals.py                  # Auto audit logging
│   ├── admin.py                    # Django admin
│   ├── apps.py                     # App config
│   ├── urls.py                     # CarePlan routes
│   ├── tests.py                    # Tests
│   └── templates/careplans/
│       ├── careplan_list.html
│       ├── careplan_detail.html
│       ├── careplan_form.html
│       └── careplan_archive.html
│
├── handovers/                       # Shift handover management
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                   # Handover model
│   ├── views.py                    # CRUD + complete views
│   ├── forms.py                    # HandoverForm
│   ├── signals.py                  # Auto audit logging
│   ├── admin.py                    # Django admin
│   ├── apps.py                     # App config
│   ├── urls.py                     # Handover routes
│   ├── tests.py                    # Tests
│   └── templates/handovers/
│       ├── handover_list.html
│       ├── handover_detail.html
│       ├── handover_form.html
│       └── handover_complete.html
│
├── incidents/                       # Incident reporting & management
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                   # Incident model
│   ├── views.py                    # CRUD + resolve/unresolve views
│   ├── forms.py                    # IncidentForm
│   ├── signals.py                  # Auto audit logging
│   ├── admin.py                    # Django admin
│   ├── apps.py                     # App config
│   ├── urls.py                     # Incident routes
│   ├── tests.py                    # Tests
│   └── templates/incidents/
│       ├── incident_list.html
│       ├── incident_detail.html
│       ├── incident_form.html
│       ├── incident_resolve.html
│       └── incident_unresolve.html
│
├── dashboard/                       # Manager dashboard
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                   # Empty (no models)
│   ├── views.py                    # Dashboard context aggregation
│   ├── forms.py                    # Empty
│   ├── admin.py                    # Empty
│   ├── apps.py                     # App config
│   ├── urls.py                     # Dashboard routes
│   ├── tests.py                    # Tests
│   └── templates/dashboard/
│       └── home.html               # Dashboard homepage
│
├── audit/                           # Audit logging & history
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py                   # AuditLog model
│   ├── views.py                    # List view with search/filter
│   ├── forms.py                    # Search/filter forms
│   ├── admin.py                    # Django admin
│   ├── apps.py                     # App config
│   ├── urls.py                     # Audit routes
│   ├── tests.py                    # Tests
│   └── templates/audit/
│       ├── auditlog_list.html
│       └── auditlog_detail.html
│
├── templates/                       # Global templates
│   ├── base.html                   # Base template with sidebar & footer
│   └── 404.html                    # Error pages
│
├── static/                          # Static files
│   ├── css/
│   │   ├── style.css               # Main styles
│   │   └── auth.css                # Auth page styles
│   ├── js/
│   │   └── script.js               # Form validation, placeholder fade
│   └── fonts/
│       └── poppins/                # Custom fonts
│
├── db.sqlite3                       # Development database (local)
├── manage.py                        # Django CLI
├── requirements.txt                 # Python dependencies
└── .env                             # Environment variables
```

---

## Application Architecture

### 7 Local Apps Architecture

Each app follows Django's standard MVT pattern:

```
App Directory/
├── models.py          → Define data models
├── views.py           → Handle HTTP requests/responses
├── forms.py           → Define data forms and validation
├── urls.py            → URL routing within app
├── signals.py         → Automatic operations (audit logging)
├── admin.py           → Django admin configuration
├── apps.py            → App configuration (signal registration)
├── tests.py           → Unit and integration tests
├── migrations/        → Database schema changes
└── templates/         → HTML templates
```

### Apps Overview

| App | Purpose | Key Model | Views |
|-----|---------|-----------|-------|
| **accounts** | User auth & management | CustomUser | Login, Signup, Approval |
| **residents** | Resident CRUD | Resident | List, Detail, Create, Edit, Archive |
| **careplans** | Care plan management | CarePlan | List, Detail, Create, Edit, Archive |
| **handovers** | Shift handovers | Handover | List, Detail, Create, Edit, Complete |
| **incidents** | Incident tracking | Incident | List, Detail, Create, Edit, Resolve |
| **dashboard** | Manager dashboard | None | Home (aggregated stats) |
| **audit** | Change logging & compliance | AuditLog | List, Search, Filter |

---

## Data Models

### CustomUser Model (accounts)
```python
Fields:
  - id: AutoField
  - username: CharField (unique)
  - email: EmailField (unique)
  - first_name: CharField
  - last_name: CharField
  - password: CharField (hashed)
  - role: CharField (choices: MANAGER, SENIOR, CARER)
  - is_active: BooleanField
  - is_approved: BooleanField
  - is_staff: BooleanField
  - created_at: DateTimeField (auto_now_add)
  - updated_at: DateTimeField (auto_now)

Methods:
  - get_full_name()
  - get_role_display()
  - __str__(): returns username
```

### Resident Model (residents)
```python
Fields:
  - id: AutoField
  - first_name: CharField
  - last_name: CharField
  - date_of_birth: DateField
  - admission_date: DateField
  - medical_info: TextField
  - emergency_contact: CharField
  - allergies: TextField
  - status: CharField (choices: ACTIVE, ARCHIVED, DISCHARGED)
  - created_by: ForeignKey(CustomUser)
  - created_at: DateTimeField (auto_now_add)
  - updated_at: DateTimeField (auto_now)
  - archived_at: DateTimeField (nullable)
  - archived_by: ForeignKey(CustomUser, nullable)

Methods:
  - get_full_name()
  - get_age()
  - archive()
  - unarchive()
  - __str__(): returns full_name
```

### CarePlan Model (careplans)
```python
Fields (UK Standard 10 Sections):
  - id: AutoField
  - resident: OneToOneField(Resident)
  - section_1_personal_details: TextField
  - section_2_care_needs: TextField
  - section_3_health_conditions: TextField
  - section_4_medications: TextField
  - section_5_communication: TextField
  - section_6_nutrition: TextField
  - section_7_mobility: TextField
  - section_8_personal_hygiene: TextField
  - section_9_mental_health: TextField
  - section_10_social_activities: TextField
  - status: CharField (choices: ACTIVE, ARCHIVED, COMPLETED)
  - created_by: ForeignKey(CustomUser)
  - created_at: DateTimeField (auto_now_add)
  - updated_at: DateTimeField (auto_now)

Methods:
  - archive()
  - unarchive()
  - get_status_display()
  - __str__(): returns f"Care Plan for {resident}"
```

### Handover Model (handovers)
```python
Fields:
  - id: AutoField
  - resident: ForeignKey(Resident)
  - date: DateField
  - shift: CharField (choices: MORNING, AFTERNOON, NIGHT)
  - priority: CharField (choices: LOW, MEDIUM, HIGH, URGENT)
  - details: TextField
  - notes: TextField
  - is_completed: BooleanField (default=False)
  - completed_at: DateTimeField (nullable)
  - completed_by: ForeignKey(CustomUser, nullable)
  - created_by: ForeignKey(CustomUser)
  - created_at: DateTimeField (auto_now_add)
  - updated_at: DateTimeField (auto_now)

Methods:
  - mark_complete()
  - get_priority_color()
  - __str__(): returns f"Handover {resident} - {date}"
```

### Incident Model (incidents)
```python
Fields:
  - id: AutoField
  - resident: ForeignKey(Resident)
  - incident_type: CharField (choices: FALL, INJURY, MEDICATION, BEHAVIOR, OTHER)
  - title: CharField
  - description: TextField
  - date_time: DateTimeField
  - location: CharField
  - reported_by: ForeignKey(CustomUser)
  - is_resolved: BooleanField (default=False)
  - resolved_at: DateTimeField (nullable)
  - resolved_by: ForeignKey(CustomUser, nullable)
  - resolution_notes: TextField (nullable)
  - created_at: DateTimeField (auto_now_add)
  - updated_at: DateTimeField (auto_now)

Methods:
  - resolve()
  - unresolve()
  - get_type_display()
  - days_since_incident()
  - __str__(): returns title
```

### AuditLog Model (audit)
```python
Fields:
  - id: AutoField
  - user: ForeignKey(CustomUser)
  - action: CharField (choices: 16 actions like CREATE, UPDATE, DELETE, etc.)
  - content_type: ForeignKey(ContentType)
  - object_id: CharField
  - model_name: CharField
  - changes_summary: TextField
  - timestamp: DateTimeField (auto_now_add)

Methods:
  - get_action_display()
  - get_object_url()
  - __str__(): returns f"{action} by {user}"

Indexed Fields:
  - timestamp
  - user
  - action
```

### Model Relationships
```
CustomUser (1) ──→ (M) Resident (created_by)
           ──→ (M) CarePlan (created_by)
           ──→ (M) Handover (created_by)
           ──→ (M) Incident (reported_by)
           ──→ (M) AuditLog (user)

Resident (1) ──→ (1) CarePlan
         ──→ (M) Handover
         ──→ (M) Incident

All Models → AuditLog (via Django signals post_save)
```

---

## URL Routing

### Root Configuration (config/urls.py)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('accounts.urls')),
    path('residents/', include('residents.urls')),
    path('careplans/', include('careplans.urls')),
    path('handovers/', include('handovers.urls')),
    path('incidents/', include('incidents.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('audit/', include('audit.urls')),
]
```

### App-Level Routes

#### Accounts (accounts/urls.py)
```
/auth/login/                      → LoginView
/auth/signup/                     → SignupView
/auth/logout/                     → LogoutView
/auth/pending/                    → PendingApprovalView
/auth/pending-users/              → PendingUsersListView
/auth/pending-users/approve/<id>/ → ApproveUserView
/auth/pending-users/reject/<id>/  → RejectUserView
```

#### Residents (residents/urls.py)
```
/residents/                       → ResidentListView
/residents/archived/              → ArchivedResidentsView
/residents/create/                → ResidentCreateView
/residents/<id>/                  → ResidentDetailView
/residents/<id>/edit/             → ResidentUpdateView
/residents/<id>/archive/          → ArchiveResidentView
/residents/<id>/unarchive/        → UnarchiveResidentView
```

#### Care Plans (careplans/urls.py)
```
/careplans/                       → CarePlanListView
/careplans/archived/              → ArchivedCarePlansView
/careplans/create/                → CarePlanCreateView
/careplans/<id>/                  → CarePlanDetailView
/careplans/<id>/edit/             → CarePlanUpdateView
/careplans/<id>/archive/          → ArchiveCarePlanView
/careplans/<id>/unarchive/        → UnarchiveCarePlanView
```

#### Handovers (handovers/urls.py)
```
/handovers/                       → HandoverListView
/handovers/create/                → HandoverCreateView
/handovers/<id>/                  → HandoverDetailView
/handovers/<id>/edit/             → HandoverUpdateView
/handovers/<id>/complete/         → CompleteHandoverView
```

#### Incidents (incidents/urls.py)
```
/incidents/                       → IncidentListView
/incidents/create/                → IncidentCreateView
/incidents/<id>/                  → IncidentDetailView
/incidents/<id>/edit/             → IncidentUpdateView
/incidents/<id>/resolve/          → ResolveIncidentView
/incidents/<id>/unresolve/        → UnresolveIncidentView
```

#### Dashboard (dashboard/urls.py)
```
/dashboard/                       → DashboardHomeView
/dashboard/stats/                 → StatsView (JSON)
```

#### Audit (audit/urls.py)
```
/audit/                           → AuditLogListView
/audit/search/                    → AuditSearchView
/audit/filter/                    → AuditFilterView
```

---

## Views & Logic

### View Pattern - Class-Based Views with Decorators

#### Standard CRUD View Structure
```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
@method_decorator(approval_required, name='dispatch')
class ResidentListView(ListView):
    model = Resident
    template_name = 'residents/resident_list.html'
    context_object_name = 'residents'
    paginate_by = 10
    
    def get_queryset(self):
        # Filter by role and status
        if self.request.user.role == 'CARER':
            return Resident.objects.filter(status='ACTIVE')
        return Resident.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archived_count'] = Resident.objects.filter(status='ARCHIVED').count()
        return context
```

### Signal-Based Audit Logging

All models trigger automatic audit logging via Django signals:

```python
# residents/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from audit.models import AuditLog

@receiver(post_save, sender=Resident)
def log_resident_changes(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    AuditLog.objects.create(
        user=get_current_user(),  # from middleware
        action=action,
        content_type=ContentType.objects.get_for_model(Resident),
        object_id=instance.id,
        model_name='Resident',
        changes_summary=f"{action}: {instance.get_full_name()}"
    )
```

### Dashboard Context Aggregation

The dashboard view aggregates statistics from all models:

```python
class DashboardHomeView(LoginRequiredMixin, ApprovalRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_residents'] = Resident.objects.filter(status='ACTIVE').count()
        context['total_careplans'] = CarePlan.objects.filter(status='ACTIVE').count()
        context['pending_handovers'] = Handover.objects.filter(is_completed=False).count()
        context['unresolved_incidents'] = Incident.objects.filter(is_resolved=False).count()
        
        # Recent activity
        context['recent_activities'] = AuditLog.objects.all().order_by('-timestamp')[:5]
        context['recent_incidents'] = Incident.objects.all().order_by('-created_at')[:5]
        
        return context
```

---

## Authentication & Authorization

### Role-Based Access Control

#### CustomUser Roles
```python
ROLE_CHOICES = [
    ('MANAGER', 'Care Home Manager'),
    ('SENIOR', 'Senior Carer'),
    ('CARER', 'Carer'),
]
```

#### Permission Matrix

| Feature | Manager | Senior Carer | Carer |
|---------|---------|--------------|-------|
| View Residents | ✅ | ✅ | ✅ |
| Edit Residents | ✅ | ✅ | ❌ |
| Create Residents | ✅ | ❌ | ❌ |
| Archive Residents | ✅ | ❌ | ❌ |
| View Care Plans | ✅ | ✅ | ✅ |
| Edit Care Plans | ✅ | ✅ | ❌ |
| Create Care Plans | ✅ | ❌ | ❌ |
| View Handovers | ✅ | ✅ | ✅ |
| Complete Handovers | ✅ | ✅ | ✅ |
| Create Handovers | ✅ | ✅ | ✅ |
| View Incidents | ✅ | ✅ | ✅ |
| Report Incidents | ✅ | ✅ | ✅ |
| Resolve Incidents | ✅ | ✅ | ❌ |
| View Audit Logs | ✅ | ❌ | ❌ |
| Approve New Users | ✅ | ❌ | ❌ |

### Custom Decorators

```python
# accounts/decorators.py

def approval_required(view_func):
    """Restrict access to approved users only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_approved:
            return redirect('pending_approval')
        return view_func(request, *args, **kwargs)
    return wrapper

def role_required(allowed_roles):
    """Restrict access by role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                raise PermissionDenied()
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
```

### Authentication Flow

```
1. User submits login form
2. django-allauth authenticates credentials
3. Checks if user is approved (custom check)
4. If not approved → redirect to pending_approval page
5. If approved → create session & redirect to dashboard
6. Middleware captures current_user for audit logging
```

---

## Signals & Audit Logging

### Signal Registration (in apps.py ready() method)

```python
# residents/apps.py
def ready(self):
    import residents.signals

# careplans/apps.py
def ready(self):
    import careplans.signals

# handovers/apps.py
def ready(self):
    import handovers.signals

# incidents/apps.py
def ready(self):
    import incidents.signals
```

### Middleware for User Tracking

```python
# middleware.py
import threading

_thread_locals = threading.local()

class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.user = request.user
    
    def process_response(self, request, response):
        if hasattr(_thread_locals, 'user'):
            del _thread_locals.user
        return response

def get_current_user():
    return getattr(_thread_locals, 'user', None)
```

### Audit Actions (16 types)

```python
ACTION_CHOICES = [
    ('CREATE', 'Created'),
    ('UPDATE', 'Updated'),
    ('DELETE', 'Deleted'),
    ('ARCHIVE', 'Archived'),
    ('UNARCHIVE', 'Unarchived'),
    ('RESOLVE', 'Resolved'),
    ('UNRESOLVE', 'Unresolved'),
    ('COMPLETE', 'Completed'),
    ('APPROVE', 'Approved User'),
    ('REJECT', 'Rejected User'),
    ('ACTIVATE', 'Activated'),
    ('DEACTIVATE', 'Deactivated'),
    ('LOGIN', 'Logged In'),
    ('LOGOUT', 'Logged Out'),
    ('EXPORT', 'Exported Data'),
    ('IMPORT', 'Imported Data'),
]
```

### Automatic Audit Trail Example

```python
# When a Resident is saved:
# 1. Model.save() called
# 2. post_save signal triggered
# 3. Signal handler: log_resident_changes()
# 4. AuditLog.objects.create() adds entry
# 5. Entry includes: user, action, timestamp, changes

Before: Resident(name='John', status='ACTIVE')
After:  Resident(name='John', status='ARCHIVED')
AuditLog: user=Manager, action=ARCHIVE, model=Resident, 
          changes_summary='ARCHIVE: John Doe', timestamp=2026-02-20 10:30
```

---

## Frontend Architecture

### Template Hierarchy

```
base.html (Master template)
├── sidebar.html (Navigation tree)
├── topbar.html (Current user info)
├── footer.html (Copyright info)
│
├── auth/
│   ├── login.html
│   ├── signup.html
│   └── approval.html
│
├── residents/
│   ├── resident_list.html
│   ├── resident_detail.html
│   ├── resident_form.html
│   └── resident_archive.html
│
├── careplans/
│   ├── careplan_list.html
│   ├── careplan_detail.html
│   ├── careplan_form.html
│   └── careplan_archive.html
│
├── handovers/
│   ├── handover_list.html
│   ├── handover_detail.html
│   ├── handover_form.html
│   └── handover_complete.html
│
├── incidents/
│   ├── incident_list.html
│   ├── incident_detail.html
│   ├── incident_form.html
│   ├── incident_resolve.html
│   └── incident_unresolve.html
│
└── dashboard/
    └── home.html
```

### Static Assets

```
static/
├── css/
│   ├── style.css          (Main stylesheet)
│   │   - Base colors, typography, spacing
│   │   - Info card components (.info-card, .info-label, .info-value)
│   │   - Responsive padding classes
│   │   - Footer mt-auto for sticky footer
│   │
│   └── auth.css           (Authentication pages)
│       - Form layout (.auth-form-signup 600px width)
│       - Right sidebar authentication
│       - Scrollable container (max-height: 100vh)
│       - 2-column form layout
│       - Responsive breakpoints
│
├── js/
│   └── script.js          (Client-side logic)
│       - Placeholder fade on login (clear focus, restore blur)
│       - Form validation
│       - Dynamic interactions
│
└── fonts/
    └── Poppins/           (Typography)
```

### Design System

#### Color Palette
```css
Primary:      #007bff (Bootstrap blue)
Secondary:    #6c757d (Gray)
Success:      #28a745 (Green)
Warning:      #ffc107 (Yellow)
Danger:       #dc3545 (Red)
```

#### Typography
```
Font Family: Poppins (sans-serif)
Headings:    400-700 weight
Body:        400 weight
Mono:        Monospace (code blocks)
```

#### Responsive Breakpoints (Bootstrap 5)
```
xs: < 576px
sm: ≥ 576px
md: ≥ 768px
lg: ≥ 992px
xl: ≥ 1200px
xxl: ≥ 1400px
```

### Key Frontend Components

#### Info Card Component
```html
<div class="info-card">
    <div class="info-label">Field Name</div>
    <div class="info-value">Field Value</div>
</div>
```

#### Responsive Table
```html
<div class="table-responsive">
    <table class="table table-sm table-striped">
        <!-- Responsive columns -->
        <td class="col-lg-4 col-md-6">
```

#### Bootstrap Grid Layout
```html
<!-- 2-column responsive -->
<div class="row">
    <div class="col-md-6">Left</div>
    <div class="col-md-6">Right</div>
</div>
```

---

## Configuration

### Environment Variables (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@host/dbname

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

### Settings Configuration (config/settings.py)

```python
# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'cloudinary',
    'cloudinary_storage',
    # Local apps
    'accounts',
    'residents',
    'careplans',
    'handovers',
    'incidents',
    'dashboard',
    'audit',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'middleware.CurrentUserMiddleware',  # Custom middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Authentication
AUTH_USER_MODEL = 'accounts.CustomUser'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ['DATABASE_URL'],
        conn_max_age=600
    )
}

# Storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Pagination
PAGINATE_BY = 10
```

---

## Deployment

### Prerequisites
- Python 3.12
- PostgreSQL (Neon)
- Cloudinary account
- Server (Heroku, PythonAnywhere, VPS, etc.)

### Deployment Steps

#### 1. Environment Setup
```bash
git clone <repository>
cd carehome
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Create admin user
```

#### 3. Static Files
```bash
python manage.py collectstatic --noinput
```

#### 4. Environment Configuration
Create `.env` file with all required variables (see Configuration section)

#### 5. Local Testing
```bash
python manage.py runserver
# Access at http://127.0.0.1:8000
```

#### 6. Production Deployment

**Option A: Heroku**
```bash
heroku login
heroku create carehome-app
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

**Option B: PythonAnywhere**
- Upload files via Git
- Configure virtualenv
- Set up web app with WSGI config
- Add environment variables

**Option C: VPS (Ubuntu)**
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3.12 python3-pip postgresql nginx gunicorn

# Deploy
git clone <repo>
cd carehome
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
gunicorn config.wsgi:application
```

#### 7. Server Configuration

**Gunicorn Service** (systemd)
```ini
[Unit]
Description=Gunicorn service for CareHome
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/carehome
ExecStart=/path/to/venv/bin/gunicorn config.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

**Nginx Reverse Proxy**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/carehome/staticfiles/;
    }
}
```

### Post-Deployment Checklist
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS configured
- [ ] SECRET_KEY set (strong, unique)
- [ ] Database backed up
- [ ] Email service configured
- [ ] Cloudinary API keys verified
- [ ] SSL/HTTPS enabled
- [ ] Admin user created
- [ ] First user approved by admin
- [ ] Error logging configured

### Monitoring & Maintenance

```bash
# View logs
tail -f /var/log/gunicorn/carehome.log
tail -f /var/log/nginx/error.log

# Database backup
pg_dump -U user -h host dbname > backup.sql

# Update code
git pull origin main
python manage.py migrate
systemctl restart gunicorn

# Clear cache
python manage.py clear_cache
```

---

## Development Workflow

### Setting Up Development Environment
```bash
# Clone repository
git clone <repository>
cd carehome

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with development variables
echo "DATABASE_URL=postgresql://user:password@localhost/carehome_dev" > .env
echo "DEBUG=True" >> .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver

# Access at http://127.0.0.1:8000
```

### Creating an App
```bash
python manage.py startapp myapp
```

### Database Migrations
```bash
# Create migration files after model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# View migration status
python manage.py showmigrations

# Rollback migration
python manage.py migrate appname 0001  # Go back to specific migration
```

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test residents

# Run with verbosity
python manage.py test -v 2

# Test coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/my-feature

# Create Pull Request
# (on GitHub/GitLab)

# After merge, delete branch
git branch -d feature/my-feature
```

---

## API Endpoints Summary

### Authentication
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET/POST | `/auth/login/` | User login |
| GET/POST | `/auth/signup/` | User registration |
| GET | `/auth/logout/` | User logout |
| GET | `/auth/pending/` | Pending approval page |

### Residents (10 endpoints)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/residents/` | List residents |
| GET/POST | `/residents/create/` | Create resident |
| GET | `/residents/<id>/` | View resident detail |
| GET/POST | `/residents/<id>/edit/` | Edit resident |
| POST | `/residents/<id>/archive/` | Archive resident |
| POST | `/residents/<id>/unarchive/` | Unarchive resident |
| GET | `/residents/archived/` | View archived residents |

### Care Plans (10 endpoints)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/careplans/` | List care plans |
| GET/POST | `/careplans/create/` | Create care plan |
| GET | `/careplans/<id>/` | View care plan |
| GET/POST | `/careplans/<id>/edit/` | Edit care plan |
| POST | `/careplans/<id>/archive/` | Archive care plan |
| POST | `/careplans/<id>/unarchive/` | Unarchive care plan |
| GET | `/careplans/archived/` | View archived plans |

### Handovers (7 endpoints)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/handovers/` | List handovers |
| GET/POST | `/handovers/create/` | Create handover |
| GET | `/handovers/<id>/` | View handover |
| GET/POST | `/handovers/<id>/edit/` | Edit handover |
| POST | `/handovers/<id>/complete/` | Mark as complete |

### Incidents (8 endpoints)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/incidents/` | List incidents |
| GET/POST | `/incidents/create/` | Report incident |
| GET | `/incidents/<id>/` | View incident detail |
| GET/POST | `/incidents/<id>/edit/` | Edit incident |
| POST | `/incidents/<id>/resolve/` | Mark as resolved |
| POST | `/incidents/<id>/unresolve/` | Reopen incident |

### Dashboard (2 endpoints)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/dashboard/` | View dashboard |
| GET | `/dashboard/stats/` | Get stats (JSON) |

### Audit (3 endpoints)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/audit/` | View audit logs |
| GET | `/audit/search/` | Search audit logs |
| GET | `/audit/filter/` | Filter audit logs |

---

## Database Schema

### Tables
```sql
-- Users
users_customuser
├── id (PK)
├── email (UNIQUE)
├── username (UNIQUE)
├── password
├── first_name
├── last_name
├── role (MANAGER|SENIOR|CARER)
├── is_approved (Boolean)
├── is_active (Boolean)
├── is_staff (Boolean)
├── created_at (DateTime)
└── updated_at (DateTime)

-- Residents
residents_resident
├── id (PK)
├── first_name
├── last_name
├── date_of_birth (Date)
├── admission_date (Date)
├── medical_info (Text)
├── emergency_contact
├── allergies (Text)
├── status (ACTIVE|ARCHIVED|DISCHARGED)
├── created_by (FK → users_customuser)
├── created_at (DateTime)
├── updated_at (DateTime)
├── archived_at (DateTime, nullable)
└── archived_by (FK → users_customuser, nullable)

-- Care Plans
careplans_careplan
├── id (PK)
├── resident_id (FK → residents_resident, UNIQUE)
├── section_1_personal_details (Text)
├── section_2_care_needs (Text)
├── section_3_health_conditions (Text)
├── section_4_medications (Text)
├── section_5_communication (Text)
├── section_6_nutrition (Text)
├── section_7_mobility (Text)
├── section_8_personal_hygiene (Text)
├── section_9_mental_health (Text)
├── section_10_social_activities (Text)
├── status (ACTIVE|ARCHIVED|COMPLETED)
├── created_by (FK → users_customuser)
├── created_at (DateTime)
└── updated_at (DateTime)

-- Handovers
handovers_handover
├── id (PK)
├── resident_id (FK → residents_resident)
├── date (Date)
├── shift (MORNING|AFTERNOON|NIGHT)
├── priority (LOW|MEDIUM|HIGH|URGENT)
├── details (Text)
├── notes (Text)
├── is_completed (Boolean)
├── completed_at (DateTime, nullable)
├── completed_by (FK → users_customuser, nullable)
├── created_by (FK → users_customuser)
├── created_at (DateTime)
└── updated_at (DateTime)

-- Incidents
incidents_incident
├── id (PK)
├── resident_id (FK → residents_resident)
├── incident_type (FALL|INJURY|MEDICATION|BEHAVIOR|OTHER)
├── title
├── description (Text)
├── date_time (DateTime)
├── location
├── reported_by (FK → users_customuser)
├── is_resolved (Boolean)
├── resolved_at (DateTime, nullable)
├── resolved_by (FK → users_customuser, nullable)
├── resolution_notes (Text, nullable)
├── created_at (DateTime)
└── updated_at (DateTime)

-- Audit Logs
audit_auditlog
├── id (PK)
├── user_id (FK → users_customuser)
├── action (CREATE|UPDATE|DELETE|ARCHIVE|...)
├── content_type_id (FK → django_content_type)
├── object_id
├── model_name
├── changes_summary (Text)
└── timestamp (DateTime, indexed)

-- Foreign Keys & Indexes
CREATE INDEX idx_resident_created_by ON residents_resident(created_by_id);
CREATE INDEX idx_handover_resident ON handovers_handover(resident_id);
CREATE INDEX idx_incident_resident ON incidents_incident(resident_id);
CREATE INDEX idx_auditlog_user ON audit_auditlog(user_id);
CREATE INDEX idx_auditlog_timestamp ON audit_auditlog(timestamp);
```

---

## Testing Strategy

### Unit Tests
```python
# residents/tests.py
from django.test import TestCase
from accounts.models import CustomUser
from residents.models import Resident

class ResidentModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username='testuser',
            email='test@example.com',
            role='MANAGER'
        )
        self.resident = Resident.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth='1950-01-01',
            created_by=self.user
        )

    def test_resident_creation(self):
        self.assertEqual(self.resident.get_full_name(), 'John Doe')
        self.assertEqual(self.resident.status, 'ACTIVE')

    def test_resident_archive(self):
        self.resident.archive()
        self.assertEqual(self.resident.status, 'ARCHIVED')
```

### View Tests
```python
from django.test import TestCase, Client
from django.urls import reverse

class ResidentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='MANAGER',
            is_approved=True
        )

    def test_resident_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('resident_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'residents/resident_list.html')
```

### Integration Tests
Test signal firing, audit logging, and form submission workflows

---

## Key Dependencies

```
Django==6.0.2
django-allauth==0.61.1
django-cloudinary-storage==0.0.7
cloudinary==1.39.1
dj-database-url==2.1.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
daphne==4.0.0
python-decouple==3.8
```

---

## Performance Optimization

### Database Optimization
- Use `select_related()` for ForeignKey/OneToOne
- Use `prefetch_related()` for reverse relations
- Add indexes on frequently queried fields
- Implement pagination (10-50 items per page)

### Caching Strategy
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def dashboard_view(request):
    ...
```

### Static File Optimization
- Minify CSS and JavaScript
- Use CDN for static files
- Compress images before upload

---

## Security Best Practices

✅ **Implemented**
- CSRF protection on all forms
- SQL injection prevention (ORM)
- XSS protection (template escaping)
- Password hashing (Django default)
- Role-based access control
- Login required decorators
- Approval workflow for new users

✅ **Recommendations**
- Enable HTTPS/SSL
- Set `SECURE_SSL_REDIRECT = True`
- Use secure session cookies
- Regular security updates
- Implement rate limiting
- Use environment variables for secrets
- Regular database backups
- Monitor audit logs for suspicious activity

---

## Troubleshooting

### Common Issues

#### 1. runserver Exit Code 1
**Cause**: Port already in use or migration errors
```bash
# Change port
python manage.py runserver 127.0.0.1:8001

# Check migrations
python manage.py migrate --check

# Run migrations
python manage.py migrate
```

#### 2. Database Connection Error
**Cause**: Invalid DATABASE_URL or missing PostgreSQL
```bash
# Check .env file for DATABASE_URL
# Verify database is running
# Test connection: psql -d your_database
```

#### 3. Static Files Not Loading
```bash
python manage.py collectstatic
# Add to nginx config
location /static/ {
    alias /path/to/carehome/staticfiles/;
}
```

#### 4. Cloudinary Upload Issues
```bash
# Verify Cloudinary credentials in settings.py
# Test upload: python manage.py shell
# >>> from cloudinary.uploader import upload
# >>> upload('test.jpg')
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-20 | Initial release with 7 apps, complete audit logging, UI/UX improvements |

---

## Contact & Support

**Developer**: Care Home Development Team  
**Email**: support@carehome.local  
**Repository**: [GitHub Repository]  
**Documentation**: [Full Docs]

---

## License

[Add your license here]

---

**End of Architecture Document**

Last Updated: February 20, 2026
