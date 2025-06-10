#!/usr/bin/env python3
"""
Fast Bulk Product Scraper using Sitemap URLs
===========================================
This script combines sitemap URL extraction with fast bulk product scraping.
It extracts URLs from sitemaps and scrapes product data quickly.

Features:
- Extract URLs from sitemap only
- Fast scraping (< 1 second per product)
- Generate combined CSV and JSON files
- Extract only product links
- Clean up individual files after combining

Author: GitHub Copilot
"""

# Importing the time module
# What: This brings in Python's time-related functions for delays and timing
# Why: We need to add delays between web requests and measure how long scraping takes
# How: We'll use time.sleep() to pause between requests and time tracking for performance
import time

# Importing the json module
# What: This brings in Python's built-in tool for working with JSON data format
# Why: We need to save product information as JSON files and create combined data files
# How: We'll use json.dump() to save data and json.loads() to read data
import json

# Importing the csv module
# What: This brings in Python's built-in tool for working with CSV (spreadsheet) files
# Why: We need to create CSV files that can be opened in Excel for easy data viewing
# How: We'll use csv.DictWriter() to create structured CSV files with headers
import csv

# Importing the os module
# What: This brings in operating system interaction tools
# Why: We need to delete temporary files and work with file system operations
# How: We'll use os.remove() to delete files after combining them
import os

# Importing Path from pathlib module
# What: This brings in modern file and folder path handling tools
# Why: We need to create directories, check if files exist, and manage file paths
# How: We'll use Path() to create directories and work with file locations
from pathlib import Path

# Importing datetime from datetime module
# What: This brings in tools for working with dates and times
# Why: We need to timestamp our files and measure how long scraping operations take
# How: We'll use datetime.now() to get current time and create timestamps
from datetime import datetime

# Importing the logging module
# What: This brings in Python's system for recording what the program is doing
# Why: We need to track progress, record successes, and log any errors during bulk scraping
# How: We'll use logger.info() for progress updates and logger.error() for problems
import logging

# Importing SitemapExtractor from our sitemap_extractor file
# What: This brings in our custom tool for extracting URLs from website sitemaps
# Why: We need to get a list of all product URLs from the website's sitemap
# How: We'll create a SitemapExtractor object to download and parse sitemap files
from sitemap_extractor import SitemapExtractor

# Importing ProductScraper from our product_scraper_automated file
# What: This brings in our custom tool for scraping individual product pages
# Why: We need to extract detailed information from each product page
# How: We'll create ProductScraper objects for each product URL we want to scrape
from product_scraper_automated import ProductScraper

# Setting up the logging system
# What: This configures how Python will record information about what the program is doing
# Why: We want to see detailed information about bulk scraping progress and any errors
# How: We set the level to INFO (shows informational messages) and define the message format
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Creating a logger object for this specific file
# What: This creates a logger that we can use throughout this file to record events
# Why: We want to track bulk scraping progress and save it to logs
# How: logger.info() will record normal events, logger.error() will record problems
logger = logging.getLogger(__name__)


