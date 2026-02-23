# CareHome Management System - User Stories

## User Story 1: Manager Creates and Manages Residents with Care Plans

### User Story

**As a** Care Home Manager  
**I want to** create new residents in the system with integrated care plans  
**So that** I can maintain a complete profile of each resident including their care requirements without navigating between multiple pages

---

### Acceptance Criteria

**Given** a manager is logged in and approved  
**When** they navigate to the Residents list page  
**Then** they should see an "Add Resident" button in the top right

**Given** a manager clicks "Add Resident"  
**When** they are directed to the resident creation form  
**Then** they should see sections for:
  - Personal Information (First Name, Last Name, DOB, Gender, Room Number, Profile Picture)
  - Emergency Contact Information (Name, Phone)
  - Medical Information (Medical Notes)
  - Care Plan Details (all 10 UK-standard sections: Assessment Summary, Personal Care, Mobility, Nutrition, Medication, Communication, Wellbeing, Skin Integrity, Daily Routine, Safeguarding Risks)

**Given** a manager fills out the resident form with all required fields  
**When** they click "Save Resident"  
**Then**:
  - A new Resident record is created in the database
  - A new CarePlan record is created and linked to the resident
  - The manager is redirected to the Residents list
  - An audit log entry is created recording the resident creation
  - The newly created resident appears exactly once in the list

**Given** a manager has created a resident  
**When** they click on the resident's name in the list  
**Then** they see a detailed view showing:
  - Resident personal details (name, DOB, room, contact info)
  - Profile picture (if uploaded)
  - Medical notes
  - Associated care plan
  - Incident history (last 10 incidents)
  - Care plans (active plans only)
  - Action buttons for Edit and Archive (for managers only)

**Given** a manager chooses to edit a resident  
**When** they click the Edit button  
**Then** they:
  - Can modify all resident fields
  - Can create or update the associated care plan
  - See the existing care plan data pre-populated if one exists
  - Can save changes and return to the resident list

**Given** a manager wants to archive a resident  
**When** they click the Archive button  
**Then**:
  - The resident's `is_active` field changes to False
  - The resident no longer appears in the active residents list
  - The resident can be found in the "Archived" residents view
  - An audit log is created
  - The resident's data is preserved (soft delete, not hard delete)

**Given** a manager is viewing the Residents list  
**When** they click the "Archived" button  
**Then** they see only archived (inactive) residents  
**And** they can unarchive residents by clicking an "Unarchive" button

**Given** a manager is creating or editing a resident  
**When** care plan fields are left empty  
**Then** no care plan record is created or updated (optional care plan creation)

---

### Technical Tasks

#### Task 1.1: Database & Model Verification
- [ ] Verify `Resident` model has fields: `first_name`, `last_name`, `date_of_birth`, `gender`, `room_number`, `emergency_contact_name`, `emergency_contact_phone`, `medical_notes`, `profile_picture`, `created_by`, `is_active`, `created_at`, `updated_at`
- [ ] Verify `CarePlan` model has fields: `resident` (ForeignKey), `title`, all 10 section fields, `review_date`, `created_by`, `is_active`, `created_at`, `updated_at`
- [ ] Verify relationship: `CarePlan` has ForeignKey to `Resident` with `related_name='care_plans'`
- [ ] Confirm migration is applied to production database

**Status**: ✅ COMPLETE

#### Task 1.2: ResidentCreateView Implementation
- [ ] Verify `ResidentCreateView` exists with proper decorators (`@login_required`, `@approval_required`, `@method_decorator`)
- [ ] Verify dispatch method restricts access to MANAGER role only
- [ ] Verify `get_context_data()` includes `CarePlanForm` 
- [ ] Verify `post()` method handles both `ResidentForm` and `CarePlanForm`
- [ ] Verify `forms_valid()` method:
  - Saves resident with `created_by = current_user`
  - Creates LinkedCarePlan if careplan form has data
  - Sets `self.object` before redirecting (fixes NoneType error)
  - Redirects to resident list with success
