// --- CHART 1: LAPORAN PER BULAN (LINE CHART MAROON) ---
const ctxBulan = document.getElementById('chartLaporanBulan').getContext('2d');
new Chart(ctxBulan, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
        datasets: [{
            label: 'Jumlah Laporan',
            data: [40, 30, 50, 35, 42, 55, 85, 70],
            backgroundColor: 'rgba(128, 0, 0, 0.2)', // Isian Maroon Transparan
            borderColor: '#800000',                 // Garis Maroon Solid
            borderWidth: 2,
            tension: 0.3,
            fill: true
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false }
        }
    }
});

// --- CHART 2: STATUS LAPORAN (DOUGHNUT CHART DENGAN KOMBINASI MAROON) ---
const ctxStatus = document.getElementById('chartStatusLaporan').getContext('2d');
new Chart(ctxStatus, {
    type: 'doughnut',
    data: {
        labels: ['Reported', 'Verified', 'In Progress', 'Resolved'],
        datasets: [{
            data: [45, 60, 15, 20],
            backgroundColor: [
                '#800000', // Maroon untuk Reported
                '#4b5563', // Gray untuk Verified
                '#f59e0b', // Amber untuk In Progress
                '#10b981'  // Emerald untuk Resolved
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    }
});