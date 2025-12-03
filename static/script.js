// JavaScript for Book Tracker Application

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions
    const deleteForms = document.querySelectorAll('form[action*="/delete/"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const bookTitle = form.closest('tr').querySelector('td:nth-child(2)').textContent;
            if (!confirm(`Are you sure you want to delete "${bookTitle}"?`)) {
                e.preventDefault();
            }
        });
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// Optional: Add smooth scroll behavior
document.documentElement.style.scrollBehavior = 'smooth';
