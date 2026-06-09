// main.js
// Entry point: initialize router and app-wide behaviors.
import { initRouter } from './router.js?v=5';

// Init application
function initApp() {
  // Demo credentials and profile data for local development only.
  if (!localStorage.getItem('demo_email')) {
    localStorage.setItem('demo_email', 'citizen_lab10@gmail.com');
  }
  if (!localStorage.getItem('demo_password')) {
    localStorage.setItem('demo_password', 'CitizenPass123');
  }
  if (!localStorage.getItem('profile_name')) {
    localStorage.setItem('profile_name', 'Warga');
  }
  if (!localStorage.getItem('profile_email')) {
    localStorage.setItem('profile_email', 'warga@example.com');
  }

  // Start router (adds event listeners and renders initial route)
  initRouter();
}

// Run app
initApp();
