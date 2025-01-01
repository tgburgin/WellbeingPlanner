const toggleButton = document.getElementById('darkModeToggle');
const body = document.body;

// Set initial button icon
const updateToggleButtonIcon = (isDarkMode) => {
    toggleButton.textContent = isDarkMode ? "☀️" : "🌙";
};

// Load initial mode from localStorage
const isDarkMode = localStorage.getItem('darkMode') === 'true';
if (isDarkMode) {
    body.classList.add('dark-mode');
}
updateToggleButtonIcon(isDarkMode);

// Toggle dark mode
toggleButton.addEventListener('click', () => {
    const darkModeEnabled = body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', darkModeEnabled);
    updateToggleButtonIcon(darkModeEnabled);
});
