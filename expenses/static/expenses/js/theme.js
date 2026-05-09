(function () {
    const root = document.documentElement;
    const toggleButton = document.getElementById('darkModeToggle');

    function applyTheme(mode) {
        root.setAttribute('data-bs-theme', mode);
        if (toggleButton) {
            toggleButton.textContent = mode === 'dark' ? '☀️' : '🌙';
        }
        document.dispatchEvent(new CustomEvent('themeChanged', { detail: { mode } }));
    }

    const savedTheme = localStorage.getItem('themeMode');
    applyTheme(savedTheme === 'dark' ? 'dark' : 'light');

    if (toggleButton) {
        toggleButton.addEventListener('click', function () {
            const current = root.getAttribute('data-bs-theme') === 'dark' ? 'dark' : 'light';
            const next = current === 'dark' ? 'light' : 'dark';
            localStorage.setItem('themeMode', next);
            applyTheme(next);
        });
    }

    const alerts = document.querySelectorAll('.js-auto-dismiss');
    if (alerts.length > 0) {
        setTimeout(function () {
            alerts.forEach(function (alertEl) {
                alertEl.classList.add('fade');
                setTimeout(function () {
                    alertEl.remove();
                }, 350);
            });
        }, 2000);
    }
})();