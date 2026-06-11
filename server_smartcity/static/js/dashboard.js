/**
 * Dashboard.js - Lab Session 7: Pemrograman Internet 1
 * 
 * Fitur:
 * 1. Chart.js untuk visualisasi data (Doughnut & Bar Chart)
 * 2. Fetch API untuk mengambil data dari backend (tanpa reload)
 * 3. Live Search dengan Debouncing
 * 4. Detail Modal dengan Event Delegation
 * 5. DOMContentLoaded untuk inisialisasi
 */

// ============================================================
// DEBOUNCE FUNCTION - Untuk Live Search
// ============================================================
/**
 * Fungsi debounce untuk mengurangi frequency pemanggilan API
 * saat user mengetik di search input.
 * 
 * @param {Function} func - Fungsi yang akan dijalankan
 * @param {Number} delay - Delay dalam milliseconds
 * @returns {Function} - Function debounced
 */
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}


// ============================================================
// CHART INSTANCES - Global variable untuk menyimpan chart
// ============================================================
let statusChart = null;
let categoryChart = null;


// ============================================================
// FETCH DATA FUNCTIONS
// ============================================================

/**
 * Mengambil data statistik status dari API
 * @returns {Promise<Object>} - Data statistik status
 */
async function fetchStatusStatistics() {
    try {
        const response = await fetch('/main_app/api/status-statistics/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching status statistics:', error);
        return null;
    }
}


/**
 * Mengambil data statistik kategori dari API
 * @returns {Promise<Object>} - Data statistik kategori
 */
async function fetchCategoryStatistics() {
    try {
        const response = await fetch('/main_app/api/category-statistics/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching category statistics:', error);
        return null;
    }
}


/**
 * Mengambil 5 laporan terbaru dengan status REPORTED
 * @returns {Promise<Array>} - Array laporan terbaru
 */
async function fetchLatestReported() {
    try {
        const response = await fetch('/main_app/api/latest-reported/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching latest reported:', error);
        return [];
    }
}


/**
 * Mengambil 5 laporan terbaru dengan status RESOLVED
 * @returns {Promise<Array>} - Array laporan terbaru
 */
async function fetchLatestResolved() {
    try {
        const response = await fetch('/main_app/api/latest-resolved/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching latest resolved:', error);
        return [];
    }
}


/**
 * Mencari laporan berdasarkan query
 * @param {String} query - String pencarian
 * @returns {Promise<Array>} - Array hasil pencarian
 */
async function searchReports(query) {
    try {
        const response = await fetch(`/main_app/api/search/?q=${encodeURIComponent(query)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error searching reports:', error);
        return [];
    }
}


/**
 * Mengambil detail laporan berdasarkan ID
 * @param {Number} reportId - ID laporan
 * @returns {Promise<Object>} - Detail laporan
 */
async function fetchReportDetail(reportId) {
    try {
        const response = await fetch(`/main_app/api/detail/${reportId}/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching report detail:', error);
        return null;
    }
}


// ============================================================
// CHART RENDERING FUNCTIONS
// ============================================================

/**
 * Render Doughnut Chart untuk Status Laporan
 * Menggunakan Chart.js library
 */
async function renderStatusChart() {
    const data = await fetchStatusStatistics();
    
    if (!data) {
        console.error('No data for status chart');
        return;
    }

    const ctx = document.getElementById('statusChart');
    if (!ctx) return;

    // Destroy existing chart jika ada
    if (statusChart) {
        statusChart.destroy();
    }

    // Define warna untuk setiap status
    const colors = {
        'REPORTED': '#FFC107',    // Kuning
        'VERIFIED': '#17A2B8',    // Cyan
        'IN_PROGRESS': '#007BFF', // Biru
        'RESOLVED': '#28A745',    // Hijau
    };

    // Siapkan labels dan datasets
    const labels = Object.keys(data);
    const values = Object.values(data);
    const backgroundColor = labels.map(label => colors[label] || '#6C757D');

    // Render Doughnut Chart
    statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: backgroundColor,
                borderColor: '#fff',
                borderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            size: 14,
                        },
                        padding: 15,
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}