- [ ] Verify `_has_careplan_data()` helper checks if any careplan field is non-empty
- [ ] Verify form validation displays errors on failed submission

**Status**: ✅ COMPLETE (Fixed NoneType redirect issue)

#### Task 1.3: ResidentForm & CarePlanForm Styling
- [ ] Verify `ResidentForm` renders all fields with Bootstrap `form-control` classes
- [ ] Verify `CarePlanForm` renders all text areas with `form-control` classes
- [ ] Verify date fields use HTML5 date picker (`type="date"`)
- [ ] Verify form displays in a card container with proper spacing
- [ ] Verify form has Cancel and Save buttons with icons

**Status**: ✅ COMPLETE

#### Task 1.4: ResidentListView Deduplication
- [ ] Verify `ResidentListView.get_queryset()` includes:
  - `.annotate(incident_count=Count('incidents', distinct=True))`
  - `.annotate(open_incident_count=Count(..., filter=..., distinct=True))`
  - `.distinct()` at the end to prevent duplicate rows from JOIN operations
- [ ] Test that creating a resident shows it exactly once (not 5 times)
- [ ] Verify pagination works correctly with distinct() applied

**Status**: ✅ COMPLETE

#### Task 1.5: ResidentDetailView & ResidentUpdateView
- [ ] Verify `ResidentDetailView` shows all resident details
- [ ] Verify `ResidentDetailView` displays related incidents (last 10, ordered by -created_at)
- [ ] Verify `ResidentDetailView` shows incident counts (total and open)
- [ ] Verify `ResidentDetailView` shows active care plans
- [ ] Verify `ResidentUpdateView` allows managers to edit residents
- [ ] Verify `ResidentUpdateView` supports creating/updating associated care plan
- [ ] Verify `ResidentUpdateView.forms_valid()` saves changes and redirects

**Status**: ✅ COMPLETE

#### Task 1.6: Archive & Unarchive Functions
- [ ] Verify `archive_resident()` view function:
  - Checks user role (MANAGER only)
  - Sets `is_active = False`
  - Creates audit log
  - Redirects to resident detail
- [ ] Verify `unarchive_resident()` view function:
  - Checks user role (MANAGER only)
  - Sets `is_active = True`
  - Creates audit log
  - Redirects to resident detail
- [ ] Verify both functions only available to managers in templates

**Status**: ✅ COMPLETE

#### Task 1.7: Audit Logging Integration
- [ ] Verify `audit/signals.py` has `@receiver(post_save, sender=Resident)` decorator
- [ ] Verify signal creates `AuditLog` entry with:
  - `user = instance.created_by`
  - `action = 'CREATE_RESIDENT' or 'UPDATE_RESIDENT'`
  - `target_model = 'Resident'`
  - `target_id = instance.id`
  - `description = f"Resident {instance} created/updated"`
- [ ] Verify signal is registered in `apps.py` ready() method

**Status**: ✅ COMPLETE (Via signals.py)

#### Task 1.8: Template - resident_form.html
- [ ] Template extends `base.html`
- [ ] Shows form title: "Add New Resident" (create) or "Edit Resident" (update)
- [ ] Sections:
  - Personal Information section
  - Emergency Contact section
  - Medical Information section
  - Care Plan section (with all 10 fields)
- [ ] Shows form errors in alert boxes
- [ ] Has Cancel (back to list) and Save buttons
- [ ] Uses Bootstrap grid (row, col-md-6) for multi-column layout

**Status**: ✅ COMPLETE

#### Task 1.9: Template - resident_list.html
- [ ] Template extends `base.html`
- [ ] Shows:
  - Back to Dashboard button
  - "Residents" heading
  - Add Resident button (managers only)
  - Archived button
  - Search by name form
  - Status filter dropdown
- [ ] Displays residents in responsive table with columns:
  - Name
  - Room
  - Gender
  - Date of Birth
  - Incidents (with count and open indicator)
  - Status (Active badge)
  - Actions (View, Edit, Archive buttons - Edit/Archive for managers only)
- [ ] Paginated to 20 residents per page
- [ ] Empty state: "No residents found" when list is empty
- [ ] Shows pagination controls

