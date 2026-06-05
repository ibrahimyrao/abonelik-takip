document.addEventListener('DOMContentLoaded', () => {
  const html = document.documentElement;

  const setTheme = (theme) => {
    html.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    const mobileIcon = document.getElementById('mobileThemeIcon');
    const mobileText = document.getElementById('mobileThemeText');
    if (mobileIcon && mobileText) {
      mobileIcon.textContent = theme === 'dark' ? 'light_mode' : 'dark_mode';
      mobileText.textContent = theme === 'dark' ? 'Aydınlık Mod' : 'Karanlık Mod';
    }
  };

  const saved = localStorage.getItem('theme');
  if (saved) setTheme(saved);
  else setTheme('light');

  document.getElementById('themeToggle')?.addEventListener('click', () => {
    setTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });

  document.getElementById('mobileThemeToggle')?.addEventListener('click', () => {
    setTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });

  const hamburger = document.getElementById('hamburger');
  const overlay = document.getElementById('mobileOverlay');
  if (hamburger && overlay) {
    hamburger.addEventListener('click', () => {
      overlay.classList.toggle('open');
      const icon = hamburger.querySelector('.material-symbols-rounded');
      icon.textContent = overlay.classList.contains('open') ? 'close' : 'menu';
    });
  }

  document.querySelectorAll('[data-msg]').forEach((msg, i) => {
    setTimeout(() => {
      msg.style.transition = 'transform 0.3s, opacity 0.3s';
      msg.style.transform = 'translateX(30px)';
      msg.style.opacity = '0';
      setTimeout(() => msg.remove(), 300);
    }, 4000 + i * 600);
  });
});
