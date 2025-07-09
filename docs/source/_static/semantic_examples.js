// JavaScript for SPROCLIB interactive examples

document.addEventListener('DOMContentLoaded', function() {
    // Add interactive functionality for code examples
    console.log('SPROCLIB documentation loaded');
    
    // Add copy buttons to code blocks
    const codeBlocks = document.querySelectorAll('pre');
    codeBlocks.forEach(function(block) {
        const button = document.createElement('button');
        button.className = 'copy-btn';
        button.textContent = 'Copy';
        button.style.position = 'absolute';
        button.style.top = '5px';
        button.style.right = '5px';
        button.style.fontSize = '12px';
        button.style.padding = '2px 6px';
        
        block.style.position = 'relative';
        block.appendChild(button);
        
        button.addEventListener('click', function() {
            navigator.clipboard.writeText(block.textContent);
            button.textContent = 'Copied!';
            setTimeout(() => button.textContent = 'Copy', 2000);
        });
    });
});
