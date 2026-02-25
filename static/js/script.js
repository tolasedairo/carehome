// ===== Main JavaScript File =====

document.addEventListener('DOMContentLoaded', function() {
    console.log('CareHome Management System Loaded');

    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebarBackdrop = document.querySelector('.sidebar-backdrop');

    if (sidebar && sidebarToggle && sidebarBackdrop) {
        const closeSidebar = () => {
            sidebar.classList.remove('active');
            sidebarBackdrop.classList.remove('active');
        };

        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            sidebarBackdrop.classList.toggle('active');
        });

        sidebarBackdrop.addEventListener('click', closeSidebar);

        window.addEventListener('resize', () => {
            if (window.innerWidth >= 768) {
                closeSidebar();
            }
        });
    }

    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetSelector = this.getAttribute('href');
            if (!targetSelector || targetSelector === '#') {
                return;
            }
            const target = document.querySelector(targetSelector);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add active state to navigation links
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });
});

// Utility function to format dates
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Utility function to show toast notifications
function showToast(message, type = 'info') {
    const alertClass = `alert alert-${type}`;
    const alertElement = document.createElement('div');
    alertElement.classList.add('alert', `alert-${type}`, 'alert-dismissible', 'fade', 'show');
    alertElement.setAttribute('role', 'alert');
    alertElement.innerHTML = `
        <i class="fas fa-info-circle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.insertBefore(alertElement, mainContent.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertElement);
            bsAlert.close();
        }, 5000);
    }
}

// Confirm delete action
function confirmDelete(message = 'Are you sure you want to delete this?') {
    return confirm(message);
}
