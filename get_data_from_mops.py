import requests
import pandas as pd
from io import StringIO
import time
from datetime import datetime
import os

class MOPSRevenueDownloader:
    """
    Download monthly revenue summary data from MOPS (Market Observation Post System)
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def download_revenue_data(self, year, month, market_type='sii'):
        """
        Download monthly revenue data
        
        Parameters:
        -----------
        year : int
            ROC year (e.g., 113 for 2024, 114 for 2025)
        month : int
            Month (1-12)
        market_type : str
            'sii' for listed companies (上市) or 'otc' for OTC companies (上櫃)
        
        Returns:
        --------
        pandas.DataFrame
            Revenue data (combined from all industry categories)
        """
        
        # Construct URL based on market type
        # Format: https://mopsov.twse.com.tw/nas/t21/sii/t21sc03_113_7_0.html
        if market_type == 'sii':
            url = f"https://mopsov.twse.com.tw/nas/t21/sii/t21sc03_{year}_{month}_0.html"
        elif market_type == 'otc':
            url = f"https://mopsov.twse.com.tw/nas/t21/otc/t21sc03_{year}_{month}_0.html"
        else:
            raise ValueError("market_type must be 'sii' or 'otc'")
        
        try:
            print(f"Downloading {market_type.upper()} revenue data for {year}/{month:02d}...")
            print(f"URL: {url}")
            
            response = self.session.get(url)
            response.encoding = 'big5'
            
            if response.status_code != 200:
                print(f"Error: HTTP status code {response.status_code}")
                return None
            
            # Parse HTML tables
            tables = pd.read_html(StringIO(response.text))
            
            if not tables:
                print("No data found")
                return None
            
            print(f"Found {len(tables)} tables")
            
            # Filter out small tables (headers) and combine data tables
            # Data tables typically have 11 columns and more than 2 rows
            data_tables = [t for t in tables if len(t.columns) == 11 and len(t) > 2]
            
            if not data_tables:
                print("No valid data tables found")
                return None
            
            print(f"Found {len(data_tables)} data tables with revenue information")
            
            # Combine all data tables
            combined_df = pd.concat(data_tables, ignore_index=True)
            
            print(f"Successfully downloaded {len(combined_df)} rows of data")
            return combined_df
            
        except Exception as e:
            print(f"Error downloading data: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_to_csv(self, df, year, month, market_type='sii', output_dir='data'):
        """
        Save DataFrame to CSV file
        
        Parameters:
        -----------
        df : pandas.DataFrame
            Data to save
        year : int
            ROC year
        month : int
            Month
        market_type : str
            Market type
        output_dir : str
            Output directory path (default: 'data')
        """
        if df is None or df.empty:
            print("No data to save")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{output_dir}/revenue_{market_type}_{year}_{month:02d}.csv"
        
        # Check if file exists and will be overwritten
        if os.path.exists(filename):
            print(f"Overwriting existing file: {filename}")
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data saved to: {filename}")
        return filename
    
    def download_multiple_months(self, start_year, start_month, end_year, end_month, 
                                 market_type='sii', output_dir='data', delay=2):
        """
        Download revenue data for multiple months
        
        Parameters:
        -----------
        start_year : int
            Starting ROC year
        start_month : int
            Starting month
        end_year : int
            Ending ROC year
        end_month : int
            Ending month
        market_type : str
            'sii' or 'otc'
        output_dir : str
            Output directory (default: 'data')
        delay : int
            Delay between requests in seconds
        
        Returns:
        --------
        list
            List of saved file paths
        """
        
        current_year = start_year
        current_month = start_month
        saved_files = []
        
        while (current_year < end_year) or (current_year == end_year and current_month <= end_month):
            df = self.download_revenue_data(current_year, current_month, market_type)
            
            if df is not None:
                filename = self.save_to_csv(df, current_year, current_month, market_type, output_dir)
                if filename:
                    saved_files.append(filename)
            
            # Move to next month
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
            
            # Delay to avoid overwhelming the server
            if (current_year < end_year) or (current_year == end_year and current_month <= end_month):
                print(f"Waiting {delay} seconds before next request...")
                time.sleep(delay)
        
        return saved_files
    
    @staticmethod
    def convert_ad_to_roc(ad_year):
        """
        Convert AD year to ROC year
        
        Parameters:
        -----------
        ad_year : int
            AD year (e.g., 2024)
        
        Returns:
        --------
        int
            ROC year (e.g., 113)
        """
        return ad_year - 1911
    
    @staticmethod
    def convert_roc_to_ad(roc_year):
        """
        Convert ROC year to AD year
        
        Parameters:
        -----------
        roc_year : int
            ROC year (e.g., 113)
        
        Returns:
        --------
        int
            AD year (e.g., 2024)
        """
        return roc_year + 1911


def main():
    """
    Example usage
    """
    downloader = MOPSRevenueDownloader()
    
    # Example 1: Download single month
    # ROC year 113 = AD 2024
    roc_year = 113
    month = 7
    
    print("=" * 60)
    print("Downloading Listed Companies (上市) Revenue Data")
    print("=" * 60)
    df_sii = downloader.download_revenue_data(roc_year, month, market_type='sii')
    if df_sii is not None:
        print(f"\nData preview (first 5 rows):")
        print(df_sii.head())
        downloader.save_to_csv(df_sii, roc_year, month, market_type='sii')
    
    print("\n" + "=" * 60)
    print("Downloading OTC Companies (上櫃) Revenue Data")
    print("=" * 60)
    df_otc = downloader.download_revenue_data(roc_year, month, market_type='otc')
    if df_otc is not None:
        print(f"\nData preview (first 5 rows):")
        print(df_otc.head())
        downloader.save_to_csv(df_otc, roc_year, month, market_type='otc')
    
    # Example 2: Download multiple months
    # Uncomment the following lines to download data for a range of months
    """
    print("\n" + "=" * 60)
    print("Downloading Multiple Months")
    print("=" * 60)
    saved_files = downloader.download_multiple_months(
        start_year=113,  # ROC year
        start_month=1,
        end_year=113,
        end_month=12,
        market_type='sii',
        output_dir='./revenue_data',
        delay=2
    )
    print(f"\nDownloaded {len(saved_files)} files:")
    for f in saved_files:
        print(f"  - {f}")
    """
    
    # Example 3: Convert between AD and ROC years
    ad_year = 2024
    roc_year = MOPSRevenueDownloader.convert_ad_to_roc(ad_year)
    print(f"\n{ad_year} AD = {roc_year} ROC")
    print(f"{roc_year} ROC = {MOPSRevenueDownloader.convert_roc_to_ad(roc_year)} AD")


if __name__ == "__main__":
    main()