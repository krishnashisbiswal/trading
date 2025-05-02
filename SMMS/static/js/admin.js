/**
 * Admin Dashboard JavaScript for Arthavidya Trading Community
 * Created: April 2025
 */

document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar on mobile
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const adminSidebar = document.querySelector('.admin-sidebar');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            adminSidebar.classList.toggle('active');
        });
    }
    
    // Toggle dropdown menus
    const dropdownToggles = document.querySelectorAll('.profile-btn, .notification-btn');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.stopPropagation();
            const dropdown = this.nextElementSibling;
            const isActive = dropdown.style.display === 'block';
            
            // Close all dropdowns
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.style.display = 'none';
            });
            
            // Toggle current dropdown
            if (!isActive) {
                dropdown.style.display = 'block';
            }
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        const dropdowns = document.querySelectorAll('.dropdown-menu');
        dropdowns.forEach(dropdown => {
            dropdown.style.display = 'none';
        });
    });
    
    // Toggle sidebar submenu
    const submenuToggles = document.querySelectorAll('.submenu-toggle');
    
    submenuToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const submenu = this.nextElementSibling;
            const isActive = submenu.style.display === 'block';
            
            // Toggle active class on toggle button
            this.classList.toggle('active');
            
            // Toggle submenu visibility
            if (isActive) {
                submenu.style.display = 'none';
            } else {
                submenu.style.display = 'block';
            }
        });
    });
    
    // Mark notifications as read
    const markAllRead = document.querySelector('.mark-all-read');
    
    if (markAllRead) {
        markAllRead.addEventListener('click', function(e) {
            e.preventDefault();
            const unreadNotifications = document.querySelectorAll('.notification-item.unread');
            unreadNotifications.forEach(notification => {
                notification.classList.remove('unread');
            });
            
            // Update notification badge
            const badge = document.querySelector('.notifications .badge');
            if (badge) {
                badge.textContent = '0';
                badge.style.display = 'none';
            }
        });
    }
    
    // Initialize all charts
    initializeCharts();
    
    // Handle date range picker functionality
    const dateRangePicker = document.querySelector('.date-range');
    
    if (dateRangePicker) {
        dateRangePicker.addEventListener('click', function() {
            // This would normally open a date picker
            // For this demo, we'll just show an alert
            alert('Date range picker would open here');
        });
    }
    
    // Card selection functionality
    const programCards = document.querySelectorAll('.program-card');
    
    if (programCards.length > 0) {
        programCards.forEach(card => {
            card.addEventListener('click', function() {
                programCards.forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
            });
        });
    }
    
    // Payment option selection
    const paymentOptions = document.querySelectorAll('.payment-option');
    
    if (paymentOptions.length > 0) {
        paymentOptions.forEach(option => {
            option.addEventListener('click', function() {
                const radioInput = this.querySelector('input[type="radio"]');
                radioInput.checked = true;
                
                paymentOptions.forEach(opt => opt.classList.remove('selected'));
                this.classList.add('selected');
            });
        });
    }
    
    // Add row highlight on hover
    const tableRows = document.querySelectorAll('.admin-table tr');
    
    if (tableRows.length > 0) {
        tableRows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = 'var(--bg-light)';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });
    }
    
    // Filter functionality for tables
    const tableFilter = document.getElementById('table-filter');
    
    if (tableFilter) {
        tableFilter.addEventListener('input', function() {
            const filterValue = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('.admin-table tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(filterValue)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
    
    // Bulk action checkbox functionality
    const bulkSelectAll = document.getElementById('bulk-select-all');
    
    if (bulkSelectAll) {
        bulkSelectAll.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.bulk-select-item');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            
            // Update bulk action button state
            const bulkActionBtn = document.querySelector('.bulk-action-btn');
            if (bulkActionBtn) {
                bulkActionBtn.disabled = !this.checked;
            }
        });
        
        // Individual checkbox change handler
        const individualCheckboxes = document.querySelectorAll('.bulk-select-item');
        individualCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const allChecked = Array.from(individualCheckboxes).every(cb => cb.checked);
                const anyChecked = Array.from(individualCheckboxes).some(cb => cb.checked);
                
                bulkSelectAll.checked = allChecked;
                
                // Update bulk action button state
                const bulkActionBtn = document.querySelector('.bulk-action-btn');
                if (bulkActionBtn) {
                    bulkActionBtn.disabled = !anyChecked;
                }
            });
        });
    }
});

/**
 * Initialize all charts on the dashboard
 */
function initializeCharts() {
    // Revenue & Enrollments Chart
    initializeRevenueChart();
    
    // Demographics Chart
    initializeDemographicsChart();
    
    // Regional Distribution Chart
    initializeRegionalChart();
}

/**
 * Initialize the Revenue & Enrollments Chart
 */
