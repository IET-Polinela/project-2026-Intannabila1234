// dashboard.js
// Renders dashboard layout and wiring logout and sample data.

// Return HTML string for dashboard layout
export function renderDashboard() {
  return `
  <section class="dashboard-content">
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex flex-column flex-md-row align-items-start align-items-md-center justify-content-between gap-3">
          <div>
            <h1 class="display-6 fw-bold">Ringkasan Smart City</h1>
            <p class="text-muted mb-0">Selamat datang! Berikut ringkasan singkat layanan dan laporan Anda hari ini.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-12 col-xl-8">
        <div class="row g-4">
          <div class="col-12 col-md-6">
            <div class="card stats-card">
              <div class="card-body">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div>
                    <h6 class="text-uppercase text-muted mb-2">Laporan Hari Ini</h6>
                    <p class="stats-number mb-0">12</p>
                  </div>
                  <div class="stats-tag bg-warning bg-opacity-15 text-warning shadow-sm">
                    <i class="bi bi-exclamation-circle-fill fs-4"></i>
                  </div>
                </div>
                <p class="mb-0 text-muted">Total laporan baru yang masuk hari ini. Pantau terus untuk respon cepat.</p>
              </div>
            </div>
          </div>
          <div class="col-12 col-md-6">
            <div class="card stats-card">
              <div class="card-body">
                <div class="d-flex align-items-center justify-content-between mb-3">
                  <div>
                    <h6 class="text-uppercase text-muted mb-2">Total Laporan</h6>
                    <p class="stats-number mb-0">1,234</p>
                  </div>
                  <div class="stats-tag bg-success bg-opacity-15 text-success shadow-sm">
                    <i class="bi bi-check-circle-fill fs-4"></i>
                  </div>
                </div>
                <p class="mb-0 text-muted">Ringkasan semua laporan yang telah tercatat di portal Anda sampai hari ini.</p>
              </div>
            </div>
          </div>
        </div>

        <div class="card info-card mt-4">
          <div class="card-body">
            <div class="d-flex align-items-center gap-3 mb-3">
              <div class="bg-primary bg-opacity-10 text-primary rounded-3 p-3 shadow-sm">
                <i class="bi bi-info-circle-fill fs-4"></i>
              </div>
              <div>
                <h5 class="mb-1 fw-semibold">Informasi Layanan</h5>
                <p class="mb-0 text-muted">Gunakan portal ini untuk membuat laporan baru, memeriksa status pengaduan, dan mengakses informasi kota secara cepat.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-xl-4">
        <div class="card profile-card shadow-lg p-4">
          <div class="d-flex align-items-center gap-3 mb-4">
            <div class="profile-avatar">
              <i class="bi bi-person-fill"></i>
            </div>
            <div>
              <p class="text-uppercase text-white-75 mb-1 small">Profil Warga</p>
              <h5 class="mb-0 fw-semibold">Warga</h5>
            </div>
          </div>

          <dl class="row profile-data text-white">
            <dt class="col-12">Nama Lengkap</dt>
            <dd class="col-12" id="profileName">Warga</dd>
            <dt class="col-12">Alamat Email</dt>
            <dd class="col-12" id="profileEmail">warga@example.com</dd>
          </dl>
        </div>
      </div>
    </div>
  </section>
  `;
}

// Wire up dashboard interactions like logout
export function setupDashboard() {
  const logoutBtn = document.getElementById('navLogout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      location.hash = '#login';
    });
  }

  const newReportBtn = document.getElementById('navNewReport');
  if (newReportBtn) {
    newReportBtn.addEventListener('click', () => {
      alert('Fitur Laporan Baru akan tersedia segera.');
    });
  }

  const myReportsBtn = document.getElementById('navMyReports');
  if (myReportsBtn) {
    myReportsBtn.addEventListener('click', () => {
      alert('Fitur Laporan Saya akan tersedia segera.');
    });
  }

  const profileName = document.getElementById('profileName');
  if (profileName) {
    profileName.textContent = localStorage.getItem('profile_name') || 'Warga';
  }

  const profileEmail = document.getElementById('profileEmail');
  if (profileEmail) {
    profileEmail.textContent = localStorage.getItem('profile_email') || 'warga@example.com';
  }
}
