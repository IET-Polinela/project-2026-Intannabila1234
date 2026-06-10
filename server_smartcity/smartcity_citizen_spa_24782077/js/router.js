// router.js
// Simple hash-based router for two routes: #login and #dashboard
import { renderLogin, setupLoginForm } from './auth.js?v=5';
import { renderDashboard, setupDashboard } from './dashboard.js?v=5';

export function handleRouting() {
  const hash = window.location.hash || '#login';
  const app = document.getElementById('app');
  const dashboardActions = document.getElementById('dashboardActions');
  const navbarToggler = document.getElementById('navbarToggler');

  if (dashboardActions) {
    dashboardActions.classList.toggle('d-none', hash !== '#dashboard');
  }
  if (navbarToggler) {
    navbarToggler.classList.toggle('d-none', hash !== '#dashboard');
  }

  if (!app) return;

  // Route handling
  if (hash === '#login') {
    app.innerHTML = renderLogin();
    setupLoginForm();
    return;
  }

  if (hash === '#dashboard') {
    const token = localStorage.getItem('access_token');
    if (!token) {
      window.location.hash = '#login';
      return;
    }

    app.innerHTML = renderDashboard();
    setupDashboard();
    return;
  }

  window.location.hash = '#login';
}

// Initialize listeners
export function initRouter() {
  handleRouting();
  window.addEventListener('hashchange', handleRouting);
}