**Status**: ✅ COMPLETE

#### Task 1.10: Template - resident_detail.html
- [ ] Shows resident name as heading
- [ ] Displays all resident details in readable format
- [ ] Shows profile picture (if available)
- [ ] Shows incident summary:
  - Total incident count
  - Open incident count with warning badge
- [ ] Lists last 10 incidents with type, date, and link to detail
- [ ] Shows active care plans with review date
- [ ] Edit and Archive buttons (managers only)
- [ ] Back to Residents button

**Status**: ✅ COMPLETE

#### Task 1.11: URL Routing
- [ ] Verify `residents/urls.py` includes:
  - `''` → ResidentListView (name='list')
  - `'archived/'` → ArchivedResidentListView (name='archived')
  - `'create/'` → ResidentCreateView (name='create')
  - `'<int:pk>/'` → ResidentDetailView (name='detail')
  - `'<int:pk>/edit/'` → ResidentUpdateView (name='edit')
  - `'<int:pk>/archive/'` → archive_resident function (name='archive')
  - `'<int:pk>/unarchive/'` → unarchive_resident function (name='unarchive')
- [ ] Verify `app_name = 'residents'`

**Status**: ✅ COMPLETE

#### Task 1.12: Permissions & Access Control
- [ ] Verify decorators on all views: `@login_required`, `@approval_required`
- [ ] Verify manager-only views check `request.user.role == "MANAGER"`
- [ ] Verify non-managers are redirected to resident list when trying to create/edit/archive
- [ ] Verify all templates use `{% if user.role == "MANAGER" %}` for edit/archive buttons

**Status**: ✅ COMPLETE

#### Task 1.13: Error Handling & Validation
- [ ] Verify form validation shows inline errors
- [ ] Verify date fields validate date format
- [ ] Verify emergency contact phone validates as valid phone format (optional enhancement)
- [ ] Verify profile picture upload handles errors gracefully
- [ ] Verify non-existent resident returns 404 (get_object_or_404)

**Status**: ✅ COMPLETE

#### Task 1.14: Testing
- [ ] Write unit tests for `ResidentCreateView`:
  - Test GET request returns form
  - Test POST with valid data creates resident
  - Test POST with valid data creates care plan
  - Test POST with careplan fields empty does not create careplan
  - Test non-manager cannot POST
- [ ] Write unit tests for `ResidentListView`:
  - Test manager can view all residents
  - Test carer can view all residents
  - Test search functionality works
  - Test pagination works
  - Test residents appear exactly once (no duplicates)
- [ ] Write unit tests for archive/unarchive:
  - Test manager can archive
  - Test carer cannot archive
  - Test archived resident appears in archived list only
- [ ] Write integration tests for full resident creation flow

**Status**: ⚠️ PENDING (Tests exist in residents/tests.py)

#### Task 1.15: Performance Optimization
- [ ] Verify `ResidentListView` uses `select_related()` or `prefetch_related()` for incidents
- [ ] Verify `ResidentDetailView` uses optimized queries for incidents
- [ ] Verify pagination is set to reasonable limit (20 residents)
- [ ] Test query count to ensure no N+1 problems

**Status**: ⚠️ PARTIAL (Distinct annotate added, could optimize with select_related)

---

## User Story 2: Senior Carer Views and Completes Shift Handovers

### User Story

**As a** Senior Carer  
**I want to** view pending handovers for my shift and mark them as completed  
**So that** I can ensure continuity of care and communicate important information between shifts

---

### Acceptance Criteria

**Given** a senior carer is logged in and approved  
**When** they navigate to the Handovers page  
**Then** they see a list of all handovers filtered by:
  - Handovers for their assigned shift (or all shifts)
  - Priority level (Low, Normal, High, Urgent)
  - Completion status (Pending, Completed)

**Given** a senior carer views the handover list  
**When** they see a handover record  
**Then** it displays:
  - Title
  - Assigned resident (if applicable)
  - Shift (Morning, Afternoon, Night)
  - Priority (color-coded: Green=Low, Yellow=Normal, Orange=High, Red=Urgent)
  - Completion status (badge)
  - Created date/time
  - Last updated
  - Action buttons (View, Complete, Edit if creator)

