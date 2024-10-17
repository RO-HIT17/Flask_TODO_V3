document.addEventListener('DOMContentLoaded', function() {
    const themeToggleButton = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const lightThemeLink = document.getElementById('light-theme');
    const darkThemeLink = document.getElementById('dark-theme');

    
    if (localStorage.getItem('theme') === 'dark') {
        darkThemeLink.removeAttribute('disabled');
        lightThemeLink.setAttribute('disabled', 'disabled');
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
    }

    themeToggleButton.addEventListener('click', function() {
        if (darkThemeLink.disabled) {
            
            darkThemeLink.removeAttribute('disabled');
            lightThemeLink.setAttribute('disabled', 'disabled');
            localStorage.setItem('theme', 'dark');
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon'); e
        } else {
            
            lightThemeLink.removeAttribute('disabled');
            darkThemeLink.setAttribute('disabled', 'disabled');
            localStorage.setItem('theme', 'light');
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun'); 
        }
    });

    
   
    
});