# CareHome Management System - User Stories

**Project**: CareHome Management System  
**Version**: 1.0.0  
**Last Updated**: February 28, 2026  
**Status**: All user stories completed ✅

---

## Table of Contents

1. [Authentication & User Management](#authentication--user-management)
   - [US1: User Registration & Approval](#us1-user-registration--approval)
   - [US2: Role-Based Access Control](#us2-role-based-access-control)

2. [Resident Management](#resident-management)
   - [US3: Create & Manage Residents](#us3-create--manage-residents)
   - [US4: Archive & Restore Residents](#us4-archive--restore-residents)
   - [US5: Search & Filter Residents](#us5-search--filter-residents)

3. [Care Plan Management](#care-plan-management)
   - [US6: UK-Standard Care Plans](#us6-uk-standard-care-plans)

4. [Incident Reporting](#incident-reporting)
   - [US7: Report & Track Incidents](#us7-report--track-incidents)

5. [Shift Handovers](#shift-handovers)
   - [US8: Manage Shift Handovers](#us8-manage-shift-handovers)

6. [Audit & Accountability](#audit--accountability)
   - [US9: Comprehensive Audit Trail](#us9-comprehensive-audit-trail)

7. [Dashboard](#dashboard)
   - [US10: System Overview Dashboard](#us10-system-overview-dashboard)

---

## Authentication & User Management

### US1: User Registration & Approval

**User Story:**
```
As a        new staff member
I want      to register for an account with my assigned role
So that     I can access the system after manager approval
```

**Priority**: Must Have 🔴  
**Estimated Effort**: 8 story points  
**Status**: ✅ COMPLETED  
**Sprint**: Sprint 1 - Project Setup & Authentication

#### Acceptance Criteria

1. ✅ New users can register with username, email, password, and role selection
2. ✅ New accounts are created in an unapproved state by default
3. ✅ Only users with MANAGER role can approve pending accounts
4. ✅ Unapproved users cannot access the system beyond the login page
5. ✅ Unapproved users receive a notification that their account is pending approval
6. ✅ User approval actions are logged in the audit trail
7. ✅ Approved users received email confirmation (configured)
8. ✅ Managers receive notifications of pending approval requests

#### Tasks

- [ ] Create CustomUser model extending Django AbstractUser
  - [ ] Add ROLE_CHOICES enum (MANAGER, SENIOR, CARER)
  - [ ] Add is_approved BooleanField (default=False)
  - [ ] Add __str__ method for user representation
  
- [ ] Create registration form with role selection
  - [ ] Extend django-allauth signup form
  - [ ] Add role dropdown field (MANAGER, SENIOR, CARER)
  - [ ] Implement form validation
  - [ ] Set is_approved=False on account creation
  
- [ ] Create manager approval view
  - [ ] Create list view of unapproved users
  - [ ] Add approve button functionality
  - [ ] Add decline/remove user functionality
  - [ ] Restrict access to MANAGER role only
  
- [ ] Add audit logging for user approvals
  - [ ] Create signal handler for user approval
  - [ ] Log USER_APPROVAL action with timestamp and manager name
  
- [ ] Create pending approval notification page
  - [ ] Display message when unapproved user logs in
  - [ ] Show expected approval timeframe
  
- [ ] Configure email notifications
  - [ ] Set up EMAIL_BACKEND in settings
  - [ ] Create approval notification email template
  - [ ] Send confirmation email on successful registration

---

### US2: Role-Based Access Control

**User Story:**
```
As a        care home manager
I want      different permission levels for different roles
So that     data is secure and staff only access appropriate features
```

**Priority**: Must Have 🔴  
**Estimated Effort**: 13 story points  
**Status**: ✅ COMPLETED  
**Sprint**: Sprint 1 - Project Setup & Authentication

#### Acceptance Criteria

1. ✅ MANAGER role has full CRUD access to all features
2. ✅ SENIOR role can Create and Update but cannot Archive/Delete
3. ✅ CARER role has View-only access to most features
4. ✅ Permission decorators enforce authorization on all views
5. ✅ Unauthorized access attempts are blocked with 403 error
6. ✅ Unauthorized access attempts are logged in audit trail
7. ✅ Menu and navigation items hidden based on user role
8. ✅ Form fields are read-only for restricted roles

#### Tasks

- [ ] Create permission decorators
  - [ ] Create @manager_required decorator
  - [ ] Create @senior_or_manager_required decorator
  - [ ] Create @approved_required decorator
  - [ ] Create proper error handling and redirects
  
- [ ] Define role-based permissions matrix
  - [ ] Document MANAGER permissions (all features)
  - [ ] Document SENIOR permissions (create/edit only)
  - [ ] Document CARER permissions (view only)
  
- [ ] Apply decorators to all views
  - [ ] Apply @approved_required to all protected views
  - [ ] Apply role-specific decorators based on feature
  - [ ] Test authorization on all endpoints
  
- [ ] Update templates for role-based visibility
  - [ ] Hide create/edit/delete buttons for CARER users
  - [ ] Hide archive buttons for non-MANAGER users
  - [ ] Show role-appropriate navigation menu items
  - [ ] Disable form inputs for read-only roles
  
- [ ] Add role indicators in UI
  - [ ] Display user role in header/profile area
  - [ ] Show permission level on forms
  
- [ ] Test unauthorized access scenarios
  - [ ] Test CARER attempting to archive resident (should fail)
  - [ ] Test SENIOR attempting to approve user (should fail)
  - [ ] Test unapproved user accessing dashboard (should fail)
  - [ ] Verify 403 errors and redirects

---

## Resident Management

### US3: Create & Manage Residents

**User Story:**
```
As a        care home manager
I want      to create and manage resident profiles
So that     I can maintain accurate and up-to-date records
```

**Priority**: Must Have 🔴  
**Estimated Effort**: 13 story points  
**Status**: ✅ COMPLETED  
**Sprint**: Sprint 2 - Resident Management

#### Acceptance Criteria

1. ✅ Residents can be created with personal details (first name, last name, DOB, gender, room number)
2. ✅ Emergency contact information (name, phone) can be stored with each resident
3. ✅ Medical notes section for recording health information
4. ✅ Profile pictures can be uploaded via Cloudinary CDN
5. ✅ Care plans can optionally be created inline during resident creation
6. ✅ Resident details can be edited by authorized users (MANAGER/SENIOR)
7. ✅ System tracks created_by user and creation/update timestamps
8. ✅ All create and update actions are logged to audit trail
9. ✅ Residents remain searchable even after archival
10. ✅ Profile pictures are served over HTTPS (secure)

#### Tasks

- [ ] Create Resident model
  - [ ] Add personal fields: first_name, last_name, date_of_birth, gender
  - [ ] Add contact fields: emergency_contact_name, emergency_contact_phone
  - [ ] Add medical_notes TextField
  - [ ] Add room_number CharField
  - [ ] Add profile_picture CloudinaryField
  - [ ] Add created_by ForeignKey to CustomUser
  - [ ] Add created_at, updated_at timestamps
  - [ ] Add is_active flag for archive functionality
  - [ ] Add __str__ method
  
- [ ] Create Resident form
  - [ ] Create ResidentForm with all relevant fields
  - [ ] Add custom validation (DOB cannot be in future)
  - [ ] Add empty_permitted=True for optional fields
  - [ ] Style with crispy-forms and Bootstrap
  
- [ ] Create CreateView
  - [ ] Create ResidentCreateView with form
  - [ ] Add inline CarePlan form (inline_formset)
  - [ ] Implement forms_valid() to save both models
  - [ ] Add @manager_required decorator
  - [ ] Add success message
  - [ ] Redirect to resident_detail on success
  
- [ ] Create UpdateView
  - [ ] Create ResidentUpdateView
  - [ ] Allow editing of all fields
  - [ ] Add @manager_or_senior_required decorator
  - [ ] Add success message
  
- [ ] Create DetailView
  - [ ] Display all resident information
  - [ ] Show profile picture if available
  - [ ] Show linked care plans
  - [ ] Show linked incidents
  - [ ] Show linked handovers
  
- [ ] Implement profile picture upload
  - [ ] Configure Cloudinary integration
  - [ ] Set up secure URL enforcement (HTTPS)
  - [ ] Add profile_picture_url property for HTTPS fallback
  - [ ] Test image display on detail page
  
- [ ] Add audit logging for resident actions
  - [ ] Log CREATE_RESIDENT on resident creation
  - [ ] Log UPDATE_RESIDENT on resident updates
  - [ ] Include user, timestamp, and changes in log

---

### US4: Archive & Restore Residents

**User Story:**
```
As a        care home manager
I want      to archive residents who have left the care home
So that     records are preserved but don't clutter the active resident list
```

**Priority**: Must Have 🔴  
**Estimated Effort**: 8 story points  
**Status**: ✅ COMPLETED  
**Sprint**: Sprint 2 - Resident Management

#### Acceptance Criteria

1. ✅ Only MANAGER role users can archive residents
2. ✅ Archived residents do not appear in the default resident list
3. ✅ Archived residents can be viewed in a separate "Archived Residents" list
4. ✅ Only MANAGER users can restore archived residents
5. ✅ Archive/restore actions are logged to audit trail
6. ✅ Confirmation dialog shown before archiving to prevent accidents
7. ✅ Archived residents retain all historical data
8. ✅ Linked records (care plans, incidents) remain accessible for archived residents

#### Tasks

- [ ] Add archive functionality to ResidentListView
  - [ ] Add filter to exclude is_active=False from default list
  - [ ] Add "Archived Residents" view that shows is_active=False
  - [ ] Add archive button to resident detail page
  
- [ ] Create archive_resident view
  - [ ] Create archive button with confirmation dialog
  - [ ] Set is_active=False on resident
  - [ ] Add @manager_required decorator
  - [ ] Add success message
  - [ ] Log ARCHIVE_RESIDENT to audit trail
  - [ ] Redirect to resident list
  
- [ ] Create unarchive_resident view
  - [ ] Create restore button on archived resident detail page
  - [ ] Set is_active=True on resident
  - [ ] Add @manager_required decorator
  - [ ] Add success message
  - [ ] Log UNARCHIVE_RESIDENT to audit trail
  
- [ ] Update archived resident display
  - [ ] Show archived status badge/indicator
  - [ ] Reduce opacity or gray out archived residents in lists
  - [ ] Add "Restore" button on archived resident detail page
  
- [ ] Update related records
  - [ ] Ensure care plans remain accessible for archived residents
  - [ ] Ensure incidents remain linked to archived residents
  - [ ] Ensure handovers still display for archived residents
  
- [ ] Add audit logging
  - [ ] Log ARCHIVE_RESIDENT action with user and timestamp
  - [ ] Log UNARCHIVE_RESIDENT action with user and timestamp

---

### US5: Search & Filter Residents

**User Story:**
```
As a        care staff member
I want      to search and filter the resident list
So that     I can quickly find specific residents
```

**Priority**: Should Have 🟡  
**Estimated Effort**: 5 story points  
**Status**: ✅ COMPLETED  
**Sprint**: Sprint 2 - Resident Management

#### Acceptance Criteria

1. ✅ Search by resident name (first name or last name) functionality
2. ✅ Filter by active/archived status
3. ✅ Pagination for large resident lists (10-20 per page)
4. ✅ Results update dynamically without full page reload
5. ✅ Search is case-insensitive
6. ✅ Empty search returns all active residents
7. ✅ Search results show resident count
8. ✅ Results maintain user's filter and page state when opening detail view

#### Tasks

- [ ] Add search field to resident list template
  - [ ] Add search input box in list header
  - [ ] Submit via GET request with ?search= parameter
  
- [ ] Implement search in ResidentListView
  - [ ] Filter queryset by first_name__icontains or last_name__icontains
  - [ ] Preserve search term in context for template display
  - [ ] Pass search parameter to pagination links
  
- [ ] Add status filter
  - [ ] Add filter dropdown or radio buttons (Active/Archived/All)
  - [ ] Filter queryset on is_active field
  - [ ] Default to Active residents
  - [ ] Preserve filter state in pagination
  
- [ ] Implement pagination
  - [ ] Use Django Paginator (10-20 items per page)
  - [ ] Add first/previous/next/last navigation
  - [ ] Show current page number
  - [ ] Show total count of residents
  
- [ ] Update URL pattern
  - [ ] Support ?search=name parameter
  - [ ] Support ?status=active|archived parameter
  - [ ] Support ?page=N parameter

---

## Care Plan Management

### US6: UK-Standard Care Plans

**User Story:**
```
As a        senior carer
I want      to create structured care plans with UK-standard sections
So that     care delivery meets regulatory requirements
```

**Priority**: Must Have 🔴  
**Estimated Effort**: 13 story points  
**Status**: ✅ COMPLETED  
**Sprint**: Sprint 2 - Resident Management

#### Acceptance Criteria

1. ✅ Care plans include 10 key UK-standard sections:
   - Assessment Summary
   - Personal Care
   - Mobility
   - Nutrition
   - Medication
   - Communication
   - Wellbeing
   - Skin Integrity
   - Daily Routine
   - Safeguarding Risks

2. ✅ Care plans can be created inline during resident creation
3. ✅ Care plans can be created independently for existing residents
4. ✅ Care plans can be edited by authorized users (MANAGER/SENIOR)
5. ✅ Review date can be set for care plan reviews
6. ✅ Care plans can be archived/unarchived
7. ✅ All create, update, archive actions are logged to audit trail
8. ✅ Only SENIOR and MANAGER roles can create care plans
9. ✅ Care plans remain linked to resident after archival

#### Tasks

- [ ] Create CarePlan model with 10 sections
  - [ ] Add ForeignKey to Resident
  - [ ] Add TextField for each of 10 sections
  - [ ] Add title field (default "Care Plan")
  - [ ] Add review_date DateField
  - [ ] Add created_by ForeignKey
  - [ ] Add created_at, updated_at timestamps
  - [ ] Add is_active flag for archiving
  - [ ] Add __str__ method
  
- [ ] Create CarePlan form
  - [ ] Create CarePlanForm with all 10 section fields
  - [ ] Add review_date field with date picker
  - [ ] Style with crispy-forms and Bootstrap
  - [ ] Make all fields optional (blank=True allowed)
  
- [ ] Create inline CarePlan form for resident creation
  - [ ] Use InlineFormSet to embed care plan in resident form
  - [ ] Allow creation of care plan at same time as resident
  - [ ] Display 10 sections in clear layout
  
- [ ] Create CarePlanCreateView
  - [ ] Create view for creating care plan for existing resident
  - [ ] Add @senior_or_manager_required decorator
  - [ ] Pass resident_id in URL
  - [ ] Add success message
  
- [ ] Create CarePlanUpdateView
  - [ ] Allow editing of all 10 sections
  - [ ] Add @senior_or_manager_required decorator
  - [ ] Add success message
  
- [ ] Create CarePlanDetailView
  - [ ] Display all 10 sections
  - [ ] Show review date
  - [ ] Show created_by and creation date
  - [ ] Show status (active/archived)
  
- [ ] Create CarePlanListView for resident
  - [ ] Show all care plans linked to resident
  - [ ] Show active and archived care plans
  - [ ] Show review date for each plan
  - [ ] Add create and edit links
  
- [ ] Add archive functionality
  - [ ] Add archive button on detail page
  - [ ] Create archive_careplan view
  - [ ] Create unarchive button for archived plans
  
- [ ] Add audit logging
  - [ ] Log CREATE_CAREPLAN
  - [ ] Log UPDATE_CAREPLAN
  - [ ] Log ARCHIVE_CAREPLAN
  - [ ] Log UNARCHIVE_CAREPLAN

---

## Incident Reporting

### US7: Report & Track Incidents

**User Story:**
```
As a        care staff member
I want      to report incidents related to residents
So that     safety issues are documented and tracked
```

**Priority**: Must Have 🔴  
**Estimated Effort**: 10 story points  
**Status**: ✅ COMPLETED  
**Sprint**: Sprint 3 - Incidents & Handovers

#### Acceptance Criteria

1. ✅ Incident types: Fall, Medication Error, Behavioural Incident, Other
2. ✅ Incidents can be created with detailed description
3. ✅ Incidents can be linked to a specific resident (optional)
4. ✅ General incidents can be created without resident linkage
5. ✅ Incidents can be marked as resolved by authorized users
6. ✅ Filter incidents by resolved/open status
7. ✅ All staff can create incidents
8. ✅ Only MANAGER/SENIOR can mark as resolved
9. ✅ All incident actions are logged to audit trail
10. ✅ Incident list shows most recent first

#### Tasks

- [ ] Create Incident model
  - [ ] Add INCIDENT_TYPE_CHOICES: Fall, Medication Error, Behavioural, Other
  - [ ] Add incident_type CharField
  - [ ] Add ForeignKey to Resident (optional, null=True)
  - [ ] Add description TextField
  - [ ] Add is_resolved BooleanField (default=False)
  - [ ] Add created_by ForeignKey to CustomUser
  - [ ] Add created_at timestamp
  - [ ] Add updated_at timestamp
  - [ ] Add __str__ method
  
- [ ] Create IncidentForm
  - [ ] Add incident_type dropdown
  - [ ] Add incident_type dropdown
  - [ ] Add resident dropdown (optional)
  - [ ] Add description field
  - [ ] Style with crispy-forms
  
- [ ] Create IncidentCreateView
  - [ ] Create form for new incident
  - [ ] Allow pre-selection of resident from URL
  - [ ] Allow general incidents (no resident)
  - [ ] Add success message
  - [ ] Log CREATE_INCIDENT
  
- [ ] Create IncidentListView
  - [ ] Show all incidents ordered by newest first
  - [ ] Add filter by resident (if accessing from resident detail)
  - [ ] Add filter by status (open/resolved)
  - [ ] Add pagination
  - [ ] Highlight unresolved incidents
  - [ ] Show quick resolve button
  
- [ ] Create IncidentDetailView
  - [ ] Display all incident details
  - [ ] Show resident (if linked)
  - [ ] Show created_by user
  - [ ] Show creation timestamp
  - [ ] Show resolve button (if not resolved)
  
- [ ] Create resolve_incident view
  - [ ] Create button to mark as resolved
  - [ ] Add @senior_or_manager_required decorator
  - [ ] Update is_resolved=True
  - [ ] Add success message
  - [ ] Log RESOLVE_INCIDENT
  
- [ ] Create incident widget for dashboard
  - [ ] Show total open incidents
  - [ ] Show incidents by type (pie chart)
  - [ ] Show recent incidents list
  
- [ ] Add audit logging
  - [ ] Log CREATE_INCIDENT with type and description
  - [ ] Log RESOLVE_INCIDENT with resolution time

---

## Shift Handovers

### US8: Manage Shift Handovers

**User Story:**
```
As a        care staff member
I want      to create and complete shift handovers
So that     important information is communicated between shifts
```

**Priority**: Must Have 🔴  
**Estimated Effort**: 10 story points  
**Status**: ✅ COMPLETED  
**Sprint**: Sprint 3 - Incidents & Handovers

#### Acceptance Criteria

1. ✅ Handovers include: Title, Shift, Priority, Notes, Resident (optional)
2. ✅ Shift types: Morning, Afternoon, Night
3. ✅ Priority levels: Low, Normal, High, Urgent
4. ✅ Handovers can be resident-specific or general
5. ✅ Handovers can be marked as completed
6. ✅ Filter handovers by shift type
7. ✅ Filter handovers by priority level
8. ✅ Only MANAGER can delete handovers
9. ✅ All handover actions are logged to audit trail
10. ✅ Priority indicated with color coding (Low=Green, Normal=Blue, High=Orange, Urgent=Red)

#### Tasks

- [ ] Create Handover model
  - [ ] Add title CharField
  - [ ] Add SHIFT_CHOICES: Morning, Afternoon, Night
  - [ ] Add shift CharField
  - [ ] Add PRIORITY_CHOICES: Low, Normal, High, Urgent
  - [ ] Add priority CharField
  - [ ] Add notes TextField
  - [ ] Add ForeignKey to Resident (optional)
  - [ ] Add is_completed BooleanField (default=False)
  - [ ] Add created_by ForeignKey
  - [ ] Add created_at, updated_at timestamps
  - [ ] Add __str__ method
  
- [ ] Create HandoverForm
  - [ ] Add title field
  - [ ] Add shift dropdown
  - [ ] Add priority dropdown
  - [ ] Add resident dropdown (optional)
  - [ ] Add notes textarea
  - [ ] Style with crispy-forms
  
- [ ] Create HandoverCreateView
  - [ ] Create form for new handover
  - [ ] Allow pre-selection of resident from URL
  - [ ] Add success message
  - [ ] Log CREATE_HANDOVER
  
- [ ] Create HandoverListView
  - [ ] Show all handovers
  - [ ] Add filter by shift (Morning/Afternoon/Night)
  - [ ] Add filter by priority (Low/Normal/High/Urgent)
  - [ ] Add pagination
  - [ ] Show uncompleted handovers first
  - [ ] Add color coding for priority levels
  - [ ] Add quick "Mark Complete" button
  
- [ ] Create HandoverDetailView
  - [ ] Display all handover details
  - [ ] Show resident (if linked)
  - [ ] Show priority with color
  - [ ] Show creation timestamp
  - [ ] Show complete button
  
- [ ] Create complete_handover view
  - [ ] Create button to mark as completed
  - [ ] Update is_completed=True
  - [ ] Add success message
  - [ ] Log COMPLETE_HANDOVER
  
- [ ] Create handover widget for dashboard
  - [ ] Show pending handovers count
  - [ ] Show high/urgent priority handovers
  - [ ] Show handovers for current shift
  
- [ ] Add audit logging
  - [ ] Log CREATE_HANDOVER
  - [ ] Log UPDATE_HANDOVER
  - [ ] Log COMPLETE_HANDOVER

---

## Audit & Accountability

### US9: Comprehensive Audit Trail

**User Story:**
```
As a        care home manager
I want      to view all system actions in an audit log
So that     I can maintain accountability and track changes
```

**Priority**: Must Have 🔴  
**Estimated Effort**: 8 story points  
**Status**: ✅ COMPLETED  
**Sprint**: Sprint 4 - Audit & Dashboard

#### Acceptance Criteria

1. ✅ All Create, Update, Archive, Resolve, Complete actions are logged
2. ✅ Logs include: User, Action Type, Timestamp, Description, Target Model
3. ✅ Logs are searchable by action type
4. ✅ Logs are filterable by date range
5. ✅ Logs are filterable by user
6. ✅ Logs are read-only (cannot be modified or deleted)
7. ✅ Manager-only access to full audit log
8. ✅ Pagination on audit log list (50 items per page)
9. ✅ Most recent actions shown first

#### Tasks

- [ ] Create AuditLog model
  - [ ] Add ForeignKey to CustomUser
  - [ ] Add ACTION_CHOICES with 17 action types
  - [ ] Add action CharField
  - [ ] Add target_model CharField (model name)
  - [ ] Add target_id IntegerField (model ID)
  - [ ] Add timestamp DateTimeField
  - [ ] Add description TextField
  - [ ] Add indexes for common queries
  - [ ] Add __str__ method
  
- [ ] Define action types
  - [ ] CREATE_RESIDENT, UPDATE_RESIDENT, ARCHIVE_RESIDENT, UNARCHIVE_RESIDENT
  - [ ] CREATE_CAREPLAN, UPDATE_CAREPLAN, ARCHIVE_CAREPLAN, UNARCHIVE_CAREPLAN
  - [ ] CREATE_INCIDENT, UPDATE_INCIDENT, RESOLVE_INCIDENT
  - [ ] CREATE_HANDOVER, UPDATE_HANDOVER, COMPLETE_HANDOVER
  - [ ] USER_APPROVAL
  
- [ ] Create audit signal handlers
  - [ ] Create post_save signal for Resident
  - [ ] Create post_save signal for CarePlan
  - [ ] Create post_save signal for Incident
  - [ ] Create post_save signal for Handover
  - [ ] Create signal for user approval
  
- [ ] Implement AuditLogListView
  - [ ] Show all audit logs (MANAGER only)
  - [ ] Order by timestamp, newest first
  - [ ] Add pagination (50 per page)
  - [ ] Add filter by action type
  - [ ] Add filter by user
  - [ ] Add date range filter
  - [ ] Add search by description
  
- [ ] Create AuditLogDetailView
  - [ ] Show full audit log entry
  - [ ] Show target record if still exists
  - [ ] Show related user information
  
- [ ] Add audit log widget to admin
  - [ ] Show in Django admin interface
  - [ ] Make read-only
  - [ ] Show recent activity
  
- [ ] Add reporting views
  - [ ] Create user activity report
  - [ ] Create action type report
  - [ ] Show charts/statistics of actions over time

---

## Dashboard

### US10: System Overview Dashboard

**User Story:**
```
As a        care staff member
I want      a dashboard showing key metrics and recent activity
So that     I can quickly assess the current state of the care home
```

**Priority**: Must Have 🔴  
**Estimated Effort**: 8 story points  
**Status**: ✅ COMPLETED  
**Sprint**: Sprint 4 - Audit & Dashboard

#### Acceptance Criteria

1. ✅ Dashboard displays total active residents count
2. ✅ Dashboard displays open incidents count
3. ✅ Dashboard displays pending handovers count
4. ✅ Dashboard displays active care plans count
5. ✅ Recent activity feed shows latest 10 audit entries
6. ✅ Quick action buttons for common tasks
7. ✅ Role-appropriate data visibility (CARER sees less info)
8. ✅ Responsive design on mobile devices
9. ✅ Dashboard loads in under 2 seconds

#### Tasks

- [ ] Create Dashboard view
  - [ ] Create DashboardView inheriting TemplateView
  - [ ] Add @approved_required decorator
  - [ ] Retrieve dashboard metrics
  
- [ ] Calculate metric cards
  - [ ] Query total active residents: Resident.objects.filter(is_active=True).count()
  - [ ] Query open incidents: Incident.objects.filter(is_resolved=False).count()
  - [ ] Query pending handovers: Handover.objects.filter(is_completed=False).count()
  - [ ] Query active care plans: CarePlan.objects.filter(is_active=True).count()
  
- [ ] Create recent activity feed
  - [ ] Query latest 10 audit logs
  - [ ] Order by timestamp DESC
  - [ ] Show user, action, timestamp, description
  - [ ] Add link to related record if exists
  
- [ ] Create dashboard template
  - [ ] Display 4 metric cards in grid
  - [ ] Show recent activity list
  - [ ] Add quick action buttons
  - [ ] Style with Bootstrap cards
  
- [ ] Add quick action buttons
  - [ ] Button to create new resident
  - [ ] Button to create new incident
  - [ ] Button to create new handover
  - [ ] Button to view open incidents
  - [ ] Button to view pending handovers
  
- [ ] Implement role-based dashboard
  - [ ] CARER sees limited metrics
  - [ ] SENIOR sees medium data
  - [ ] MANAGER sees full dashboard
  
- [ ] Add homepage redirect
  - [ ] Redirect login success to dashboard
  - [ ] Redirect approved User to dashboard
  
- [ ] Optimize queries
  - [ ] Use .count() in queryset
  - [ ] Use select_related for foreign keys
  - [ ] Add caching if needed
  - [ ] Test page load time

---

## Summary by Priority

### Must Have (60%)
- US1: User Registration & Approval
- US2: Role-Based Access Control
- US3: Create & Manage Residents
- US4: Archive & Restore Residents
- US6: UK-Standard Care Plans
- US7: Report & Track Incidents
- US8: Manage Shift Handovers
- US9: Comprehensive Audit Trail
- US10: System Overview Dashboard

### Should Have (20%)
- US5: Search & Filter Residents

### Could Have (15%)
- Multi-site support
- Advanced reporting
- Medication management module
- Staff scheduling

### Won't Have (5%)
- Mobile native app
- Email notifications (future phase)
- Family portal (future phase)

---

## Definition of Done

Each user story is considered "Done" when:

✅ All acceptance criteria are met  
✅ Code is reviewed and approved  
✅ Unit tests written and passing  
✅ Manual testing completed  
✅ PEP8 compliance verified  
✅ Audit logging implemented  
✅ Documentation updated  
✅ Feature deployed to staging  
✅ Acceptance testing passed  

---

## Track Progress

Use this template to track which user stories are in progress:

| US # | Title | Status | Sprint | Assignee |
|------|-------|--------|--------|----------|
| US1 | User Registration & Approval | ✅ DONE | 1 | Tolase |
| US2 | Role-Based Access Control | ✅ DONE | 1 | Tolase |
| US3 | Create & Manage Residents | ✅ DONE | 2 | Tolase |
| US4 | Archive & Restore Residents | ✅ DONE | 2 | Tolase |
| US5 | Search & Filter Residents | ✅ DONE | 2 | Tolase |
| US6 | UK-Standard Care Plans | ✅ DONE | 2 | Tolase |
| US7 | Report & Track Incidents | ✅ DONE | 3 | Tolase |
| US8 | Manage Shift Handovers | ✅ DONE | 3 | Tolase |
| US9 | Comprehensive Audit Trail | ✅ DONE | 4 | Tolase |
| US10 | System Overview Dashboard | ✅ DONE | 4 | Tolase |

---

**Document Owner**: Tolase Dairo  
**Last Reviewed**: February 28, 2026  
**Next Review Date**: March 28, 2026
