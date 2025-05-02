/**
 * Arthavidya Trading Community - Admin Dashboard
 * Main JavaScript file for the admin dashboard
 */

document.addEventListener('DOMContentLoaded', function() {
    // Toggle submenu on click
    const submenuToggles = document.querySelectorAll('.submenu-toggle');
    
    submenuToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            
            const parentLi = this.parentElement;
            const submenu = this.nextElementSibling;
            
            // Check if parent is active
            const isActive = parentLi.classList.contains('active');
            
            // If not active, add active class and show submenu
            if (!isActive) {
                parentLi.classList.add('active');
                submenu.style.maxHeight = submenu.scrollHeight + 'px';
                submenu.style.opacity = '1';
            } else {
                // If already active and submenu is visible, hide it
                parentLi.classList.remove('active');
                submenu.style.maxHeight = '0';
                submenu.style.opacity = '0';
            }
        });
    });
    
    // Automatically expand submenu for active items
    const activeSubmenuItems = document.querySelectorAll('.submenu li.active');
    
    activeSubmenuItems.forEach(item => {
        const parentLi = item.parentElement.parentElement;
        const submenu = item.parentElement;
        
        parentLi.classList.add('active');
        submenu.style.maxHeight = submenu.scrollHeight + 'px';
        submenu.style.opacity = '1';
    });
    
    // Profile dropdown toggle
    const profileBtn = document.querySelector('.profile-btn');
    const profileMenu = document.querySelector('.profile-menu');
    
    if (profileBtn && profileMenu) {
        profileBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            profileMenu.classList.toggle('show');
        });
        
        // Close profile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!profileBtn.contains(e.target) && !profileMenu.contains(e.target)) {
                profileMenu.classList.remove('show');
            }
        });
    }
    
    // Notification dropdown toggle
    const notificationBtn = document.querySelector('.notification-btn');
    const notificationMenu = document.querySelector('.notification-menu');
    
    if (notificationBtn && notificationMenu) {
        notificationBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            notificationMenu.classList.toggle('show');
        });
        
        // Close notification menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!notificationBtn.contains(e.target) && !notificationMenu.contains(e.target)) {
                notificationMenu.classList.remove('show');
            }
        });
    }
    
    // Mark all notifications as read
    const markAllReadBtn = document.querySelector('.mark-all-read');
    if (markAllReadBtn) {
        markAllReadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const unreadNotifications = document.querySelectorAll('.notification-item.unread');
            unreadNotifications.forEach(notification => {
                notification.classList.remove('unread');
            });
            
            // Update badge count
            const badge = document.querySelector('.notification-btn .badge');
            badge.textContent = '0';
        });
    }
    
    // General confirmation for delete actions
    const deleteButtons = document.querySelectorAll('.action-btn.delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Initialize charts if any
    initializeCharts();
});

/**
 * Initialize charts on the dashboard
 */
function initializeCharts() {
    // Revenue Chart (if exists on the page)
    const revenueChartEl = document.getElementById('revenueChart');
    if (revenueChartEl) {
        const revenueChart = new Chart(revenueChartEl, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [
                    {
                        label: 'Revenue (₹L)',
                        data: [9.2, 10.5, 11.8, 12.6, 10.8, 11.4, 13.2, 12.8, 14.1, 15.3, 14.8, 16.2],
                        borderColor: '#0b57a4',
                        backgroundColor: 'rgba(11, 87, 164, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Enrollments',
                        data: [180, 210, 225, 245, 200, 215, 260, 240, 275, 295, 280, 310],
                        borderColor: '#cb0a3c',
                        backgroundColor: 'rgba(203, 10, 60, 0)',
                        tension: 0.4,
                        borderDash: [5, 5]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            drawBorder: false
                        }
                    },
                    x: {
                        grid: {
                            display: false,
                            drawBorder: false
                        }
                    }
                }
            }
        });
    }
    
    // Demographics Chart (if exists on the page)
    const demographicsChartEl = document.getElementById('demographicsChart');
    if (demographicsChartEl) {
        const demographicsChart = new Chart(demographicsChartEl, {
            type: 'doughnut',
            data: {
                labels: ['18-24', '25-34', '35-44', '45-54', '55+'],
                datasets: [{
                    data: [15, 42, 28, 10, 5],
                    backgroundColor: [
                        '#0b57a4',
                        '#3498db',
                        '#cb0a3c',
                        '#f39c12',
                        '#7f8c8d'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }
    
    // Regional Chart (if exists on the page)
    const regionalChartEl = document.getElementById('regionalChart');
    if (regionalChartEl) {
        const regionalChart = new Chart(regionalChartEl, {
            type: 'bar',
            data: {
                labels: ['North', 'South', 'East', 'West', 'Central', 'International'],
                datasets: [{
                    label: 'Students by Region',
                    data: [720, 850, 490, 680, 345, 210],
                    backgroundColor: [
                        'rgba(11, 87, 164, 0.7)',
                        'rgba(46, 204, 113, 0.7)',
                        'rgba(203, 10, 60, 0.7)',
                        'rgba(241, 196, 15, 0.7)',
                        'rgba(155, 89, 182, 0.7)',
                        'rgba(52, 152, 219, 0.7)'
                    ],
                    borderColor: [
                        'rgba(11, 87, 164, 1)',
                        'rgba(46, 204, 113, 1)',
                        'rgba(203, 10, 60, 1)',
                        'rgba(241, 196, 15, 1)',
                        'rgba(155, 89, 182, 1)',
                        'rgba(52, 152, 219, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

/**
 * Handle the bulk actions
 */
function setupBulkActions() {
    const bulkActions = document.getElementById('bulk-actions');
    const selectAllCheckbox = document.getElementById('select-all');
    const rowCheckboxes = document.querySelectorAll('.row-checkbox');
    const selectedCount = document.getElementById('selected-count');
    
    // Skip if these elements don't exist on the page
    if (!bulkActions || !selectAllCheckbox || rowCheckboxes.length === 0) {
        return;
    }
    
    selectAllCheckbox.addEventListener('change', function() {
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
        
        updateBulkActions();
    });
    
    rowCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateBulkActions();
            
            // Update select all checkbox
            if (!this.checked) {
                selectAllCheckbox.checked = false;
            } else {
                const allChecked = Array.from(rowCheckboxes).every(c => c.checked);
                selectAllCheckbox.checked = allChecked;
            }
        });
    });
    
    function updateBulkActions() {
        const checkedCount = document.querySelectorAll('.row-checkbox:checked').length;
        
        if (checkedCount > 0) {
            bulkActions.classList.add('show');
            selectedCount.textContent = checkedCount;
        } else {
            bulkActions.classList.remove('show');
        }
    }
}

/**
 * Set up filter dropdown functionality
 */
function setupFilterDropdown() {
    const filterBtn = document.getElementById('filter-btn');
    const filterDropdown = document.getElementById('filter-dropdown');
    
    if (!filterBtn || !filterDropdown) {
        return;
    }
    
    filterBtn.addEventListener('click', function() {
        filterDropdown.classList.toggle('show');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        if (!filterBtn.contains(event.target) && !filterDropdown.contains(event.target)) {
            filterDropdown.classList.remove('show');
        }
    });
    
    // Reset filters
    const resetBtn = filterDropdown.querySelector('.btn-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            const filterSelects = filterDropdown.querySelectorAll('select');
            filterSelects.forEach(select => {
                select.selectedIndex = 0;
            });
        });
    }
}

// Call setup functions
document.addEventListener('DOMContentLoaded', function() {
    setupBulkActions();
    setupFilterDropdown();
});