/**
 * Chart.js Integration with Django API
 * Fetch data dari Django endpoints dan render charts
 */

// Global chart instances untuk tracking
let statusChart = null;
let categoryChart = null;


// ============================================================
// 1. FETCH DATA FROM DJANGO API
// ============================================================

/**
 * Fetch status statistics dari API
 * Endpoint: /main_app/api/status-statistics/
 */
async function fetchStatusData() {
    try {
        const response = await fetch('/main_app/api/status-statistics/');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Status Data:', data);
        return data;
        
    } catch (error) {
        console.error('Error fetching status data:', error);
        return null;
    }
}


/**
 * Fetch category statistics dari API
 * Endpoint: /main_app/api/category-statistics/
 */
async function fetchCategoryData() {
    try {
        const response = await fetch('/main_app/api/category-statistics/');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Category Data:', data);
        return data;
        
    } catch (error) {
        console.error('Error fetching category data:', error);
        return null;
    }
}


// ============================================================
// 2. RENDER DOUGHNUT CHART (Status Distribution)
// ============================================================

/**
 * Render Doughnut Chart untuk Status Laporan
 * Menampilkan distribusi laporan per status
 */
async function renderStatusChart() {
    const statusData = await fetchStatusData();
    
    if (!statusData) {
        console.error('No status data available');
        return;
    }
    
    // Get canvas element
    const ctx = document.getElementById('statusChart');
    if (!ctx) {
        console.error('Canvas element #statusChart not found');
        return;
    }
    
    // Destroy existing chart jika ada (untuk prevent memory leak)
    if (statusChart) {
        statusChart.destroy();
    }
    
    // Extract labels dan values
    const labels = Object.keys(statusData);  // ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']
    const values = Object.values(statusData); // [5, 3, 2, 4]
    
    // Define colors untuk setiap status
    const colors = {
        'REPORTED': '#FFC107',      // Kuning
        'VERIFIED': '#17A2B8',      // Cyan
        'IN_PROGRESS': '#007BFF',   // Biru
        'RESOLVED': '#28A745',      // Hijau
    };
    
    const backgroundColor = labels.map(label => colors[label] || '#6C757D');
    
    // Create Doughnut Chart
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
                        label: function(context) {
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
    
    console.log('Status Chart rendered successfully');
}


// ============================================================
// 3. RENDER BAR CHART (Category Distribution)
// ============================================================

/**
 * Render Bar Chart untuk Kategori Laporan
 * Menampilkan distribusi laporan per kategori
 */
async function renderCategoryChart() {
    const categoryData = await fetchCategoryData();
    
    if (!categoryData) {
        console.error('No category data available');
        return;
    }
    
    // Get canvas element
    const ctx = document.getElementById('categoryChart');
    if (!ctx) {
        console.error('Canvas element #categoryChart not found');
        return;
    }
    
    // Destroy existing chart jika ada
    if (categoryChart) {
        categoryChart.destroy();
    }
    
    // Extract labels dan values
    const labels = Object.keys(categoryData);
    const values = Object.values(categoryData);
    
    // Define colors untuk bar chart
    const backgroundColor = [
        '#FF6384',
        '#36A2EB',
        '#FFCE56',
        '#4BC0C0',
        '#9966FF',
        '#FF9F40',
        '#FF6384',
        '#C9CBCF',
    ];
    
    // Create Bar Chart
    categoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Jumlah Laporan',
                data: values,
                backgroundColor: backgroundColor.slice(0, labels.length),
                borderColor: backgroundColor.slice(0, labels.length),
                borderWidth: 1,
            }]
        },
        options: {
            indexAxis: 'y',  // Horizontal bar chart
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Jumlah: ${context.parsed.x}`;
                        }
                    }
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
    
    console.log('Category Chart rendered successfully');
}


// ============================================================
// 4. INITIALIZATION (DOMContentLoaded)
// ============================================================

/**
 * Initialize charts saat DOM siap
 */
document.addEventListener('DOMContentLoaded', async function() {
    console.log('DOM loaded. Initializing charts...');
    
    // Render doughnut chart
    await renderStatusChart();
    
    // Render bar chart
    await renderCategoryChart();
    
    console.log('All charts initialized successfully');
});


// ============================================================
// 5. REFRESH CHARTS (Optional)
// ============================================================

/**
 * Function untuk refresh charts (optional)
 * Bisa dipanggil dari button atau interval
 */
async function refreshCharts() {
    console.log('Refreshing charts...');
    await renderStatusChart();
    await renderCategoryChart();
    console.log('Charts refreshed');
}


// Optional: Auto-refresh charts setiap 30 detik
// Uncomment jika ingin enable
// setInterval(refreshCharts, 30000);