**Given** a senior carer clicks on a handover  
**When** they view the detail page  
**Then** they see:
  - Full handover title and description
  - Resident details (if linked)
  - Shift and priority with visual indicators
  - Notes
  - Creator information
  - Created and updated timestamps
  - Completion status
  - "Mark as Complete" button (if not completed)

**Given** a senior carer completes a handover  
**When** they click "Mark as Complete"  
**Then**:
  - Handover's `is_completed` changes to True
  - Completion timestamp is recorded
  - User who completed it is recorded
  - Handover moves to "Completed" section
  - An audit log entry is created
  - Success message displays

**Given** a manager creates a handover  
**When** the handover is assigned to a resident  
**Then** the resident's name and details appear in the handover view

**Given** a handover has high or urgent priority  
**When** it's displayed in the list  
**Then** it's visually emphasized (red/orange badge)

---

### Technical Tasks

#### Task 2.1: Database & Model Verification
- [ ] Verify `Handover` model has fields: `title`, `resident` (ForeignKey, nullable), `shift` (Morning/Afternoon/Night), `priority`, `notes`, `is_completed`, `created_by`, `created_at`, `updated_at`
- [ ] Verify `completed_at` and `completed_by` fields exist (or add them)
- [ ] Verify Handover can be created without a resident (nullable)
- [ ] Create migration if adding fields

**Status**: ⚠️ PARTIAL (Model exists, but `completed_at` and `completed_by` may need to be added)

#### Task 2.2: HandoverListView
- [ ] Create/verify list view is available to all approved users
- [ ] View displays handovers with pagination (20 per page)
- [ ] Add filters to GET queryset:
  - `status` filter (pending/completed)
  - `shift` filter (morning/afternoon/night)
  - `priority` filter (low/normal/high/urgent)
- [ ] Order by: priority (high first), then created_at (newest first)

**Status**: ⚠️ PENDING

#### Task 2.3: HandoverDetailView
- [ ] View accessible to all approved users
- [ ] Shows all handover details
- [ ] Shows related resident details (if applicable)
- [ ] Shows creator information
- [ ] Shows completion status with timestamp if completed
- [ ] Edit button visible only to creator/manager

**Status**: ⚠️ PENDING

#### Task 2.4: HandoverCompleteView/Function
- [ ] Create view/function to mark handover as complete
- [ ] Only accessible to approved users
- [ ] Sets `is_completed = True`
- [ ] Records `completed_at = now()`
- [ ] Records `completed_by = current_user`
- [ ] Creates audit log entry
- [ ] Redirects to handover list or detail with success message

**Status**: ⚠️ PENDING

#### Task 2.5: HandoverCreateView
- [ ] Create view allows managers to create handovers
- [ ] Non-managers redirected
- [ ] Form includes fields: title, resident (optional), shift, priority, notes
- [ ] Validates form and saves with `created_by = current_user`
- [ ] Redirects to handover list

**Status**: ⚠️ PENDING

#### Task 2.6: HandoverUpdateView
- [ ] Allow creator and managers to edit handovers
- [ ] Pre-populate form with existing data
- [ ] Save changes and redirect to list

**Status**: ⚠️ PENDING

#### Task 2.7: Template - handover_list.html
- [ ] Extends base.html
- [ ] Shows "Handovers" heading
- [ ] Shows filters: Status (Pending/Completed), Shift, Priority
- [ ] Shows Create Handover button (managers only)
- [ ] Table with columns:
  - Title
  - Resident (if linked)
  - Shift
  - Priority (color-coded badge)
  - Status (Pending/Completed)
  - Created
  - Actions (View, Complete if pending, Edit if creator)
- [ ] Pagination controls
- [ ] Empty state message

**Status**: ⚠️ PENDING