# Creating a class called FastBulkScraper
# What: This defines a blueprint for objects that can scrape many products at once
# Why: We need an organized way to handle bulk scraping operations and data management
# How: We create a class that contains all methods needed for bulk product extraction
class FastBulkScraper:
    """Fast bulk scraper that only works with sitemap URLs"""

    # The __init__ method is a special function that runs when we create a new FastBulkScraper
    # What: This sets up the initial state of our bulk scraper object
    # Why: We need to store the sitemap URL and prepare variables for bulk data collection
    # How: We save the sitemap URL and initialize empty variables for tracking progress
    def __init__(self, sitemap_url):
        """
        Initialize fast bulk scraper - Only accepts sitemap URLs

        Args:
            sitemap_url (str): Sitemap URL (must be a valid URL)
        """
        # Check if the input is a valid URL that starts with http:// or https://
        # What: This validates that we received a proper web URL, not a file path or invalid string
        # Why: This scraper is designed only for sitemap URLs, not individual product URLs or files
        # How: We check if the string starts with http:// or https:// using startswith()
        if not sitemap_url.startswith(('http://', 'https://')):
            # If it's not a valid URL, stop the program and show an error message
            # What: This creates an error that stops execution and explains what went wrong
            # Why: We need to prevent the user from using invalid inputs that won't work
            # How: ValueError creates an exception with a clear message about the requirement
            raise ValueError(
                "Only sitemap URLs are supported. Please provide a valid URL starting with http:// or https://")

        # Store the sitemap URL for later use
        # What: This saves the sitemap URL so we can access it throughout the scraping process
        # Why: We need to remember which sitemap we're working with for all operations
        # How: We assign the input parameter to self.sitemap_source to keep it available
        self.sitemap_source = sitemap_url

        # Set the delay time between requests to 0.8 seconds
        # What: This sets how long to wait between each product scraping request
        # Why: We need delays to be respectful to the website and avoid overwhelming their servers
        # How: We store 0.8 seconds as the delay time, which is fast but still polite
        self.delay = 0.8  # Fast scraping - 0.8 seconds between requests

        # Initialize empty list to store product URLs we extract from the sitemap
        # What: This creates a container to hold all the product URLs we find
        # Why: We need somewhere to store the URLs before we scrape them individually
        # How: We start with an empty list that we'll fill with URLs from the sitemap
        self.product_urls = []

        # Initialize empty list to store all the scraped product data
        # What: This creates a container to hold all the product information we collect
        # Why: We need somewhere to store the data from each product page we scrape
        # How: We start with an empty list that we'll fill with product data dictionaries
        self.scraped_data = []

        # Initialize empty list to track URLs that fail during scraping
        # What: This creates a container to store information about failed scraping attempts
        # Why: We need to track which products couldn't be scraped and why they failed
        # How: We start with an empty list that we'll fill with error information if needed
        self.failed_urls = []

        # Initialize empty list to track temporary files we create during scraping
        # What: This creates a container to remember which individual files we create temporarily
        # Why: We need to delete these temporary files after we combine them into final files
        # How: We start with an empty list that we'll fill with file paths for later cleanup
        self.temp_files = []  # Track temporary individual files for cleanup

        # Initialize dictionary to store statistics about our scraping operation
        # What: This creates a container to track various numbers about our scraping progress
        # Why: We need to know how many products we processed, how many succeeded, failed, and timing
        # How: We create a dictionary with keys for different statistics, starting with default values
        self.stats = {
            'total_urls': 0,        # How many product URLs we found in total
            'successful_scrapes': 0,  # How many products we successfully scraped
            'failed_scrapes': 0,    # How many products failed to scrape
            'start_time': None,     # When we started the scraping process
            'end_time': None        # When we finished the scraping process
        }    # Method to extract product URLs from the sitemap
    # What: This downloads the sitemap and extracts only the product page URLs
    # Why: We need a list of product URLs before we can scrape individual products
    # How: We use SitemapExtractor to download and parse the sitemap, then filter for product URLs

    def extract_product_urls(self, url_pattern=None, max_urls=None):
        """
        Extract only product URLs from sitemap

        Args:
            url_pattern (str): Optional regex pattern to filter URLs
            max_urls (int): Maximum number of URLs to extract

        Returns:
            list: List of product URLs only
        """
        # Use try-except to handle any errors during URL extraction
        # What: This wraps our code in error handling to catch download or parsing problems
        # Why: Sitemap downloads can fail, so we need to handle errors gracefully
        # How: If anything goes wrong, we'll log the error and re-raise it
        try:
            # Print a user-friendly message about what we're doing
            # What: This shows the user that we're starting to extract URLs from the sitemap
            # Why: Users want to see progress and know what the program is doing
            # How: We use print() to display a message with the sitemap URL
            print(
                f"🔗 Extracting product URLs from sitemap: {self.sitemap_source}")

            # Create a SitemapExtractor object to handle the sitemap processing
            # What: This creates an instance of our SitemapExtractor class
            # Why: We need a specialized tool to download and parse XML sitemap files
            # How: We pass our sitemap URL to create a new SitemapExtractor object
            extractor = SitemapExtractor(self.sitemap_source)

            # Download and parse the sitemap content
            # What: This downloads the XML sitemap file and processes it into usable data
            # Why: We need to get the sitemap content before we can extract URLs
            # How: We call the load_sitemap() method which handles download and parsing
            extractor.load_sitemap()

            # Extract product URLs from the loaded sitemap, optionally with pattern filtering
            # What: This gets all product URLs from the sitemap, possibly filtered by pattern
            # Why: We only want product URLs, not other pages like categories or info pages
            # How: We call extract_product_urls() which filters for /products/ URLs
            url_data = extractor.extract_product_urls(url_pattern)

            # Extract just the URLs (product links only)
            urls = []
            for data in url_data:
                if isinstance(data, dict):
                    url = data.get('url', '')
                else:
                    url = str(data)

                # Ensure it's a product URL
                if '/products/' in url:
                    urls.append(url)

            # Limit URLs if specified
            if max_urls and len(urls) > max_urls:
                urls = urls[:max_urls]
                print(f"📝 Limited to first {max_urls} URLs")

            self.product_urls = urls
            self.stats['total_urls'] = len(urls)

            print(f"✅ Extracted {len(urls)} product URLs")
            return urls

        except Exception as e:
            logger.error(f"Error extracting URLs: {e}")
            raise

    def fast_scrape_products(self, output_dir="scraped_products"):
        """
        Fast scrape all extracted product URLs

        Args:
            output_dir (str): Directory to save scraped data

        Returns:
            dict: Scraping results and statistics
        """
        if not self.product_urls:
            raise ValueError(
                "No URLs to scrape. Call extract_product_urls() first.")

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        self.stats['start_time'] = datetime.now()

        print(
            f"\n🚀 Starting fast bulk scraping of {len(self.product_urls)} products...")
        print(f"📁 Output directory: {output_path}")
        print(f"⏱️  Delay between requests: {self.delay} seconds")

        for i, url in enumerate(self.product_urls, 1):
            try:
                print(
                    # Create scraper and extract data
                    f"[{i}/{len(self.product_urls)}] Scraping: {url.split('/')[-1]}")
                scraper = ProductScraper(url)
                raw_data = scraper.scrape_all_data()

                # Transform data to match required schema
                product_data = self._transform_data_schema(raw_data, url)

                # Save individual file temporarily
                product_handle = raw_data.get('basic_information', {}).get(
                    'product_handle', f'product_{i}')
                individual_file = output_path / f"{product_handle}.json"

                with open(individual_file, 'w', encoding='utf-8') as f:
                    json.dump(product_data, f, indent=2, ensure_ascii=False)

                # Track temp file for cleanup
                # Add to combined data
                self.temp_files.append(individual_file)
                # Don't add metadata here - it's already in the transformed data
                self.scraped_data.append(product_data)

                self.stats['successful_scrapes'] += 1

                # Show quick info
                basic_info = product_data.get('basic_information', {})
                product_name = basic_info.get('main_title', 'Unknown Product')
                pricing = product_data.get('pricing_information', {})
                price = pricing.get('sale_price', 'N/A')

                print(f"✅ {product_name} - ₹{price}")

                # Fast rate limiting
                if i < len(self.product_urls):
                    time.sleep(self.delay)

            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                self.failed_urls.append({
                    'url': url,
                    'error': str(e),
                    'index': i
                })
                self.stats['failed_scrapes'] += 1
                # Continue with next URL after shorter delay
                print(f"❌ Failed: {e}")
                time.sleep(self.delay / 2)

        self.stats['end_time'] = datetime.now()
        return self._generate_final_files(output_path)

    def _transform_data_schema(self, raw_data, url):
        """
        Transform raw scraped data to match the required JSON schema

        Args:
            raw_data (dict): Raw data from ProductScraper
            url (str): Product URL

        Returns:
            dict: Transformed data matching required schema
        """
        basic_info = raw_data.get('basic_information', {})
        pricing_info = raw_data.get('pricing_information', {})
        specs = raw_data.get('product_specifications', {})
        size_data = raw_data.get('size_and_availability', {})
        images = raw_data.get('product_images', {})

        # Transform size availability to the required format
        size_availability = {}
        if size_data.get('size_availability'):
            size_availability = size_data['size_availability']

        transformed_data = {
            "basic_information": {
                "page_title": basic_info.get('page_title', ''),
                "main_title": basic_info.get('main_title', ''),
                "url": url
            },
            "pricing_information": {
                "original_price": pricing_info.get('original_price', 0),
                "sale_price": pricing_info.get('sale_price', 0),
                "discount_percentage": pricing_info.get('discount_percentage', ''),
                "savings_amount": pricing_info.get('savings_amount', 0)
            },
            "product_specifications": {
                "fabric": specs.get('fabric', ''),
                "fit": specs.get('fit', ''),
                "closure": specs.get('closure', ''),
                "collar": specs.get('collar', ''),
                "sleeve": specs.get('sleeve', ''),
                "pattern": specs.get('pattern', ''),
                "occasion": specs.get('occasion', '')
            },
            "size_availability": size_availability,
            "product_images": {
                "product_images": images.get('product_images', []),
                "main_image": images.get('main_image', '')
            }
        }

        return transformed_data

    def _generate_final_files(self, output_path):
        """Generate final CSV and JSON files, then cleanup individual files"""
        duration = self.stats['end_time'] - self.stats['start_time']

        print(f"\n📝 Generating final files...")

        # 1. Generate combined JSON file
        combined_json_file = output_path / "all_products.json"
        with open(combined_json_file, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)

        # 2. Generate comprehensive CSV file
        csv_file = output_path / "all_products.csv"
        self._create_comprehensive_csv(csv_file)

        # 3. Save failed URLs if any
        failed_file = None
        if self.failed_urls:
            failed_file = output_path / "failed_urls.json"
            with open(failed_file, 'w', encoding='utf-8') as f:
                json.dump(self.failed_urls, f, indent=2, ensure_ascii=False)

        # 4. Cleanup individual JSON files
        print(f"🧹 Cleaning up {len(self.temp_files)} individual files...")
        cleaned_files = 0
        for temp_file in self.temp_files:
            try:
                if temp_file.exists():
                    os.remove(temp_file)
                    cleaned_files += 1
            except Exception as e:
                logger.warning(f"Could not delete {temp_file}: {e}")

        print(f"✅ Cleaned up {cleaned_files} individual files")

        # Generate report
        report = {
            'scraping_summary': {
                'total_urls': self.stats['total_urls'],
                'successful_scrapes': self.stats['successful_scrapes'],
                'failed_scrapes': self.stats['failed_scrapes'],
                'success_rate': f"{(self.stats['successful_scrapes'] / self.stats['total_urls'] * 100):.1f}%",
                'duration': str(duration),
                'average_time_per_product': f"{duration.total_seconds() / self.stats['total_urls']:.1f}s"
            },
            'files_created': {
                'combined_json': str(combined_json_file),
                'combined_csv': str(csv_file),
                'failed_urls': str(failed_file) if failed_file else None,
                'individual_files_cleaned': cleaned_files
            },
            'sitemap_source': self.sitemap_source,
            'scraping_completed_at': self.stats['end_time'].isoformat()
        }

        # Save report
        report_file = output_path / "scraping_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        # Print summary
        self._print_final_summary(report)

        return report

    def _create_comprehensive_csv(self, csv_file):
        """Create comprehensive CSV with all product data"""
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            # Define comprehensive fieldnames
            fieldnames = [
                'product_name', 'url', 'original_price', 'sale_price',
                'discount_percentage', 'savings_amount', 'fabric', 'fit',
                'closure', 'collar', 'sleeve', 'pattern', 'occasion',
                'total_images', 'main_image'
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for product_data in self.scraped_data:
                basic = product_data.get('basic_information', {})
                pricing = product_data.get('pricing_information', {})
                specs = product_data.get('product_specifications', {})
                images = product_data.get('product_images', {})

                row = {
                    'product_name': basic.get('main_title', ''),
                    'url': basic.get('url', ''),
                    'original_price': pricing.get('original_price', ''),
                    'sale_price': pricing.get('sale_price', ''),
                    'discount_percentage': pricing.get('discount_percentage', ''),
                    'savings_amount': pricing.get('savings_amount', ''),
                    'fabric': specs.get('fabric', ''),
                    'fit': specs.get('fit', ''),
                    'closure': specs.get('closure', ''),
                    'collar': specs.get('collar', ''),
                    'sleeve': specs.get('sleeve', ''),
                    'pattern': specs.get('pattern', ''),
                    'occasion': specs.get('occasion', ''),
                    'total_images': len(images.get('product_images', [])),
                    'main_image': images.get('main_image', '')
                }
                writer.writerow(row)

    def _print_final_summary(self, report):
        """Print final scraping summary"""
        summary = report['scraping_summary']

        print("\n" + "="*70)
        print("📊 FAST BULK SCRAPING COMPLETED")
        print("="*70)

        print(f"🔗 Source: {self.sitemap_source}")
        print(f"📦 Total Products: {summary['total_urls']}")
        print(f"✅ Successful: {summary['successful_scrapes']}")
        print(f"❌ Failed: {summary['failed_scrapes']}")
        print(f"📈 Success Rate: {summary['success_rate']}")
        print(f"⏱️  Total Duration: {summary['duration']}")
        print(f"🕐 Avg Time/Product: {summary['average_time_per_product']}")

        files = report['files_created']
        print(f"\n📁 Final Files Created:")
        print(f"   • Combined JSON: {files['combined_json']}")
        print(f"   • Combined CSV: {files['combined_csv']}")
        if files['failed_urls']:
            print(f"   • Failed URLs: {files['failed_urls']}")
        print(
            f"   • Individual files cleaned: {files['individual_files_cleaned']}")

        print("="*70)
        print("✅ All requirements completed successfully!")


# Convenience function for easy bulk scraping without creating objects manually
# What: This provides a simple way to scrape products without dealing with class objects
# Why: Users want a simple function they can call directly without complex setup
# How: This function creates the scraper object internally and handles all the steps
def fast_bulk_scrape(sitemap_url, max_products=None, output_dir="scraped_products", url_pattern=None):
    """
    Fast convenience function for bulk scraping from sitemap URL only

    Args:
        sitemap_url (str): Sitemap URL (must be valid URL)
        max_products (int): Maximum number of products to scrape
        output_dir (str): Output directory for scraped data
        url_pattern (str): Regex pattern to filter URLs

    Returns:
        dict: Scraping report
    """
    # Use try-except to handle any errors during the bulk scraping process
    # What: This wraps all the scraping operations in error handling
    # Why: Many things can go wrong during bulk scraping, so we need to catch errors
    # How: If anything fails, we'll log the error and re-raise it for the caller
    try:
        # Create a FastBulkScraper object with the provided sitemap URL
        # What: This creates an instance of our bulk scraper class
        # Why: We need a scraper object to perform the bulk operations
        # How: We pass the sitemap URL to initialize the scraper
        scraper = FastBulkScraper(sitemap_url)

        # Extract product URLs from the sitemap with optional filtering and limits
        # What: This downloads the sitemap and extracts a list of product URLs
        # Why: We need URLs before we can scrape individual products
        # How: We call extract_product_urls() with optional pattern and max limit
        urls = scraper.extract_product_urls(url_pattern, max_products)

        # Check if we found any URLs to scrape
        # What: This verifies that we have at least one product URL to work with
        # Why: If no URLs were found, there's nothing to scrape
        # How: We check if the urls list is empty and return None if so
        if not urls:
            # Print an error message and return None if no URLs found
            # What: This informs the user that no product URLs were found
            # Why: The user needs to know why the scraping didn't proceed
            # How: We print a clear error message and return None
            print("❌ No product URLs found to scrape")
            return None

        # Start the fast scraping process on all extracted URLs
        # What: This scrapes all the product URLs and creates output files
        # Why: This is the main operation that actually collects product data
        # How: We call fast_scrape_products() which handles individual scraping and file creation
        report = scraper.fast_scrape_products(output_dir)

        # Return the scraping report with statistics and file information
        # What: This gives the caller detailed information about what was accomplished
        # Why: The caller needs to know how many products were scraped and where files are
        # How: We return the report dictionary with success rates, timing, and file paths
        return report

    # If any error occurs, log it and re-raise for the caller to handle
    # What: This catches any errors that occurred during the scraping process
    # Why: We need to log errors for debugging and let the caller know something failed
    # How: We log the error details and re-raise the exception
    except Exception as e:
        # Log the error with details for debugging
        # What: This records what went wrong during bulk scraping
        # Why: We need error information for troubleshooting
        # How: We use logger.error() to record the exception details
        logger.error(f"Fast bulk scraping failed: {e}")

        # Re-raise the exception so the caller knows something failed
        # What: This passes the error up to whatever code called this function
        # Why: The calling code needs to know that scraping failed
        # How: We use 'raise' to re-throw the exception
        raise


def main():
    """Main function for testing fast bulk scraping"""
    print("🚀 Testing Fast Bulk Product Scraping from Sitemap")
    print("="*60)

    try:
        # Test with small batch
        sitemap_url = "https://thehouseofrare.com/sitemap.xml"

        print(f"📍 Sitemap: {sitemap_url}")
        print(f"📦 Max Products: 10 (for testing)")
        print(f"⏱️  Fast scraping mode: ~0.8 seconds per product")

        # Run fast bulk scraping
        report = fast_bulk_scrape(
            sitemap_url=sitemap_url,
            max_products=10,  # Small number for testing
            output_dir="fast_bulk_scraping"
        )

        if report:
            print(f"\n✅ Fast bulk scraping completed successfully!")
            print(f"📊 Check the 'fast_bulk_scraping' directory for results")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Main function failed: {e}")


if __name__ == "__main__":
    main()
