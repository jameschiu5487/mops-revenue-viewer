# MOPS Revenue Data Viewer

A web application for querying and viewing monthly revenue data from Taiwan's Market Observation Post System (MOPS).

## Features

-   Query revenue data by market type (Listed/OTC), year, and month
-   Automatic data download from MOPS website
-   Interactive data table with search functionality
-   Export data to CSV
-   Modern and responsive UI

## Installation

1. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:

```bash
python app.py
```

2. Open your browser and navigate to:

```
http://localhost:5000
```

3. Use the web interface to:
    - Select market type (Listed Companies or OTC Companies)
    - Enter ROC year (e.g., 113 for 2024)
    - Enter month (1-12)
    - Click "Query Data" to download and display results

## Project Structure

```
.
├── app.py                  # Flask backend application
├── get_data_from_mops.py   # MOPS data downloader module
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheet
│   └── js/
│       └── app.js         # Frontend JavaScript
└── data/                  # Downloaded CSV files storage
```

## API Endpoints

### POST /api/download

Download revenue data from MOPS.

**Request Body:**

```json
{
    "market_type": "sii", // "sii" or "otc"
    "year": 113, // ROC year
    "month": 7 // 1-12
}
```

**Response:**

```json
{
  "success": true,
  "filename": "data/revenue_sii_113_07.csv",
  "columns": [...],
  "data": [...],
  "row_count": 990
}
```

## Notes

-   Downloaded CSV files are stored in the `data/` directory
-   Files with the same name will be overwritten
-   Year format is ROC (Republic of China) year (AD year - 1911)
