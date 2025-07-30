// Additional JavaScript for Noah123d documentation

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Mermaid
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({
            startOnLoad: true,
            theme: document.body.getAttribute('data-md-color-scheme') === 'slate' ? 'dark' : 'default',
            themeVariables: {
                primaryColor: '#673ab7',
                primaryTextColor: '#fff',
                primaryBorderColor: '#9c27b0',
                lineColor: '#9c27b0',
                secondaryColor: '#e1bee7',
                tertiaryColor: '#f3e5f5'
            }
        });
    }
    
    // Add copy button functionality to code blocks
    addCopyButtons();
    
    // Add performance metrics highlighting
    highlightPerformanceMetrics();
    
    // Add grid layout visualization helpers
    enhanceGridExamples();
});

function addCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(function(codeBlock) {
        const pre = codeBlock.parentNode;
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = 'Copy';
        button.setAttribute('aria-label', 'Copy code to clipboard');
        
        button.addEventListener('click', function() {
            navigator.clipboard.writeText(codeBlock.textContent).then(function() {
                button.textContent = 'Copied!';
                button.classList.add('copied');
                setTimeout(function() {
                    button.textContent = 'Copy';
                    button.classList.remove('copied');
                }, 2000);
            });
        });
        
        pre.style.position = 'relative';
        pre.appendChild(button);
    });
}

function highlightPerformanceMetrics() {
    // Find performance tables and add interactive features
    const perfTables = document.querySelectorAll('.performance-table');
    
    perfTables.forEach(function(table) {
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(function(row) {
            row.addEventListener('mouseover', function() {
                row.style.backgroundColor = 'var(--noah-grid-color)';
            });
            
            row.addEventListener('mouseout', function() {
                row.style.backgroundColor = '';
            });
        });
    });
}

function enhanceGridExamples() {
    // Add visual indicators to grid layout examples
    const gridExamples = document.querySelectorAll('.grid-example');
    
    gridExamples.forEach(function(example) {
        const header = document.createElement('div');
        header.className = 'grid-example-header';
        header.innerHTML = '<strong>📐 Grid Layout Example</strong>';
        example.insertBefore(header, example.firstChild);
    });
}

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add version badge if available
if (typeof NOAH123D_VERSION !== 'undefined') {
    const versionBadge = document.createElement('span');
    versionBadge.className = 'badge-info';
    versionBadge.textContent = `v${NOAH123D_VERSION}`;
    
    const header = document.querySelector('.md-header__title');
    if (header) {
        header.appendChild(versionBadge);
    }
}
