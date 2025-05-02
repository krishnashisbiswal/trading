/**
 * Admin Sidebar Navigation JavaScript
 * For Arthavidya Trading Community
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
});

/**
 * Initialize all sidebar functionality
 */
function initializeSidebar() {
    setupSubmenuToggles();
    expandActiveSubmenu();
    setupMobileToggle();
}

/**
 * Setup submenu toggle buttons
 */
function setupSubmenuToggles() {
    const submenuToggles = document.querySelectorAll('.submenu-toggle');
    
    submenuToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            
            const parentLi = this.parentElement;
            const submenu = this.nextElementSibling;
            
            // Toggle active class
            parentLi.classList.toggle('active');
            
            // Toggle submenu visibility
            if (submenu.style.display === 'none' || submenu.style.display === '') {
                submenu.style.display = 'block';
                // Rotate arrow icon
                this.querySelector('.submenu-indicator').style.transform = 'translateY(-50%) rotate(90deg)';
            } else {
                submenu.style.display = 'none';
                // Reset arrow icon
                this.querySelector('.submenu-indicator').style.transform = 'translateY(-50%)';
            }
        });
    });
}

/**
 * Automatically expand submenu for active menu items
 */
function expandActiveSubmenu() {
    // Find all active submenu items
    const activeSubItems = document.querySelectorAll('.submenu li.active');
    
    activeSubItems.forEach(item => {
        // Get the parent menu item and its submenu
        const parentMenu = item.closest('.submenu').parentElement;
        const submenu = item.closest('.submenu');
        
        // Add active class to parent and show submenu
        parentMenu.classList.add('active');
        submenu.style.display = 'block';
        
        // Rotate the arrow icon
        const indicator = parentMenu.querySelector('.submenu-indicator');
        if (indicator) {
            indicator.style.transform = 'translateY(-50%) rotate(90deg)';
        }
    });
}

/**
 * Setup mobile sidebar toggle button
 */
function setupMobileToggle() {
    const sidebarToggleBtn = document.querySelector('.sidebar-toggle');
    const adminSidebar = document.querySelector('.admin-sidebar');
    
    // If toggle button exists
    if (sidebarToggleBtn && adminSidebar) {
        sidebarToggleBtn.addEventListener('click', function() {
            adminSidebar.classList.toggle('mobile-active');
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 992) {
                if (!adminSidebar.contains(e.target) && !sidebarToggleBtn.contains(e.target)) {
                    adminSidebar.classList.remove('mobile-active');
                }
            }
        });
    }
}

/**
 * Helper function to close all submenus
 */
function closeAllSubmenus() {
    const submenus = document.querySelectorAll('.submenu');
    const submenuToggles = document.querySelectorAll('.submenu-toggle');
    
    submenus.forEach(submenu => {
        submenu.style.display = 'none';
    });
    
    submenuToggles.forEach(toggle => {
        toggle.parentElement.classList.remove('active');
        const indicator = toggle.querySelector('.submenu-indicator');
        if (indicator) {
            indicator.style.transform = 'translateY(-50%)';
        }
    });
}

/**
 * Public method to refresh sidebar state
 * Can be called after dynamic content changes
 */
function refreshSidebar() {
    closeAllSubmenus();
    expandActiveSubmenu();
}