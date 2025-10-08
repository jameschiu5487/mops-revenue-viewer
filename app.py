from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from get_data_from_mops import MOPSRevenueDownloader

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download_data():
    try:
        data = request.json
        market_type = data.get('market_type', 'sii')
        year = int(data.get('year'))
        month = int(data.get('month'))
        
        # Validate input
        if market_type not in ['sii', 'otc']:
            return jsonify({'error': 'Invalid market type'}), 400
        
        if month < 1 or month > 12:
            return jsonify({'error': 'Month must be between 1 and 12'}), 400
        
        # Download data
        downloader = MOPSRevenueDownloader()
        df = downloader.download_revenue_data(year, month, market_type)
        
        if df is None or df.empty:
            return jsonify({'error': 'Failed to download data'}), 500
        
        # Save to CSV
        filename = downloader.save_to_csv(df, year, month, market_type)
        
        # Convert DataFrame to JSON for display
        # Clean up the multi-level columns if present
        if isinstance(df.columns, pd.MultiIndex):
            # Flatten multi-level columns
            new_columns = []
            for col in df.columns.values:
                # Get the second level if it exists and is not empty, otherwise use first level
                if col[1] and not col[1].startswith('Unnamed'):
                    new_columns.append(col[1])
                elif col[0] and not col[0].startswith('Unnamed'):
                    new_columns.append(col[0])
                else:
                    # If both are unnamed, try to extract meaningful text
                    combined = ' '.join(str(c) for c in col if c and not str(c).startswith('Unnamed'))
                    new_columns.append(combined if combined else col[1])
            df.columns = new_columns
        
        # Clean up column names - remove "Unnamed: X_level_Y" patterns
        df.columns = [col.replace('Unnamed: 0_level_0 ', '').replace('Unnamed: 1_level_0 ', '').strip() 
                      for col in df.columns]
        
        # Replace NaN values with empty string for JSON serialization
        df = df.fillna('')
        
        # Convert to dict for JSON response
        data_dict = df.to_dict('records')
        columns = list(df.columns)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'columns': columns,
            'data': data_dict,
            'row_count': len(df)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
