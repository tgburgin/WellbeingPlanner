const toggleButton = document.getElementById('darkModeToggle');
const body = document.body;

const updateToggleButtonIcon = (isDarkMode) => {
    toggleButton.textContent = isDarkMode ? "☀️" : "🌙";
};

const isDarkMode = localStorage.getItem('darkMode') === 'true';
if (isDarkMode) {
    body.classList.add('dark-mode');
}
updateToggleButtonIcon(isDarkMode);

toggleButton.addEventListener('click', () => {
    const darkModeEnabled = body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', darkModeEnabled);
    updateToggleButtonIcon(darkModeEnabled);

    // Reinitialize dynamic styles for accordions
    document.querySelectorAll('.accordion-button').forEach(button => {
        if (darkModeEnabled) {
            button.style.backgroundColor = '#1e1e1e';
            button.style.color = '#e0e0e0';
        } else {
            button.style.backgroundColor = '';
            button.style.color = '';
        }
    });
});
