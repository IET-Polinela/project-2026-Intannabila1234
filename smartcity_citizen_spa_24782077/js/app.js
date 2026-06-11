import { requestAPI } from './api.js';

export let allReports = [];
export let currentTab = 'feed';
export let currentPage = 1;
export let totalPages = 0;
export let editingReportId = null;

const API_BASE = 'http://103.151.63.87:8009';
const REPORTS_ENDPOINT = `${API_BASE}/api/reports/`;
const REPORT_DETAIL_ENDPOINT = `${API_BASE}/api/reports/`;
const DEFAULT_PAGE_SIZE = 10;

export async function loadDashboardData(tab = currentTab, page = currentPage) {
  currentTab = tab;
  currentPage = page;

  try {
    const response = await requestAPI(
      `${REPORTS_ENDPOINT}?tab=${encodeURIComponent(tab)}&page=${page}&page_size=${DEFAULT_PAGE_SIZE}`
    );

    allReports = Array.isArray(response?.results)
      ? response.results
      : [];

    const totalCount = Number(response?.count ?? 0);
    totalPages = Math.ceil(totalCount / DEFAULT_PAGE_SIZE);

    renderList();
    renderPagination();
    await loadSummaryStats();
  } catch (error) {
    console.error('loadDashboardData error:', error);
    allReports = [];
    totalPages = 0;
    renderList();
    renderPagination();
  }
}

export async function loadSummaryStats() {
  try {
    const response = await requestAPI(`${REPORTS_ENDPOINT}?tab=my_reports&page_size=1000`);
    const reports = Array.isArray(response?.results)
      ? response.results
      : [];

    const draftCount = reports.filter((item) => item.status === 'DRAFT').length;
    const diprosesCount = reports.filter((item) => item.status === 'DIPROSES').length;
    const selesaiCount = reports.filter((item) => item.status === 'SELESAI').length;

    updateSidebarStat('#draftCount', draftCount);
    updateSidebarStat('#diprosesCount', diprosesCount);
    updateSidebarStat('#selesaiCount', selesaiCount);
  } catch (error) {
    console.error('loadSummaryStats error:', error);
  }
}

export function editDraft(id) {
  const report = allReports.find((item) => Number(item.id) === Number(id));
  if (!report) {
    console.warn(`Draft report not found: ${id}`);
    return;
  }

  const titleField = document.getElementById('reportTitle');
  const descriptionField = document.getElementById('reportDescription');
  const statusField = document.getElementById('reportStatus');

  if (titleField) titleField.value = report.title || '';
  if (descriptionField) descriptionField.value = report.description || '';
  if (statusField) statusField.value = report.status || '';

  editingReportId = id;

  const modalElement = document.getElementById('reportModal');
  if (modalElement && window.bootstrap && typeof window.bootstrap.Modal === 'function') {
    const modal = new window.bootstrap.Modal(modalElement);
    modal.show();
  }
}

export async function submitReportForm(status = 'DRAFT', event = null) {
  if (event && typeof event.preventDefault === 'function') {
    event.preventDefault();
  }

  const titleField = document.getElementById('reportTitle');
  const descriptionField = document.getElementById('reportDescription');
  const statusField = document.getElementById('reportStatus');

  const title = titleField?.value.trim() || '';
  const description = descriptionField?.value.trim() || '';
  const finalStatus = status || statusField?.value || 'DRAFT';

  if (!title || !description) {
    alert('Judul dan deskripsi wajib diisi.');
    return;
  }

  const body = {
    title,
    description,
    status: finalStatus,
  };

  const method = editingReportId == null ? 'POST' : 'PUT';
  const url = editingReportId == null
    ? REPORTS_ENDPOINT
    : `${REPORT_DETAIL_ENDPOINT}${editingReportId}/`;

  try {
    await requestAPI(url, method, body);

    resetReportForm();
    editingReportId = null;
    closeReportModal();
    await loadDashboardData(currentTab, currentPage);
  } catch (error) {
    console.error('submitReportForm error:', error);
    alert('Gagal menyimpan laporan. Coba lagi.');
  }
}

export function resetEditingReportId() {
  editingReportId = null;
}

export function resetReportForm() {
  const form = document.getElementById('reportForm');
  if (form) {
    form.reset();
  }
}

export function setupReportForm() {
  // No native submit handler required because buttons are type="button".
  return;
}

function renderList() {
  const container = document.getElementById('reportList');
  if (!container) return;

  container.innerHTML = allReports.length
    ? allReports
        .map((report) => {
          const statusLabel = escapeHtml(report.status);
          const progressValue = getStatusProgress(report.status);
          return `
            <div class="card mb-3">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <div>
                    <h5 class="card-title mb-1">${escapeHtml(report.title)}</h5>
                    <p class="text-muted mb-1">Status: <strong>${statusLabel}</strong></p>
                  </div>
                  <button type="button" class="btn btn-sm btn-outline-primary" onclick="window.editDraft && window.editDraft(${report.id})">Edit</button>
                </div>
                <p class="card-text mb-3">${escapeHtml(report.description)}</p>
                <div class="mb-3">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <small class="text-muted">Progress</small>
                    <small class="text-muted">${progressValue}%</small>
                  </div>
                  <div class="progress" style="height: 10px;">
                    <div class="progress-bar" role="progressbar" style="width: ${progressValue}%" aria-valuenow="${progressValue}" aria-valuemin="0" aria-valuemax="100"></div>
                  </div>
                </div>
                <p class="text-muted mb-0"><strong>Pelapor:</strong> ${escapeHtml(report.reporter)}</p>
              </div>
            </div>
          `;
        })
        .join('')
    : '<p class="text-muted">Tidak ada laporan untuk ditampilkan.</p>';
}

function getStatusProgress(status) {
  switch (status) {
    case 'DRAFT':
      return 20;
    case 'DIPROSES':
      return 50;
    case 'SELESAI':
      return 100;
    case 'VERIFIED':
      return 75;
    default:
      return 40;
  }
}

function renderPagination() {
  const container = document.getElementById('paginationControls');
  if (!container) return;

  if (totalPages <= 1) {
    container.innerHTML = '';
    return;
  }

  const pages = Array.from({ length: totalPages }, (_, index) => index + 1);
  container.innerHTML = pages
    .map((page) => {
      const activeClass = page === currentPage ? 'active' : '';
      return `
        <button type="button" class="btn btn-sm btn-outline-secondary me-1 ${activeClass}" data-page="${page}">${page}</button>
      `;
    })
    .join('');

  container.querySelectorAll('button[data-page]').forEach((button) => {
    button.addEventListener('click', async () => {
      const page = Number(button.getAttribute('data-page'));
      if (!page || page === currentPage) return;
      currentPage = page;
      await loadDashboardData(currentTab, currentPage);
    });
  });
}

function updateSidebarStat(selector, value) {
  const element = document.querySelector(selector);
  if (element) {
    element.textContent = String(value);
  }
}

function closeReportModal() {
  const modalElement = document.getElementById('reportModal');
  if (modalElement && window.bootstrap && typeof window.bootstrap.Modal === 'function') {
    const modal = window.bootstrap.Modal.getInstance(modalElement);
    if (modal) {
      modal.hide();
    }
  }
}

function escapeHtml(value) {
  if (typeof value !== 'string') return '';
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

if (typeof window !== 'undefined') {
  window.editDraft = editDraft;
}
