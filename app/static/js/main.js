// Main JavaScript for ViewNow application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize code highlighting
    if (typeof hljs !== 'undefined') {
        hljs.highlightAll();
    }
    
    // Handle form submission to ensure HTML content is captured
    const htmlForm = document.querySelector('form[action*="create_snippet"]');
    if (htmlForm) {
        htmlForm.addEventListener('submit', function(e) {
            const editor = document.getElementById('editor');
            const htmlContent = document.getElementById('html_content');
            
            if (editor && htmlContent) {
                htmlContent.value = editor.innerText;
                
                // Basic validation
                if (!htmlContent.value.trim()) {
                    e.preventDefault();
                    alert('请输入HTML代码');
                    return false;
                }
            }
        });
    }
    
    // Initialize copy buttons
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const target = this.getAttribute('data-copy-target');
            const element = document.querySelector(target);
            
            if (element) {
                const textArea = document.createElement('textarea');
                textArea.value = element.innerText || element.value;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                // Show feedback
                const originalText = this.innerText;
                this.innerText = '已复制!';
                setTimeout(() => {
                    this.innerText = originalText;
                }, 2000);
            }
        });
    });
});
