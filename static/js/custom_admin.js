// Custom Admin Panel JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // Force horizontal scrolling for tables
    function makeTablesScrollable() {
        // Find all tables
        const tables = document.querySelectorAll('table');
        
        tables.forEach(table => {
            // Get or create wrapper
            let wrapper = table.parentElement;
            
            // If parent isn't already a scroll wrapper, create one
            if (!wrapper.classList.contains('table-scroll-wrapper')) {
                const scrollWrapper = document.createElement('div');
                scrollWrapper.className = 'table-scroll-wrapper';
                scrollWrapper.style.overflowX = 'auto';
                scrollWrapper.style.width = '100%';
                scrollWrapper.style.display = 'block';
                
                // Wrap the table
                table.parentNode.insertBefore(scrollWrapper, table);
                scrollWrapper.appendChild(table);
                
                console.log('✓ Made table scrollable');
            }
        });
    }
    
    // Run immediately
    makeTablesScrollable();
    
    // Run again after a short delay (for dynamically loaded content)
    setTimeout(makeTablesScrollable, 500);
    
    // Sidebar Toggle
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mainContent = document.getElementById('mainContent');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            
            // Save state to localStorage
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebarCollapsed', isCollapsed);
        });
    }
    
    // Restore sidebar state from localStorage
    const sidebarCollapsed = localStorage.getItem('sidebarCollapsed');
    if (sidebarCollapsed === 'true') {
        sidebar.classList.add('collapsed');
    }
    
    // Category Toggle
    const categoryHeaders = document.querySelectorAll('.category-header');
    categoryHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const category = this.parentElement;
            category.classList.toggle('collapsed');
        });
    });
    
    // Table Search Functionality
    const searchInput = document.getElementById('searchTables');
    const menuItems = document.querySelectorAll('.menu-item');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            menuItems.forEach(item => {
                const tableName = item.querySelector('.item-name');
                if (tableName) {
                    const text = tableName.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        item.classList.remove('hidden');
                    } else {
                        item.classList.add('hidden');
                    }
                }
            });
            
            // Show message if no results
            const visibleItems = document.querySelectorAll('.menu-item:not(.hidden)');
            if (visibleItems.length === 0 && searchTerm !== '') {
                showNoResults();
            } else {
                hideNoResults();
            }
        });
    }
    
    // Highlight active menu item
    const currentPath = window.location.pathname;
    menuItems.forEach(item => {
        const link = item.querySelector('a');
        if (link && link.getAttribute('href') === currentPath) {
            item.classList.add('active');
            
            // Expand parent category if in one
            const parentCategory = item.closest('.menu-category');
            if (parentCategory) {
                parentCategory.classList.remove('collapsed');
            }
        }
    });
    
    // Refresh button functionality
    const refreshButton = document.querySelector('.btn-icon[title="Refresh"]');
    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            this.classList.add('loading');
            location.reload();
        });
    }
    
    // Mobile menu toggle
    if (window.innerWidth <= 768) {
        const menuToggle = document.createElement('button');
        menuToggle.className = 'mobile-menu-toggle';
        menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
        menuToggle.style.cssText = 'position: fixed; top: 20px; left: 20px; z-index: 1001; background: var(--primary-color); color: white; border: none; padding: 10px 15px; border-radius: 6px; cursor: pointer;';
        
        document.body.appendChild(menuToggle);
        
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
        
        // Close sidebar when clicking outside on mobile
        mainContent.addEventListener('click', function() {
            if (sidebar.classList.contains('show')) {
                sidebar.classList.remove('show');
            }
        });
    }
    
    // Smooth scroll to top
    const contentWrapper = document.querySelector('.content-wrapper');
    if (contentWrapper) {
        const scrollTopBtn = document.createElement('button');
        scrollTopBtn.className = 'scroll-to-top';
        scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
        scrollTopBtn.style.cssText = 'position: fixed; bottom: 30px; right: 30px; background: var(--primary-color); color: white; border: none; padding: 12px 16px; border-radius: 50%; cursor: pointer; display: none; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4); transition: all 0.3s; z-index: 999;';
        
        document.body.appendChild(scrollTopBtn);
        
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollTopBtn.style.display = 'block';
            } else {
                scrollTopBtn.style.display = 'none';
            }
        });
        
        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        
        scrollTopBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        scrollTopBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    }
    
    // Add tooltips for collapsed sidebar
    const addTooltips = () => {
        if (sidebar.classList.contains('collapsed')) {
            menuItems.forEach(item => {
                const link = item.querySelector('a');
                const span = item.querySelector('span');
                if (link && span) {
                    link.setAttribute('title', span.textContent);
                }
            });
        }
    };
    
    sidebarToggle?.addEventListener('click', addTooltips);
    addTooltips();
    
    // Helper functions
    function showNoResults() {
        let noResultsMsg = document.querySelector('.no-results-message');
        if (!noResultsMsg) {
            noResultsMsg = document.createElement('div');
            noResultsMsg.className = 'no-results-message';
            noResultsMsg.style.cssText = 'padding: 20px; text-align: center; color: rgba(255, 255, 255, 0.5); font-size: 14px;';
            noResultsMsg.innerHTML = '<i class="fas fa-search" style="font-size: 24px; margin-bottom: 10px; display: block;"></i>No tables found';
            document.querySelector('.menu-items').appendChild(noResultsMsg);
        }
    }
    
    function hideNoResults() {
        const noResultsMsg = document.querySelector('.no-results-message');
        if (noResultsMsg) {
            noResultsMsg.remove();
        }
    }
    
    // Add animation to table rows
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach((row, index) => {
        row.style.animation = `fadeIn 0.3s ease ${index * 0.02}s`;
    });
    
    // Enhance action buttons
    const actionButtons = document.querySelectorAll('.btn');
    actionButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            this.appendChild(ripple);
            
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.5);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    console.log('✓ Custom Admin Panel JavaScript loaded successfully');
});

// Add ripple animation CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .btn {
        position: relative;
        overflow: hidden;
    }
`;
document.head.appendChild(style);