#### Task 2.8: Template - handover_detail.html
- [ ] Shows handover title as heading
- [ ] Shows all details: shift, priority, notes
- [ ] Shows resident details (if linked)
- [ ] Shows creator and timestamps
- [ ] Shows completion info (who completed, when) if completed
- [ ] "Mark as Complete" button if pending
- [ ] Edit button if user is creator/manager
- [ ] Back button to handover list

**Status**: ⚠️ PENDING

#### Task 2.9: Template - handover_form.html
- [ ] Form for create and edit
- [ ] Shows "New Handover" or "Edit Handover" heading
- [ ] Fields: Title, Resident (optional select), Shift (select), Priority (select), Notes (textarea)
- [ ] Save and Cancel buttons
- [ ] Form validation error display

**Status**: ⚠️ PENDING

#### Task 2.10: URL Routing
- [ ] Verify/create routes in `handovers/urls.py`:
  - `''` → HandoverListView (name='list')
  - `'create/'` → HandoverCreateView (name='create')
  - `'<int:pk>/'` → HandoverDetailView (name='detail')
  - `'<int:pk>/edit/'` → HandoverUpdateView (name='edit')
  - `'<int:pk>/complete/'` → HandoverCompleteView or function (name='complete')

**Status**: ⚠️ PENDING

#### Task 2.11: Audit Logging
- [ ] Signal in `handovers/signals.py` logs creation
- [ ] Signal logs on update
- [ ] Manual audit log on completion

**Status**: ⚠️ PENDING

#### Task 2.12: Testing
- [ ] Test handover list view for approved users
- [ ] Test ability to filter by status, shift, priority
- [ ] Test marking handover as complete
- [ ] Test audit logs created

**Status**: ⚠️ PENDING

---

## User Story 3: Staff Views and Reports Incidents

### User Story

**As a** Care Staff Member (Carer, Senior Carer, or Manager)  
**I want to** report incidents involving residents quickly and easily  
**So that** we maintain a complete incident record for safety, compliance, and pattern detection

---

### Acceptance Criteria

**Given** a staff member is logged in and approved  
**When** they navigate to Incidents  
**Then** they see:
  - List of all incidents ordered by newest first
  - Incidents categorized by type: Fall, Medication Error, Behavioural, Other
  - Visual indicators for resolved vs unresolved (badges)
  - Search by resident name or incident description
  - Filter by incident type
  - Filter by resolution status

**Given** a staff member clicks "Create Incident"  
**When** the incident form loads  
**Then** it shows fields for:
  - Incident Type (dropdown)
  - Resident involved (autocomplete select, optional)
  - Description (required textarea)
  - Created at timestamp (auto-filled to current time)

**Given** a staff member fills in incident details  
**When** they click "Save Incident"  
**Then**:
  - Incident is created in database
  - Reporter is recorded as the current user
  - Audit log entry is created
  - Success message displays
  - Staff member is redirected to incident list

**Given** a staff member views an incident detail  
**When** they access the detail page  
**Then** they see:
  - Incident type and description
  - Resident involved (with link to resident detail)
  - Reporter name and creation date
  - Resolution status (badge)
  - Resolution details (if resolved)
  - Who resolved it and when (if resolved)

**Given** an incident is unresolved  
**When** a staff member views it  
**Then** they see a "Mark as Resolved" button

**Given** a staff member marks an incident as resolved  
**When** they click "Mark as Resolved"  
**Then**:
  - Incident's `is_resolved` changes to True
  - Timestamp and resolver info recorded
  - Audit log created
  - Resolution status updates in list view

**Given** a staff member views an incident marked as resolved  
**When** they see resolution notes  
**Then** they can add/edit notes about the resolution

---

### Technical Tasks

#### Task 3.1: Database & Model Verification
- [ ] Verify `Incident` model has fields: `resident` (nullable FK), `incident_type`, `description`, `created_by`, `is_resolved`, `resolved_at` (nullable), `resolved_by` (nullable FK), `created_at`
- [ ] Add `resolved_at` and `resolved_by` fields if missing
- [ ] Create migration if needed

**Status**: ⚠️ PARTIAL (Model exists, resolved_at and resolved_by need verification)

