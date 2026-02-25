# Care Home Management System Documentation

## Project Overview
This Care Home Management System is a Django-based application designed to manage residents, care plans, incidents, handovers, and audit logging with role-based access control. It uses a custom user model with approval workflow, Cloudinary for resident images, and supports managers, senior carers, and carers.

**Core Functional Areas:**
- Authentication & Role Approval
- Resident & Care Plan Management
- Incident Reporting & Resolution
- Shift Handovers
- Audit Logging
- Dashboard Overview

**Technical Notes:**
- Built with Django 4.x, Python 3.11+  
- Uses Class-Based Views (CBVs) for most CRUD operations  
- Inline Care Plan handling in Resident Create/Update views  
- Role and approval enforcement via decorators and `CustomUser` model  
- Cloudinary for image storage  
- Audit logs record all key actions (create, update, archive/unarchive, resolve, complete)  
- Pagination and search/filtering implemented on lists  
- GitHub Projects used to track tasks per user story

---

## User Stories and Project Tasks

### 1. Manage Residents and Care Plans
**User Story:**  
As a Care Home Manager, I want to create and manage resident profiles with optional care plans so that I can maintain complete and compliant care records.

**Acceptance Criteria:**
- Residents can be created with required personal details
- Care plans can optionally be created during resident creation
- Residents can be edited by authorized users
- Residents can be archived (soft delete)
- Audit logs record create/update/archive actions
- Resident list supports search and filtering
- Care plans display structured UK-standard sections
- Only managers can archive residents

**Technical Notes:**
- Uses `ResidentCreateView`, `ResidentUpdateView`, `ResidentListView`  
- Inline Care Plan form handled in the same view  
- Audit logs recorded via `AuditLog` model  
- Manager-only actions protected by decorators

**Project Tasks:**
- [ ] Create `ResidentForm` and `CarePlanForm`
- [ ] Implement `ResidentCreateView` with inline CarePlan creation
- [ ] Implement `ResidentUpdateView` with CarePlan editing
- [ ] Implement `ResidentListView` with search, filter, and pagination
- [ ] Implement `archive_resident` and `unarchive_resident` functions
- [ ] Add audit logging for create, update, archive/unarchive actions
- [ ] Add role-based access (manager only for archive/edit)
- [ ] Write tests for resident creation, update, archive/unarchive

---

### 2. Incident Reporting and Resolution
**User Story:**  
As a Care Home Staff member, I want to create and manage incidents for residents so that all incidents are recorded, tracked, and resolved efficiently.

**Acceptance Criteria:**
- Incidents can be created for a specific resident or general
- Users can view a list of incidents with filters (resolved/open)
- Incidents can be marked as resolved
- Audit logs record all incident actions

**Technical Notes:**
- Uses `Incident` model and CBVs (`ListView`, `CreateView`, `UpdateView`)
- Incident resolution handled in `UpdateView`
- Role checks to allow only authorized users to modify

**Project Tasks:**
- [ ] Implement `IncidentCreateView` and `IncidentUpdateView`
- [ ] Implement `IncidentListView` with open/resolved filters
- [ ] Add audit logging for incident create, update, and resolve
- [ ] Write tests for incident creation, update, and resolution

---

### 3. Shift Handovers
**User Story:**  
As a Care Home Staff member, I want to create and manage shift handovers so that important resident information is passed between shifts efficiently.

**Acceptance Criteria:**
- Handovers can be created for residents or general notes
- Handovers have priority levels and shift assignment
- Handovers can be marked as completed
- Audit logs record handover actions

**Technical Notes:**
- Uses `Handover` model and CBVs (`ListView`, `CreateView`, `UpdateView`)
- Completion status managed in `UpdateView`

**Project Tasks:**
- [ ] Implement `HandoverCreateView` and `HandoverUpdateView`
- [ ] Implement `HandoverListView` with priority and shift filters
- [ ] Add audit logging for handover create, update, complete
- [ ] Write tests for handover creation and completion

---

### 4. Authentication & Role Approval
**User Story:**  
As a system administrator, I want to manage user roles and approvals so that only approved staff can access restricted features.

**Acceptance Criteria:**
- Users have roles: Manager, Senior Carer, Carer
- Only managers can approve new users
- Approval status enforced via decorators

**Technical Notes:**
- Uses `CustomUser` model extending `AbstractUser`
- Role and approval enforced in views via `approval_required` decorator

**Project Tasks:**
- [ ] Implement custom `CustomUser` model
- [ ] Implement manager approval workflow
- [ ] Apply `approval_required` decorator to restricted views
- [ ] Write tests for user creation, role assignment, and approval

---

### 5. Audit Logging
**User Story:**  
As an administrator, I want all key actions logged so that I can track changes and ensure accountability.

**Acceptance Criteria:**
- Create, update, archive, resolve, complete actions are logged
- Logs include user, timestamp, action, target model and ID
- Logs displayed in admin panel or dedicated page

**Technical Notes:**
- Uses `AuditLog` model
- Logs triggered in view `forms_valid` methods and specific action functions

**Project Tasks:**
- [ ] Implement `AuditLog` model
- [ ] Trigger logs in relevant views and functions
- [ ] Display logs in admin or dashboard
- [ ] Write tests for audit logging

---

### 6. Dashboard Overview
**User Story:**  
As a Care Home Manager, I want a dashboard overview so that I can quickly view resident stats, incidents, and handovers.

**Acceptance Criteria:**
- Display key statistics: total residents, open incidents, pending handovers
- Quick access links to residents, incidents, handovers
- Role-based content (manager sees more details)

**Technical Notes:**
- Uses CBV for dashboard (`TemplateView`)
- Data aggregated from `Resident`, `Incident`, `Handover`

**Project Tasks:**
- [ ] Implement `DashboardView`
- [ ] Aggregate and display statistics
- [ ] Apply role-based content visibility
- [ ] Write tests for dashboard data accuracy

---

## Submission Notes
- GitHub Repository includes all apps and documentation
- `CARE_HOME_DOCUMENTATION.md` included at root
- Tasks linked to GitHub Projects for clear delivery tracking
- SQLite DB (`test_db.sqlite3`) ignored in `.gitignore`  

---
