let currentData = [];
let currentColumns = [];
let currentSearchTerm = '';
let sortState = {
    column: null,
    ascending: true
};

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('queryForm');
    const submitBtn = document.getElementById('submitBtn');
    const searchBox = document.getElementById('searchBox');
    const exportBtn = document.getElementById('exportBtn');
    
    form.addEventListener('submit', handleSubmit);
    searchBox.addEventListener('input', handleSearch);
    exportBtn.addEventListener('click', handleExport);
});

async function handleSubmit(e) {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    const statusMessage = document.getElementById('statusMessage');
    
    // Get form data
    const marketType = document.getElementById('marketType').value;
    const year = parseInt(document.getElementById('year').value);
    const month = parseInt(document.getElementById('month').value);
    
    // Disable button and show loader
    submitBtn.disabled = true;
    btnText.textContent = 'Downloading...';
    loader.style.display = 'inline-block';
    
    // Show info message
    showStatus('Downloading data from MOPS...', 'info');
    
    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                market_type: marketType,
                year: year,
                month: month
            })
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Failed to download data');
        }
        
        // Store data
        currentData = result.data;
        currentColumns = result.columns;
        
        // Display results
        displayResults(result);
        showStatus(`Successfully downloaded ${result.row_count} rows of data`, 'success');
        
    } catch (error) {
        console.error('Error:', error);
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        // Re-enable button
        submitBtn.disabled = false;
        btnText.textContent = 'Query Data';
        loader.style.display = 'none';
    }
}

function displayResults(result) {
    const resultsPanel = document.getElementById('resultsPanel');
    const rowCount = document.getElementById('rowCount');
    const fileName = document.getElementById('fileName');
    const tableHead = document.getElementById('tableHead');
    const tableBody = document.getElementById('tableBody');
    const searchBox = document.getElementById('searchBox');
    
    // Show results panel
    resultsPanel.style.display = 'block';
    resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Update info
    rowCount.textContent = `${result.row_count} rows`;
    fileName.textContent = result.filename;
    
    // Clear search and reset search state
    searchBox.value = '';
    currentSearchTerm = '';
    
    // Clear previous table
    tableHead.innerHTML = '';
    tableBody.innerHTML = '';
    
    // Define sortable columns (numeric columns)
    const sortableColumns = [
        '當月營收', '上月營收', '去年當月營收', 
        '上月比較 增減(%)', '去年同月 增減(%)',
        '當月累計營收', '去年累計營收', '前期比較 增減(%)'
    ];
    
    // Create table header with sort functionality
    const headerRow = document.createElement('tr');
    result.columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        
        // Add sort functionality to numeric columns
        if (sortableColumns.includes(col)) {
            th.classList.add('sortable');
            th.innerHTML = `${col} <span class="sort-icon">⇅</span>`;
            th.addEventListener('click', () => sortTable(col));
        }
        
        headerRow.appendChild(th);
    });
    tableHead.appendChild(headerRow);
    
    // Create table body
    renderTableBody(result.data, result.columns);
}

function renderTableBody(data, columns) {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';
    
    data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(col => {
            const td = document.createElement('td');
            const value = row[col] || '-';
            td.textContent = value;
            
            // Add numeric class for right alignment
            if (isNumericColumn(col)) {
                td.classList.add('numeric');
            }
            
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    });
}

function sortTable(column) {
    // Toggle sort direction if clicking the same column
    if (sortState.column === column) {
        sortState.ascending = !sortState.ascending;
    } else {
        sortState.column = column;
        sortState.ascending = true;
    }
    
    // Sort the data
    const sortedData = [...currentData].sort((a, b) => {
        let aVal = a[column];
        let bVal = b[column];
        
        // Convert to numbers, treating empty/invalid values as 0
        aVal = parseFloat(String(aVal).replace(/,/g, '')) || 0;
        bVal = parseFloat(String(bVal).replace(/,/g, '')) || 0;
        
        if (sortState.ascending) {
            return aVal - bVal;
        } else {
            return bVal - aVal;
        }
    });
    
    // Update sort icons
    updateSortIcons(column);
    
    // Re-render table body
    renderTableBody(sortedData, currentColumns);
    
    // Re-apply search filter after sorting
    if (currentSearchTerm) {
        applySearch();
    }
}

function updateSortIcons(activeColumn) {
    const headers = document.querySelectorAll('th.sortable');
    headers.forEach(th => {
        const icon = th.querySelector('.sort-icon');
        if (icon) {
            const columnName = th.textContent.replace('⇅', '').replace('↑', '').replace('↓', '').trim();
            if (columnName === activeColumn) {
                icon.textContent = sortState.ascending ? '↑' : '↓';
            } else {
                icon.textContent = '⇅';
            }
        }
    });
}

function isNumericColumn(column) {
    const numericColumns = [
        '當月營收', '上月營收', '去年當月營收', 
        '上月比較 增減(%)', '去年同月 增減(%)',
        '當月累計營收', '去年累計營收', '前期比較 增減(%)'
    ];
    return numericColumns.includes(column);
}

function handleSearch(e) {
    currentSearchTerm = e.target.value.toLowerCase();
    applySearch();
}

function applySearch() {
    const tableBody = document.getElementById('tableBody');
    const rows = tableBody.getElementsByTagName('tr');
    
    Array.from(rows).forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(currentSearchTerm)) {
            row.classList.remove('hidden');
        } else {
            row.classList.add('hidden');
        }
    });
}

function handleExport() {
    if (currentData.length === 0) {
        alert('No data to export');
        return;
    }
    
    // Convert data to CSV
    const csv = convertToCSV(currentData, currentColumns);
    
    // Create download link
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `revenue_data_${Date.now()}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function convertToCSV(data, columns) {
    const header = columns.join(',');
    const rows = data.map(row => {
        return columns.map(col => {
            const value = row[col] || '';
            // Escape quotes and wrap in quotes if contains comma
            if (String(value).includes(',') || String(value).includes('"')) {
                return `"${String(value).replace(/"/g, '""')}"`;
            }
            return value;
        }).join(',');
    });
    
    return [header, ...rows].join('\n');
}

function showStatus(message, type) {
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    
    if (type === 'success') {
        setTimeout(() => {
            statusMessage.style.display = 'none';
        }, 5000);
    }
}
