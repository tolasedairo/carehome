# Screenshots Folder

This folder should contain all screenshots referenced in the main README.md

## Required Screenshots

### Feature Screenshots (save in this folder directly)

1. `login.png` - Login page showing the authentication form
2. `resident-list.png` - List of residents with search/filter functionality
3. `resident-detail.png` - Individual resident detail page
4. `careplan-form.png` - Care plan creation/edit form
5. `incident-list.png` - List of incidents
6. `handover-list.png` - List of handovers
7. `audit-log.png` - Audit log page
8. `dashboard.png` - Dashboard with metrics
9. `github-projects-board.png` - Screenshot of your GitHub Projects board

### Validation Screenshots (save in validation/ subfolder)

**HTML Validation:**
- `html-base.png`
- `html-dashboard.png`
- `html-resident-list.png`
- `html-resident-form.png`
- `html-careplan-form.png`
- `html-incident-list.png`
- `html-handover-list.png`
- `html-login.png`

**CSS Validation:**
- `css-validation.png`
- `css-auth-validation.png`

**JavaScript Validation:**
- `js-validation.png`

**Python Validation:**
- `python-residents-models.png`
- `python-residents-views.png`
- `python-residents-forms.png`

**Lighthouse Testing:**
- `lighthouse-desktop-dashboard.png`
- `lighthouse-desktop-residents.png`
- `lighthouse-mobile-dashboard.png`
- `lighthouse-mobile-residents.png`

**WAVE Accessibility:**
- `wave-dashboard.png`
- `wave-resident-form.png`

## How to Take Screenshots

### For Feature Screenshots:
1. Run your Django development server
2. Login as different user roles to show functionality
3. Navigate to each page
4. Use browser's screenshot tool or Snipping Tool (Windows) / Screenshot (Mac)
5. Save with the exact filename listed above

### For Validation Screenshots:
1. Visit the validation tools:
   - HTML: https://validator.w3.org/
   - CSS: https://jigsaw.w3.org/css-validator/
   - JavaScript: https://jshint.com/
   - Python: https://pep8ci.herokuapp.com/
   - Lighthouse: Chrome DevTools > Lighthouse tab
   - WAVE: https://wave.webaim.org/

2. Run validation on your code/pages
3. Take screenshot showing "No errors" or validation results
4. Save in the validation/ subfolder

## Tips

- Use consistent screenshot dimensions (1920x1080 for desktop views)
- Show realistic data (not placeholder text)
- Ensure screenshots are clear and readable
- Show success messages where applicable
- Capture different user roles accessing the system
