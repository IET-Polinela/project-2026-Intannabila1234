import { loadDashboardData, setupReportForm, submitReportForm, resetEditingReportId, resetReportForm } from './app.js?v=5';

// dashboard.js
// Renders dashboard layout and wiring logout and report interactions.

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
          <div class="d-flex gap-2">
            <button type="button" class="btn btn-primary" id="navNewReport">Laporan Baru</button>
            <button type="button" class="btn btn-outline-light" id="navMyReports">Laporan Saya</button>
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

        <div class="card mb-4">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <div>
                <h5 class="mb-0 fw-semibold">Daftar Laporan</h5>
                <small class="text-muted">Tampilkan data berdasarkan tab Feed Kota atau Laporan Saya.</small>
              </div>
              <div class="btn-group" role="group" aria-label="Toggle report tabs">
                <button type="button" id="tabFeed" class="btn btn-outline-secondary active">Feed Kota</button>
                <button type="button" id="tabMyReports" class="btn btn-outline-secondary">Laporan Saya</button>
              </div>
            </div>
            <div id="reportList"></div>
            <div id="paginationControls" class="mt-3"></div>
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
        <div class="card profile-card shadow-lg p-4 mb-4">
          <div class="d-flex align-items-center gap-3 mb-4">
            <div class="profile-avatar">
              <i class="bi bi-person-fill"></i>
            </div>
            <div>
              <p class="text-uppercase text-white-75 mb-1 small">Profil Warga</p>
              <h5 class="mb-0 fw-semibold">Warga</h5>
            </div>
          </div>

          <dl class="row profile-data text-white mb-0">
            <dt class="col-12">Nama Lengkap</dt>
            <dd class="col-12" id="profileName">Warga</dd>
            <dt class="col-12">Alamat Email</dt>
            <dd class="col-12" id="profileEmail">warga@example.com</dd>
          </dl>
        </div>

        <div class="card shadow-sm p-4">
          <h6 class="mb-3">Rekap Status</h6>
          <div class="d-flex justify-content-between mb-2">
            <span>Draft</span>
            <strong id="draftCount">0</strong>
          </div>
          <div class="d-flex justify-content-between mb-2">
            <span>Diproses</span>
            <strong id="diprosesCount">0</strong>
          </div>
          <div class="d-flex justify-content-between">
            <span>Selesai</span>
            <strong id="selesaiCount">0</strong>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="reportModal" tabindex="-1" aria-labelledby="reportModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="reportModalLabel">Form Laporan</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form id="reportForm">
              <div class="mb-3">
                <label for="reportTitle" class="form-label">Judul Laporan</label>
                <input type="text" class="form-control" id="reportTitle" placeholder="Masukkan judul laporan" required />
              </div>
              <div class="mb-3">
                <label for="reportDescription" class="form-label">Deskripsi</label>
                <textarea class="form-control" id="reportDescription" rows="4" placeholder="Jelaskan masalah secara singkat" required></textarea>
              </div>
              <div class="mb-3">
                <label for="reportStatus" class="form-label">Status</label>
                <select class="form-select" id="reportStatus">
                  <option value="DRAFT">Draft</option>
                  <option value="VERIFIED">Ajukan</option>
                </select>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Batal</button>
            <button type="button" id="saveDraftBtn" class="btn btn-outline-primary">Simpan Draft</button>
            <button type="button" id="submitReportBtn" class="btn btn-primary">Ajukan</button>
          </div>
        </div>
      </div>
    </div>
  </section>
  `;
}

// Wire up dashboard interactions like logout and reports
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
      resetEditingReportId();
      resetReportForm();
      const modalElement = document.getElementById('reportModal');
      if (modalElement && window.bootstrap && typeof window.bootstrap.Modal === 'function') {
        const modal = new window.bootstrap.Modal(modalElement);
        modal.show();
      }
    });
  }

  const navMyReportsBtn = document.getElementById('navMyReports');
  const tabMyReportsBtn = document.getElementById('tabMyReports');
  const tabFeedBtn = document.getElementById('tabFeed');

  function setActiveTab(selected) {
    if (tabFeedBtn) tabFeedBtn.classList.toggle('active', selected === 'feed');
    if (tabMyReportsBtn) tabMyReportsBtn.classList.toggle('active', selected === 'my_reports');
  }

  if (navMyReportsBtn) {
    navMyReportsBtn.addEventListener('click', async () => {
      setActiveTab('my_reports');
      await loadDashboardData('my_reports', 1);
    });
  }

  if (tabMyReportsBtn) {
    tabMyReportsBtn.addEventListener('click', async () => {
      setActiveTab('my_reports');
      await loadDashboardData('my_reports', 1);
    });
  }

  if (tabFeedBtn) {
    tabFeedBtn.addEventListener('click', async () => {
      setActiveTab('feed');
      await loadDashboardData('feed', 1);
    });
  }

  const saveDraftBtn = document.getElementById('saveDraftBtn');
  if (saveDraftBtn) {
    saveDraftBtn.addEventListener('click', () => submitReportForm('DRAFT'));
  }

  const submitReportBtn = document.getElementById('submitReportBtn');
  if (submitReportBtn) {
    submitReportBtn.addEventListener('click', () => submitReportForm('VERIFIED'));
  }

  const profileName = document.getElementById('profileName');
  if (profileName) {
    profileName.textContent = localStorage.getItem('profile_name') || 'Warga';
  }

  const profileEmail = document.getElementById('profileEmail');
  if (profileEmail) {
    profileEmail.textContent = localStorage.getItem('profile_email') || 'warga@example.com';
  }

  setupReportForm();
  setActiveTab('feed');
  loadDashboardData('feed', 1);
}