#### Task 3.2: IncidentListView
- [ ] Create view for listing incidents
- [ ] Available to all approved users
- [ ] Pagination (20 per page)
- [ ] Add queryset filters:
  - `type` parameter for incident type
  - `status` parameter (resolved/unresolved)
  - `search` parameter for description search
- [ ] Order by -created_at
- [ ] Annotate with resolver info if resolved

**Status**: ⚠️ PENDING

#### Task 3.3: IncidentDetailView
- [ ] View accessible to all approved users
- [ ] Show all incident details
- [ ] Show resident details (if linked)
- [ ] Show reporter and creation timestamp
- [ ] Show resolution info (if resolved)
- [ ] "Mark as Resolved" button if unresolved

**Status**: ⚠️ PENDING

#### Task 3.4: IncidentCreateView
- [ ] Form with fields: incident_type, resident (optional), description
- [ ] Accessible to all approved users
- [ ] Auto-set `created_by = current_user`
- [ ] Validate form and save
- [ ] Redirect to incident list with success message

**Status**: ⚠️ PENDING

#### Task 3.5: IncidentUpdateView
- [ ] Allow editing incident details
- [ ] Accessible to creator and managers
- [ ] Pre-populate form

**Status**: ⚠️ PENDING

#### Task 3.6: IncidentResolveView/Function
- [ ] Create view/function to mark incident as resolved
- [ ] Set `is_resolved = True`
- [ ] Record `resolved_at = now()`
- [ ] Record `resolved_by = current_user`
- [ ] Allow optional resolution notes
- [ ] Create audit log
- [ ] Redirect with success message

**Status**: ⚠️ PENDING

#### Task 3.7: IncidentForm
- [ ] Fields: incident_type (required), resident (optional), description (required)
- [ ] Bootstrap styling

**Status**: ⚠️ PENDING

#### Task 3.8: Templates
- [ ] `incident_list.html`: Table with type, resident, reporter, status, created date
- [ ] `incident_detail.html`: Full incident details with resolve button
- [ ] `incident_form.html`: Create/edit form

**Status**: ⚠️ PENDING

#### Task 3.9: URL Routing
- [ ] Routes for list, create, detail, edit, resolve

**Status**: ⚠️ PENDING

#### Task 3.10: Audit Logging
- [ ] Log incident creation
- [ ] Log incident resolution

**Status**: ⚠️ PENDING

#### Task 3.11: Testing
- [ ] Test incident creation
- [ ] Test incident resolution
- [ ] Test incident filtering and search

**Status**: ⚠️ PENDING

---

## User Story 4: Manager Views Dashboard with Key Metrics

### User Story

**As a** Care Home Manager  
**I want to** see a dashboard with key metrics and recent activity  
**So that** I can quickly understand the current status of residents, incidents, and care quality

---

### Acceptance Criteria

**Given** a manager is logged in and approved  
**When** they navigate to the Dashboard  
**Then** they see:
  - Total number of active residents
  - Total number of active care plans
  - Number of pending handovers
  - Number of unresolved incidents
  - Recent incidents (last 5) with type, resident, and date
  - Recent handovers (with completion status)
  - Audit log (recent 10 actions by any user)
  - High/urgent priority handovers highlighted

**Given** a manager views the dashboard  
**When** they see pending handovers  
**Then** they can click to view or complete them

**Given** incidents are displayed on dashboard  
**When** an incident is unresolved  
**Then** it's highlighted in a warning color

---

### Technical Tasks

#### Task 4.1: DashboardHomeView
- [ ] Extend context data to include:
  - `total_residents`: Resident.objects.filter(is_active=True).count()
  - `total_careplans`: CarePlan.objects.filter(is_active=True).count()
  - `active_handovers`: Handover.objects.filter(is_completed=False).count()
  - `unresolved_incidents`: Incident.objects.filter(is_resolved=False).count()
  - `recent_incidents`: Incident.objects.all().order_by('-created_at')[:5]
  - `recent_handovers`: Handover.objects.all().order_by('-created_at')[:5]
  - `recent_activities`: AuditLog.objects.all().order_by('-timestamp')[:10]
  - `urgent_handovers`: Handover.objects.filter(priority='URGENT', is_completed=False)

