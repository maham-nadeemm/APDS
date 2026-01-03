// Main JavaScript for Operations & Monitoring System

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    initializeDate();
    initializeNotifications();
    initializeMenuToggle();
    initializeGlowEffects();
    initializeButtonAnimations();
});

// Initialize current date
function initializeDate() {
    const dateElement = document.getElementById('currentDate');
    if (dateElement) {
        const now = new Date();
        dateElement.textContent = now.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
}

// Initialize notifications
function initializeNotifications() {
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationsPanel = document.getElementById('notificationsPanel');
    const notificationsList = document.getElementById('notificationsList');
    const notificationBadge = document.getElementById('notificationBadge');
    const markAllReadBtn = document.getElementById('markAllRead');
    
    if (!notificationBtn || !notificationsPanel) return;
    
    // Toggle notifications panel
    notificationBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        notificationsPanel.classList.toggle('active');
        loadNotifications();
    });
    
    // Close panel when clicking outside
    document.addEventListener('click', function(e) {
        if (!notificationsPanel.contains(e.target) && !notificationBtn.contains(e.target)) {
            notificationsPanel.classList.remove('active');
        }
    });
    
    // Load notifications
    function loadNotifications() {
        fetch('/api/notifications?unread_only=true')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateNotificationBadge(data.data.length);
                    renderNotifications(data.data);
                }
            })
            .catch(error => {
                console.error('Error loading notifications:', error);
            });
    }
    
    // Update notification badge
    function updateNotificationBadge(count) {
        if (notificationBadge) {
            notificationBadge.textContent = count;
            notificationBadge.style.display = count > 0 ? 'flex' : 'none';
        }
    }
    
    // Render notifications
    function renderNotifications(notifications) {
        if (!notificationsList) return;
        
        if (notifications.length === 0) {
            notificationsList.innerHTML = '<div class="empty-state">No notifications</div>';
            return;
        }
        
        notificationsList.innerHTML = notifications.map(notif => {
            const timeAgo = getTimeAgo(notif.created_at);
            const unreadClass = notif.is_read ? '' : 'unread';
            return `
                <div class="notification-item ${unreadClass}" onclick="markNotificationRead(${notif.id})">
                    <h4>${notif.title}</h4>
                    <p>${notif.message}</p>
                    <div class="notification-time">${timeAgo}</div>
                </div>
            `;
        }).join('');
    }
    
    // Mark all as read
    if (markAllReadBtn) {
        markAllReadBtn.addEventListener('click', function() {
            fetch('/api/notifications/read-all', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadNotifications();
                    showToast('All notifications marked as read', 'success');
                }
            });
        });
    }
    
    // Load unread count on page load
    fetch('/api/notifications/unread-count')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateNotificationBadge(data.count);
            }
        });
    
    // Refresh notifications every 30 seconds
    setInterval(loadNotifications, 30000);
}

// Mark notification as read
function markNotificationRead(notificationId) {
    fetch(`/api/notifications/${notificationId}/read`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Reload notifications
            const notificationBtn = document.getElementById('notificationBtn');
            if (notificationBtn) {
                notificationBtn.click();
            }
        }
    });
}

// Initialize menu toggle for mobile
function initializeMenuToggle() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
}

// Toast notification system
function showToast(message, type = 'info') {
    // Remove existing toast
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type} show`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

// Get time ago string
function getTimeAgo(dateString) {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) {
        return 'Just now';
    } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else {
        const days = Math.floor(diffInSeconds / 86400);
        return `${days} day${days > 1 ? 's' : ''} ago`;
    }
}

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = '#ef4444';
        } else {
            field.style.borderColor = '';
        }
    });
    
    return isValid;
}

// Confirm dialog helper
function confirmAction(message) {
    return confirm(message);
}

// Format date helper
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format datetime helper
function formatDateTime(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Initialize glow effects for cards (lightweight)
function initializeGlowEffects() {
    // Simplified - using CSS-only hover effects for better performance
    // Removed JavaScript-based glow animations
}

// Initialize button animations (lightweight)
function initializeButtonAnimations() {
    // Removed heavy ripple and pulse animations for performance
    // Buttons now use CSS-only hover effects
}

// Auto-refresh lists when page becomes visible
document.addEventListener('DOMContentLoaded', function() {
    // Check if we should refresh on load (from redirect with refresh param)
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('refresh')) {
        // Remove the refresh parameter from URL
        const newUrl = window.location.pathname;
        window.history.replaceState({}, document.title, newUrl);
        
        // Trigger a custom event that pages can listen to
        window.dispatchEvent(new CustomEvent('forceRefresh'));
    }
});

