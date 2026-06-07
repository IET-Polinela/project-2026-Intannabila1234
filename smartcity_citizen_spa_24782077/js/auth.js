// auth.js
// Handles rendering login form and login submission.
import { requestAPI } from './api.js';

// Render the login HTML (returned as string)
export function renderLogin() {
  return `
  <div class="login-shell">
    <div class="login-card glass-card shadow-sm">
      <div class="card-body p-4 p-md-5">
        <div class="login-hero p-4 rounded-4 mb-4 text-center">
          <div class="d-flex align-items-center justify-content-center mb-3">
            <div class="badge bg-info text-dark rounded-pill p-3 shadow-sm"><i class="bi bi-building-fill fs-4"></i></div>
          </div>
          <h1 class="h3 fw-bold login-title mb-2">Smart City Portal</h1>
          <p class="text-muted mb-0">Selamat datang di portal warga. Masuk untuk melihat ringkasan layanan dan laporan Anda.</p>
        </div>

        <form id="loginForm">
          <div class="mb-3 input-group shadow-sm">
            <span class="input-group-text"><i class="bi bi-envelope"></i></span>
            <input id="loginEmail" type="email" class="form-control" placeholder="Email" required />
          </div>

          <div class="mb-3 input-group shadow-sm">
            <span class="input-group-text"><i class="bi bi-lock"></i></span>
            <input id="loginPassword" type="password" class="form-control" placeholder="Password" required />
          </div>

          <div class="d-flex flex-column flex-sm-row align-items-center justify-content-between mb-4">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="" id="rememberMe" />
              <label class="form-check-label" for="rememberMe">Remember Me</label>
            </div>
            <a href="#" class="small text-primary text-decoration-none">Forgot Password?</a>
          </div>

          <div class="d-grid mb-3">
            <button type="submit" class="btn btn-primary btn-lg fw-semibold"><i class="bi bi-box-arrow-in-right me-2"></i>Masuk ke Dashboard</button>
          </div>
        </form>

        <div class="text-center pt-2 border-top mt-3">
          <small class="text-muted">Belum punya akun warga? <a href="#" class="text-primary text-decoration-none fw-semibold">Daftar Sekarang</a></small>
        </div>
      </div>
    </div>
  </div>
  `;
}

// Attach submit handler to the login form
export function setupLoginForm() {
  const form = document.getElementById('loginForm');
  if (!form) return;

  const demoEmail = localStorage.getItem('demo_email');
  const demoPass = localStorage.getItem('demo_password');
  if (demoEmail) {
    const inputEmail = document.getElementById('loginEmail');
    if (inputEmail) inputEmail.value = demoEmail;
  }
  if (demoPass) {
    const inputPass = document.getElementById('loginPassword');
    if (inputPass) inputPass.value = demoPass;
  }

  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();

    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value.trim();

    if (!email || !password) {
      alert('Isi email dan password');
      return;
    }

    try {
      const data = await requestAPI('http://127.0.0.1:8000/api/token/', 'POST', {
        email,
        password,
      });

      const access = data.access || data.access_token || data.token || null;
      const refresh = data.refresh || data.refresh_token || null;

      if (!access) throw new Error('Token tidak ditemukan di response');

      localStorage.setItem('access_token', access);
      if (refresh) localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('demo_email', email);

      alert('Login Berhasil');
      location.hash = '#dashboard';
    } catch (err) {
      console.error('Login error', err);
      const message = (err && err.data && err.data.detail) || err.message || 'Login Gagal';
      alert(`Login Gagal: ${message}`);
    }
  });
}