/**
 * Render Bar Chart untuk Kategori Laporan
 * Menggunakan Chart.js library
 */
async function renderCategoryChart() {
    const data = await fetchCategoryStatistics();
    
    if (!data) {
        console.error('No data for category chart');
        return;
    }

    const ctx = document.getElementById('categoryChart');
    if (!ctx) return;

    // Destroy existing chart jika ada
    if (categoryChart) {
        categoryChart.destroy();
    }

    // Siapkan labels dan datasets
    const labels = Object.keys(data);
    const values = Object.values(data);

    // Render Bar Chart
    categoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Jumlah Laporan',
                data: values,
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40',
                ],
                borderColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40',
                ],
                borderWidth: 1,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false,
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                    }
                }
            }
        }
    });
}


// ============================================================
// RENDER LIST FUNCTIONS
// ============================================================

/**
 * Render list laporan berdasarkan array
 * Menampilkan laporan dalam bentuk list group
 */
function renderReportList(reports, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (reports.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-3">Belum ada laporan</p>';
        return;
    }

    let html = '';
    reports.forEach(report => {
        // Badge status dengan warna berbeda
        let statusBadge = '';
        if (report.status === 'REPORTED') {
            statusBadge = '<span class="badge bg-warning">REPORTED</span>';
        } else if (report.status === 'VERIFIED') {
            statusBadge = '<span class="badge bg-info">VERIFIED</span>';
        } else if (report.status === 'IN_PROGRESS') {
            statusBadge = '<span class="badge bg-primary">IN_PROGRESS</span>';
        } else if (report.status === 'RESOLVED') {
            statusBadge = '<span class="badge bg-success">RESOLVED</span>';
        }

        html += `
            <div class="list-group-item">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <h6 class="mb-1">${report.title}</h6>
                        <p class="mb-1 text-muted small">📍 ${report.location}</p>
                        <p class="mb-0 text-muted small">🏷️ ${report.category}</p>
                    </div>
                    <div class="col-md-4 text-end">
                        ${statusBadge}
                        <button 
                            class="btn btn-sm btn-outline-primary ms-2 detail-btn"
                            data-report-id="${report.id}"
                        >
                            Detail
                        </button>
                    </div>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}


/**
 * Render search results
 * Menampilkan hasil pencarian di search results container
 */
function renderSearchResults(reports) {
    const container = document.getElementById('searchResults');
    if (!container) return;

    if (reports.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-3">Tidak ada hasil pencarian</p>';
        return;
    }

    let html = '<div class="list-group">';
    reports.forEach(report => {
        // Badge status dengan warna berbeda
        let statusBadge = '';
        if (report.status === 'REPORTED') {
            statusBadge = '<span class="badge bg-warning">REPORTED</span>';
        } else if (report.status === 'VERIFIED') {
            statusBadge = '<span class="badge bg-info">VERIFIED</span>';
        } else if (report.status === 'IN_PROGRESS') {
            statusBadge = '<span class="badge bg-primary">IN_PROGRESS</span>';
        } else if (report.status === 'RESOLVED') {
            statusBadge = '<span class="badge bg-success">RESOLVED</span>';
        }

        html += `
            <a href="#" class="list-group-item list-group-item-action">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <h6 class="mb-1">${report.title}</h6>
                        <p class="mb-1 text-muted small">📍 ${report.location}</p>
                    </div>
                    <div class="col-md-4 text-end">
                        ${statusBadge}
                        <button 
                            class="btn btn-sm btn-outline-primary ms-2 detail-btn"
                            data-report-id="${report.id}"
                        >
                            Detail
                        </button>
                    </div>
                </div>
            </a>
        `;
    });
    html += '</div>';

    container.innerHTML = html;
}


// ============================================================
// MODAL FUNCTIONS
// ============================================================

/**
 * Menampilkan detail laporan di modal
 * Menggunakan Bootstrap Modal
 */
async function showDetailModal(reportId) {
    const report = await fetchReportDetail(reportId);
    
    if (!report) {
        alert('Gagal mengambil detail laporan');
        return;
    }

    // Tentukan badge status
    let statusBadge = '';
    if (report.status === 'REPORTED') {
        statusBadge = '<span class="badge bg-warning">REPORTED</span>';
    } else if (report.status === 'VERIFIED') {
        statusBadge = '<span class="badge bg-info">VERIFIED</span>';
    } else if (report.status === 'IN_PROGRESS') {
        statusBadge = '<span class="badge bg-primary">IN_PROGRESS</span>';
    } else if (report.status === 'RESOLVED') {
        statusBadge = '<span class="badge bg-success">RESOLVED</span>';
    }

    // Update modal content
    const modalContent = document.getElementById('modalContent');
    modalContent.innerHTML = `
        <div class="container-fluid">
            <div class="row mb-3">
                <div class="col-md-12">
                    <label class="form-label fw-bold">Judul:</label>
                    <p>${report.title}</p>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label fw-bold">Lokasi:</label>
                    <p>📍 ${report.location}</p>
                </div>
                <div class="col-md-6">
                    <label class="form-label fw-bold">Kategori:</label>
                    <p>🏷️ ${report.category || '-'}</p>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-12">
                    <label class="form-label fw-bold">Status:</label>
                    <p>${statusBadge}</p>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <label class="form-label fw-bold">Deskripsi:</label>
                    <p>${report.description || '-'}</p>
                </div>
            </div>
        </div>
    `;

    // Update modal title
    document.getElementById('detailModalLabel').textContent = `Detail Laporan #${report.id}`;

    // Tampilkan modal menggunakan Bootstrap 5
    const modal = new bootstrap.Modal(document.getElementById('detailModal'));
    modal.show();
}


// ============================================================
// EVENT LISTENERS
// ============================================================

/**
 * Event listener untuk Live Search
 * Menggunakan Debouncing untuk mengurangi API calls
 */
const debouncedSearch = debounce(async function (query) {
    const searchResults = document.getElementById('searchResults');
    
    if (query.length < 2) {
        searchResults.innerHTML = '';
        return;
    }

    const results = await searchReports(query);
    renderSearchResults(results);
}, 300); // Delay 300ms


// ============================================================
// INITIALIZATION - DOMContentLoaded
// ============================================================

/**
 * Inisialisasi dashboard saat DOM siap
 * - Load charts
 * - Load latest reports
 * - Setup event listeners
 */
document.addEventListener('DOMContentLoaded', async function () {
    console.log('Dashboard initialized');

    // 1. Render Charts
    await renderStatusChart();
    await renderCategoryChart();

    // 2. Load Latest Reports
    const latestReported = await fetchLatestReported();
    const latestResolved = await fetchLatestResolved();
    
    renderReportList(latestReported, 'latestReportedList');
    renderReportList(latestResolved, 'latestResolvedList');

    // 3. Setup Search Input Event Listener
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function (e) {
            const query = e.target.value.trim();
            debouncedSearch(query);
        });

        // Clear search results saat input dikosongkan
        searchInput.addEventListener('focus', function () {
            if (this.value.trim() === '') {
                document.getElementById('searchResults').innerHTML = '';
            }
        });

        searchInput.addEventListener('blur', function () {
            setTimeout(() => {
                document.getElementById('searchResults').innerHTML = '';
            }, 200);
        });
    }

    // 4. Event Delegation untuk Detail Button
    // Menggunakan event delegation untuk handle click event pada dinamis button
    document.addEventListener('click', function (e) {
        // Cek apakah element yang diklik adalah detail-btn
        if (e.target.classList.contains('detail-btn')) {
            e.preventDefault();
            const reportId = e.target.getAttribute('data-report-id');
            if (reportId) {
                showDetailModal(reportId);
            }
        }
    });

    // 5. Refresh Charts setiap 30 detik (optional)
    // setInterval(async () => {
    //     await renderStatusChart();
    //     await renderCategoryChart();
    // }, 30000);
});