**Status**: ⚠️ PENDING

#### Task 4.2: Template - home.html
- [ ] Display KPI cards: Total Residents, Care Plans, Pending Handovers, Unresolved Incidents
- [ ] Show recent incidents with type badge, resident link, status
- [ ] Show recent handovers with priority color
- [ ] Show audit log with user, action, timestamp
- [ ] Make clickable to navigate to detail pages

**Status**: ⚠️ PENDING

#### Task 4.3: Styling
- [ ] Use Bootstrap card layout for metrics
- [ ] Color-code priority/status badges
- [ ] Responsive design for mobile

**Status**: ⚠️ PENDING

---

## User Story 5: Manager Approves New User Registrations

### User Story

**As a** Care Home Manager  
**I want to** review and approve pending user registrations  
**So that** I can ensure only authorized personnel access the system

---

### Acceptance Criteria

**Given** a new user registers for the system  
**When** they submit their registration  
**Then** they are created with `is_approved = False`

**Given** a new user attempts to log in before approval  
**When** they submit login credentials  
**Then** they see message: "Your account is pending approval from a manager"

**Given** a manager navigates to "Pending Approvals"  
**When** they access the page  
**Then** they see:
  - List of all unapproved users
  - User name, email, role, registration date
  - Action buttons: Approve, Reject

**Given** a manager clicks "Approve" on a user  
**When** the action is confirmed  
**Then**:
  - User's `is_approved` changes to True
  - User can now log in
  - Audit log entry created
  - Success message displays

**Given** a manager clicks "Reject"  
**When** confirmed  
**Then**:
  - User's `is_active` changes to False
  - User cannot log in
  - Account data is preserved (not deleted)
  - Audit log entry created
  - Success message displays

---

### Technical Tasks

#### Task 5.1: CustomUser Model Verification
- [ ] Verify `is_approved` field exists as BooleanField(default=False)
- [ ] Verify new users are created with is_approved=False in signup

**Status**: ✅ COMPLETE

#### Task 5.2: PendingUsersListView
- [ ] Create view for managers only
- [ ] Query: CustomUser.objects.filter(is_approved=False)
- [ ] Display user list with columns: name, email, role, joined date
- [ ] Add Approve/Reject buttons

**Status**: ✅ COMPLETE

#### Task 5.3: ApproveUserView
- [ ] Set `is_approved = True`
- [ ] Create audit log
- [ ] Redirect with success message

**Status**: ✅ COMPLETE

#### Task 5.4: RejectUserView
- [ ] Set `is_active = False`
- [ ] Create audit log
- [ ] Redirect with success message

**Status**: ✅ COMPLETE

#### Task 5.5: PendingApprovalView
- [ ] Show message to users awaiting approval
- [ ] Redirect from dashboard if not approved

**Status**: ✅ COMPLETE

#### Task 5.6: Login Flow
- [ ] Check `is_approved` during login
- [ ] Redirect to pending approval page if not approved
- [ ] Show clear message

**Status**: ✅ COMPLETE (Via allauth + custom decorators)

#### Task 5.7: Templates
- [ ] `pending_users_list.html`: Table and action buttons
- [ ] `pending_approval.html`: Waiting message

**Status**: ✅ COMPLETE

---

## Summary

**Completed User Stories**: 1 (Residents), 5 (User Approval)  
**In Progress**: 2 (Handovers), 3 (Incidents), 4 (Dashboard)  
**Total Coverage**: 5/5 major features

---

## Notes & Recommendations

1. **Priority**: Focus on completing Handovers (US 2) and Incidents (US 3) to have full operational features
2. **Testing**: Each user story should have corresponding unit and integration tests
3. **Performance**: Add database indexes on frequently filtered fields (created_at, is_resolved, is_completed, priority)
4. **UI/UX**: Ensure all filters and search are intuitive and performant
5. **Mobile Responsiveness**: Test all templates on mobile devices
6. **Accessibility**: Ensure all buttons and form fields have proper labels and ARIA attributes