function initializeRevenueChart() {
    const revenueChartCanvas = document.getElementById('revenueChart');
    
    if (revenueChartCanvas) {
        const ctx = revenueChartCanvas.getContext('2d');
        
        // Sample data for the last month
        const labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
        const revenueData = [285000, 425000, 375000, 510000];
        const enrollmentsData = [24, 36, 29, 42];
        
        // Chart configuration
        const revenueChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Revenue (₹)',
                        data: revenueData,
                        backgroundColor: 'rgba(11, 87, 164, 0.7)',
                        borderColor: 'rgba(11, 87, 164, 1)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Enrollments',
                        data: enrollmentsData,
                        type: 'line',
                        backgroundColor: 'rgba(203, 10, 60, 0.1)',
                        borderColor: 'rgba(203, 10, 60, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(203, 10, 60, 1)',
                        tension: 0.4,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Revenue (₹)'
                        },
                        ticks: {
                            callback: function(value) {
                                return '₹' + value / 1000 + 'K';
                            }
                        }
                    },
                    y1: {
                        beginAtZero: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Enrollments'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.datasetIndex === 0) {
                                    label += '₹' + context.raw.toLocaleString();
                                } else {
                                    label += context.raw;
                                }
                                return label;
                            }
                        }
                    }
                }
            }
        });
        
        // Handle chart range change
        const revenueChartRange = document.getElementById('revenue-chart-range');
        
        if (revenueChartRange) {
            revenueChartRange.addEventListener('change', function() {
                const range = this.value;
                let newLabels, newRevenueData, newEnrollmentsData;
                
                switch (range) {
                    case 'week':
                        newLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
                        newRevenueData = [41000, 38500, 42300, 39800, 54600, 33200, 28400];
                        newEnrollmentsData = [3, 4, 5, 3, 6, 2, 2];
                        break;
                    case 'month':
                        newLabels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
                        newRevenueData = [285000, 425000, 375000, 510000];
                        newEnrollmentsData = [24, 36, 29, 42];
                        break;
                    case 'quarter':
                        newLabels = ['Jan', 'Feb', 'Mar'];
                        newRevenueData = [1450000, 1620000, 1595000];
                        newEnrollmentsData = [122, 135, 131];
                        break;
                    case 'year':
                        newLabels = ['Q1', 'Q2', 'Q3', 'Q4'];
                        newRevenueData = [4665000, 5120000, 4890000, 5240000];
                        newEnrollmentsData = [388, 428, 409, 437];
                        break;
                }
                
                revenueChart.data.labels = newLabels;
                revenueChart.data.datasets[0].data = newRevenueData;
                revenueChart.data.datasets[1].data = newEnrollmentsData;
                revenueChart.update();
            });
        }
    }
}

/**
 * Initialize the Demographics Chart
 */
function initializeDemographicsChart() {
    const demographicsChartCanvas = document.getElementById('demographicsChart');
    
    if (demographicsChartCanvas) {
        const ctx = demographicsChartCanvas.getContext('2d');
        
        // Sample data
        const demographicsChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['18-24', '25-34', '35-44', '45-54', '55+'],
                datasets: [{
                    data: [15, 42, 28, 10, 5],
                    backgroundColor: [
                        'rgba(11, 87, 164, 0.8)',
                        'rgba(25, 31, 69, 0.8)',
                        'rgba(203, 10, 60, 0.8)',
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(255, 193, 7, 0.8)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.raw + '%';
                            }
                        }
                    }
                },
                cutout: '65%'
            }
        });
    }
}

/**
 * Initialize the Regional Distribution Chart
 */
function initializeRegionalChart() {
    const regionalChartCanvas = document.getElementById('regionalChart');
    
    if (regionalChartCanvas) {
        const ctx = regionalChartCanvas.getContext('2d');
        
        // Sample data
        const regionalChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['North', 'South', 'East', 'West', 'Central', 'International'],
                datasets: [{
                    label: 'Students',
                    data: [680, 920, 470, 540, 350, 210],
                    backgroundColor: [
                        'rgba(11, 87, 164, 0.7)',
                        'rgba(25, 31, 69, 0.7)',
                        'rgba(203, 10, 60, 0.7)',
                        'rgba(40, 167, 69, 0.7)',
                        'rgba(255, 193, 7, 0.7)',
                        'rgba(23, 162, 184, 0.7)'
                    ],
                    borderWidth: 0,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Students'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                },
                barThickness: 30
            }
        });
    }
}

/**
 * Format currency values
 * @param {number} value - The value to format
 * @returns {string} Formatted currency value
 */
function formatCurrency(value) {
    if (value >= 100000) {
        return '₹' + (value / 100000).toFixed(1) + 'L';
    } else if (value >= 1000) {
        return '₹' + (value / 1000).toFixed(1) + 'K';
    } else {
        return '₹' + value;
    }
}

/**
 * Format date values
 * @param {Date} date - The date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
    const options = { day: 'numeric', month: 'short', year: 'numeric' };
    return date.toLocaleDateString('en-IN', options);
}

/**
 * Handle file uploads with preview
 * @param {HTMLElement} fileInput - The file input element
 * @param {HTMLElement} previewContainer - The container for the preview
 */
function handleFileUpload(fileInput, previewContainer) {
    fileInput.addEventListener('change', function() {
        previewContainer.innerHTML = '';
        
        if (this.files && this.files[0]) {
            const file = this.files[0];
            const reader = new FileReader();
            
            reader.onload = function(e) {
                const filePreview = document.createElement('div');
                filePreview.className = 'preview-item';
                
                if (file.type.startsWith('image/')) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    filePreview.appendChild(img);
                } else {
                    const icon = document.createElement('i');
                    icon.className = 'fas fa-file';
                    filePreview.appendChild(icon);
                }
                
                const fileName = document.createElement('span');
                fileName.textContent = file.name;
                filePreview.appendChild(fileName);
                
                previewContainer.appendChild(filePreview);
            };
            
            reader.readAsDataURL(file);
        }
    });
}