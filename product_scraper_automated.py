#!/usr/bin/env python3
"""
E-commerce Product Data Scraper - Flat JSON Schema Version
=========================================================
This script extracts product information from thehouseofrare.com webpages
and outputs it in a flat JSON structure for easier consumption.

Features:
- Direct URL scraping from thehouseofrare.com
- Dynamic content loading with wait strategies
- Local HTML file processing
- Flat JSON output structure
- Individual size availability fields

Author: GitHub Copilot
"""

# Importing the json module
# What: This brings in Python's built-in tool for working with JSON data format
# Why: We need to save product information as JSON files and read JavaScript data from websites
# How: We'll use json.dump() to save data and json.loads() to convert text into Python objects
import json

# Importing the re module (regular expressions)
# What: This brings in Python's pattern matching and text searching tools
# Why: We need to find specific patterns in text like prices, product IDs, and image URLs
# How: We'll use re.search() and re.findall() to extract data from HTML and JavaScript code
import re

# Importing the requests module
# What: This brings in a library for downloading web pages from the internet
# Why: We need to fetch web page content from thehouseofrare.com to scrape product data
# How: We'll use requests.get() to download web page HTML content from URLs
import requests

# Importing the time module
# What: This brings in Python's time-related functions for delays and pausing
# Why: We need to wait between operations to let web pages load completely
# How: We'll use time.sleep() to pause execution and give websites time to load
import time

# Importing BeautifulSoup from bs4 module
# What: This brings in a powerful tool for reading and navigating HTML web pages
# Why: We need to find specific elements in HTML like prices, product names, and images
# How: We'll use BeautifulSoup to parse HTML and find elements by tags, classes, and IDs
from bs4 import BeautifulSoup

# Importing Path from pathlib module
# What: This brings in modern file and folder path handling tools
# Why: We need to work with file locations and create directories for saving scraped data
# How: We'll use Path() to create file paths and check if files exist on the computer
from pathlib import Path

# Importing urlparse from urllib.parse module
# What: This brings in URL analysis and validation tools
# Why: We need to check if a string is a valid URL and extract parts like domain names
# How: We'll use urlparse() to break down URLs and validate they're from the correct website
from urllib.parse import urlparse

# Importing the logging module
# What: This brings in Python's system for recording what the program is doing
# Why: We need to track progress, record successes, and log any errors that occur
# How: We'll use logger.info() for normal events and logger.error() for problems
import logging

# Setting up the logging system
# What: This configures how Python will record information about what the program is doing
# Why: We want to see detailed information about the scraping process and any errors
# How: We set the level to INFO (shows informational messages) and define the message format
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Creating a logger object for this specific file
# What: This creates a logger that we can use throughout this file to record events
# Why: We want to track what happens during scraping and save it to logs
# How: logger.info() will record normal events, logger.error() will record problems
logger = logging.getLogger(__name__)


# Creating a class called ProductScraper
# What: This defines a blueprint for objects that can scrape product information from web pages
# Why: We need an organized way to handle all the scraping functions and data extraction
# How: We create a class that contains all methods needed to extract product data from HTML
class ProductScraper:
    """Scraper class for extracting product information from HTML files or URLs"""

    # The __init__ method is a special function that runs when we create a new ProductScraper
    # What: This sets up the initial state of our scraper object
    # Why: We need to store the source (URL or file) and prepare variables for the scraped data
    # How: We save the source and initialize empty variables for soup and product_data
    def __init__(self, source):
        """
        Initialize the scraper with either a file path or URL

        Args:
            source (str): Path to HTML file or URL to scrape
        """
        # Store the source (either a URL or file path) that we want to scrape
        # What: This saves the input source for later use throughout the scraping process
        # Why: We need to remember what we're scraping whether it's a web URL or local file
        # How: We assign the input parameter to self.source to keep it available to all methods
        self.source = source

        # Check if the source is a URL or a file path
        # What: This determines whether we're working with a web URL or local HTML file
        # Why: We need to handle URLs and files differently when loading and processing content
        # How: We call a helper method that analyzes the source string to identify its type
        self.is_url = self._is_url(source)

        # Initialize an empty variable to store parsed HTML content
        # What: This creates a placeholder for the BeautifulSoup object that will hold our HTML
        # Why: BeautifulSoup will parse the HTML and we need somewhere to store the parsed content
        # How: We set it to None initially, will be filled when we load and parse the HTML
        self.soup = None

        # Initialize an empty dictionary to store all extracted product information
        # What: This creates a container for all the product data we'll collect during scraping
        # Why: We need a structured way to organize prices, names, images, sizes, and other data
        # How: We start with an empty dictionary that we'll fill with organized product data
        self.product_data = {}

    # Helper method to check if a source string is a URL or file path
    # What: This analyzes a string to determine if it's a web URL or local file path
    # Why: We need to handle URLs and files differently when loading content
    # How: We use urlparse to check if the string has URL components like scheme and domain
    def _is_url(self, source):
        """Check if the source is a URL"""
        # Use try-except to handle any errors during URL parsing
        # What: This wraps the URL parsing in error handling
        # Why: Invalid strings could cause urlparse to fail
        # How: If parsing fails, we'll assume it's not a URL and return False
        try:
            # Parse the source string to extract URL components
            # What: This breaks down the string into parts like scheme (http), domain, path, etc.
            # Why: We need to check if all required URL parts are present
            # How: urlparse() returns an object with scheme, netloc, path, and other URL parts
            result = urlparse(source)

            # Check if both scheme (http/https) and netloc (domain) are present
            # What: This verifies that the string has the essential parts of a valid URL
            # Why: A valid URL must have both a protocol (http/https) and a domain name
            # How: We use all() to check if both result.scheme and result.netloc have values
            return all([result.scheme, result.netloc])
        except:
            # If URL parsing fails, return False
            # What: This handles any errors by assuming the string is not a URL
            # Why: If we can't parse it as a URL, it's probably a file path
            # How: We simply return False without raising an error
            return False

    def _validate_url(self, url):
        """Validate if URL is from thehouseofrare.com"""
        parsed_url = urlparse(url)
        allowed_domains = ['thehouseofrare.com', 'www.thehouseofrare.com']
        if parsed_url.netloc.lower() not in allowed_domains:
            raise ValueError(
                f"URL must be from thehouseofrare.com domain. Got: {parsed_url.netloc}")
        return True

    def load_html(self):
        """Load and parse HTML from file or URL with dynamic content handling"""
        try:
            if self.is_url:
                self._validate_url(self.source)
                logger.info(f"Fetching content from URL: {self.source}")

                # Set up headers to mimic a real browser
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }

                response = requests.get(
                    self.source, headers=headers, timeout=30)
                response.raise_for_status()
                html_content = response.text
                logger.info(
                    f"Successfully fetched content from URL: {self.source}")

            else:
                # Load from file
                file_path = Path(self.source)
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                logger.info(f"Successfully loaded HTML file: {file_path}")

            self.soup = BeautifulSoup(html_content, 'html.parser')

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading HTML: {e}")
            raise

    def extract_basic_info(self):
        """Extract basic product information"""
        basic_info = {}

        try:
            # Extract from meta tags and JavaScript data
            title_element = self.soup.find('title')
            if title_element:
                basic_info['page_title'] = title_element.get_text().strip()

            # Extract from product scripts
            script_pattern = r'"title":\s*"([^"]+)"'
            scripts = self.soup.find_all('script')
            for script in scripts:
                if script.string and 'moeApp.product' in script.string:
                    title_match = re.search(script_pattern, script.string)
                    if title_match:
                        basic_info['product_title'] = title_match.group(1)

            # Extract main product name from h1 and h2 tags
            main_title = self.soup.find('h1', class_='main-title')
            if main_title:
                title_span = main_title.find('span')
                if title_span:
                    basic_info['main_title'] = title_span.get_text().strip()

            logger.info("Successfully extracted basic product information")

        except Exception as e:
            logger.error(f"Error extracting basic info: {e}")

        return basic_info

    def extract_pricing_info(self):
        """Extract pricing information"""
        pricing_info = {}

        try:
            # Extract from price wrapper
            price_wrapper = self.soup.find(
                'div', class_='compare-price-wrapper')
            if price_wrapper:
                # Original price (MRP)
                compare_price = price_wrapper.find(
                    'span', class_='compare-price')
                if compare_price:
                    price_text = compare_price.get_text().strip()
                    price_match = re.search(r'₹\s*([\d,]+)', price_text)
                    if price_match:
                        pricing_info['original_price'] = int(
                            price_match.group(1).replace(',', ''))

                # Sale price
                regular_price = price_wrapper.find(
                    'span', class_='regular-price')
                if regular_price:
                    price_text = regular_price.get_text().strip()
                    price_match = re.search(r'₹\s*([\d,]+)', price_text)
                    if price_match:
                        pricing_info['sale_price'] = int(
                            price_match.group(1).replace(',', ''))

                # Discount percentage
                discount_perc = price_wrapper.find('span', class_='perc_price')
                if discount_perc:
                    discount_text = discount_perc.get_text().strip()
                    pricing_info['discount_percentage'] = discount_text

            # Calculate savings
            if 'original_price' in pricing_info and 'sale_price' in pricing_info:
                savings = pricing_info['original_price'] - \
                    pricing_info['sale_price']
                pricing_info['savings_amount'] = savings

            logger.info("Successfully extracted pricing information")

        except Exception as e:
            logger.error(f"Error extracting pricing info: {e}")

        return pricing_info

    def extract_product_specifications(self):
        """Extract product specifications and attributes"""
        specifications = {}

        try:
            # Extract from specification input fields
            spec_names = ['fabric', 'fit', 'closure',
                          'collar', 'sleeve', 'pattern', 'occasion']

            for spec_name in spec_names:
                spec_input = self.soup.find('input', {'name': spec_name})
                if spec_input:
                    value = spec_input.get('value', '').strip()
                    if value:
                        specifications[spec_name] = value

            logger.info("Successfully extracted product specifications")

        except Exception as e:
            logger.error(f"Error extracting specifications: {e}")

        return specifications

    def extract_size_availability(self):
        """Extract size options and availability"""
        size_info = {}

        try:
            size_availability = {}

            # Extract from variant radios
            size_inputs = self.soup.find_all('input', attrs={'name': 'Size'})
            for size_input in size_inputs:
                size_value = size_input.get('value', '')
                if size_value:
                    # Check if size is available (not inactive)
                    parent = size_input.find_parent('h3')
                    is_available = True
                    if parent and 'inactive-option' in parent.get('class', []):
                        is_available = False

                    size_availability[size_value] = is_available

            size_info['size_availability'] = size_availability
            logger.info("Successfully extracted size information")

        except Exception as e:
            logger.error(f"Error extracting size info: {e}")

        return size_info

    def extract_product_images(self):
        """Extract product images"""
        images = {}

        try:
            image_urls = []

            # Method 1: Extract from script containing image URLs
            scripts = self.soup.find_all('script')
            for script in scripts:
                if script.string and 'images:' in script.string:
                    # Find the images array
                    images_pattern = r'images:\s*\[(.*?)\]'
                    images_match = re.search(
                        images_pattern, script.string, re.DOTALL)
                    if images_match:
                        # Clean and extract URLs
                        image_urls_raw = images_match.group(1)
                        urls = re.findall(
                            r'"([^"]*\.(jpg|jpeg|png|webp)[^"]*)"', image_urls_raw, re.IGNORECASE)
                        for url_match in urls:
                            url = url_match[0]
                            clean_url = url.replace('\\/', '/')

                            if clean_url.startswith('//'):
                                image_urls.append('https:' + clean_url)
                            elif clean_url.startswith('/'):
                                image_urls.append(
                                    'https://thehouseofrare.com' + clean_url)
                            else:
                                image_urls.append(clean_url)

            # Remove duplicates while preserving order
            unique_images = []
            seen = set()
            for url in image_urls:
                if url not in seen:
                    unique_images.append(url)
                    seen.add(url)

            if unique_images:
                images['product_images'] = unique_images
                images['main_image'] = unique_images[0] if unique_images else None

            logger.info(
                f"Successfully extracted {len(unique_images)} product images")

        except Exception as e:
            logger.error(f"Error extracting images: {e}")

        return images

    def create_flat_structure(self, nested_data):
        """
        Create a flat JSON structure from the nested product data

        What: This reorganizes nested product data into a single flat dictionary
        Why: The output should be a simple, flat JSON structure without nested categories
        How: We extract specific fields from each category and place them at the root level

        Args:
            nested_data (dict): Nested product data dictionary

        Returns:
            dict: Flat product data structure matching the desired schema
        """
        # What: Create an empty dictionary to store our flat structure
        # Why: We need a clean container to build our simplified output format
        # How: Initialize an empty dict that we'll populate with flattened data
        flat_data = {}

        # What: Extract basic information fields to root level
        # Why: Page title, product title, and URL should be at the top level
        # How: Get data from basic_information category and place it directly in flat_data
        basic_info = nested_data.get('basic_information', {})
        flat_data['page_title'] = basic_info.get('page_title', '')
        flat_data['main_title'] = basic_info.get('main_title', '')

        # What: Add the product URL to the output
        # Why: The schema requires the URL field for reference
        # How: Use the source URL if it's a URL, otherwise leave empty
        flat_data['url'] = self.source if self.is_url else ''

        # What: Extract pricing information to root level
        # Why: Price data should be easily accessible without nested structure
        # How: Get pricing data and place original_price, sale_price, etc. at root level
        pricing_info = nested_data.get('pricing_information', {})
        flat_data['original_price'] = pricing_info.get('original_price', 0)
        flat_data['sale_price'] = pricing_info.get('sale_price', 0)
        flat_data['discount_percentage'] = pricing_info.get(
            'discount_percentage', '')
        flat_data['savings_amount'] = pricing_info.get('savings_amount', 0)

        # What: Extract product specifications to root level
        # Why: Fabric, fit, collar, etc. should be directly accessible
        # How: Get each specification field and place it at the root level
        specs = nested_data.get('product_specifications', {})
        flat_data['fabric'] = specs.get('fabric', '')
        flat_data['fit'] = specs.get('fit', '')
        flat_data['closure'] = specs.get('closure', '')
        flat_data['collar'] = specs.get('collar', '')
        flat_data['sleeve'] = specs.get('sleeve', '')
        flat_data['pattern'] = specs.get('pattern', '')
        flat_data['occasion'] = specs.get('occasion', '')

        # What: Extract size availability as individual size fields
        # Why: Each size should be a separate field showing true/false availability
        # How: Convert size_availability dict into individual size-availability fields
        size_info = nested_data.get('size_and_availability', {})
        size_availability = size_info.get('size_availability', {})

        # What: Define standard size format mapping
        # Why: Convert from simple sizes (S, M, L) to size-measurement format (S-38, M-40)
        # How: Create a mapping dictionary for size codes to measurements
        size_mapping = {
            'XS': 'XS-36',
            'S': 'S-38',
            'M': 'M-40',
            'L': 'L-42',
            'XL': 'XL-44',
            'XXL': 'XXL-46',
            '3XL': '3XL-48'
        }

        # What: Add size availability fields for each standard size
        # Why: Each size needs its own boolean field in the flat structure
        # How: Loop through size mapping and set true/false based on availability
        for size_code, size_label in size_mapping.items():
            # Check if this size is available in the scraped data
            is_available = size_availability.get(size_code, False)
            flat_data[size_label] = is_available

        # What: Extract image information to root level
        # Why: Product images should be easily accessible as arrays
        # How: Get the product_images list and main_image from images category
        images_info = nested_data.get('product_images', {})
        flat_data['product_images'] = images_info.get('product_images', [])
        flat_data['main_image'] = images_info.get('main_image', '')

        # What: Log the successful creation of flat structure
        # Why: We want to track that the data transformation completed successfully
        # How: Use logger to record that we've created the flat JSON structure
        logger.info(
            "Successfully created flat JSON structure matching desired schema")
        return flat_data

    def scrape_all_data(self):
        """Scrape all product data and organize into flat structure"""
        # What: Log that we're starting the data extraction process
        # Why: We want to track when the scraping process begins
        # How: Use logger to record the start of product data extraction
        logger.info("Starting product data extraction...")

        # What: Load and parse the HTML content from URL or file
        # Why: We need the HTML content before we can extract any data
        # How: Call load_html() which handles both URLs and local files
        self.load_html()

        # What: Extract all data categories using existing extraction methods
        # Why: We need to gather all product information before flattening the structure
        # How: Call each extraction method and organize results into nested categories
        nested_data = {
            'basic_information': self.extract_basic_info(),
            'pricing_information': self.extract_pricing_info(),
            'product_specifications': self.extract_product_specifications(),
            'size_and_availability': self.extract_size_availability(),
            'product_images': self.extract_product_images()
        }

        # What: Convert nested structure to flat structure matching desired schema
        # Why: The output should be a flat JSON structure for easier consumption
        # How: Call create_flat_structure() to transform nested data into flat format
        self.product_data = self.create_flat_structure(nested_data)

        # What: Log successful completion of data extraction
        # Why: We want to track when the scraping process completes successfully
        # How: Use logger to record successful completion
        logger.info("Product data extraction completed successfully")
        return self.product_data

    def save_to_json(self, filename=None):
        """Save extracted data to JSON file"""
        try:
            if not filename:
                # What: Generate a filename from the product URL or source
                # Why: We need a meaningful filename for the JSON output file
                # How: Extract a handle from the URL path or use a default name
                if self.is_url:
                    # Extract product handle from URL path
                    url_parts = self.source.rstrip('/').split('/')
                    handle = url_parts[-1] if url_parts else 'product'
                else:
                    handle = 'product'
                filename = f"{handle}_product_data.json"

            # What: Determine where to save the JSON file
            # Why: URLs save to current directory, files save to same directory as source
            # How: Use Path to create appropriate file paths
            if self.is_url:
                output_path = Path.cwd() / filename
            else:
                source_path = Path(self.source)
                output_path = source_path.parent / filename

            # What: Write the product data to a JSON file
            # Why: We need to save the scraped data for later use
            # How: Use json.dump() with proper formatting and encoding
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(self.product_data, file,
                          indent=2, ensure_ascii=False)

            logger.info(f"Product data saved to: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            raise

    def print_summary(self):
        """Print a summary of extracted data"""
        # What: Display a formatted summary of all extracted product data
        # Why: Users need a quick overview of what data was successfully scraped
        # How: Print organized sections showing key product information
        print("\n" + "="*60)
        print("📊 PRODUCT DATA EXTRACTION SUMMARY")
        print("="*60)

        # What: Display basic product information
        # Why: Users need to see the product name, URL, and page title
        # How: Extract fields directly from the flat structure
        print(f"🔹 Product Information:")
        print(f"   • Page Title: {self.product_data.get('page_title', 'N/A')}")
        print(
            f"   • Product Name: {self.product_data.get('main_title', 'N/A')}")
        print(f"   • URL: {self.product_data.get('url', 'N/A')}")

        # What: Display pricing information
        # Why: Users need to see original price, sale price, and savings
        # How: Extract pricing fields directly from the flat structure
        print(f"🔹 Pricing:")
        print(
            f"   • Original: ₹{self.product_data.get('original_price', 'N/A')}")
        print(f"   • Sale: ₹{self.product_data.get('sale_price', 'N/A')}")
        print(
            f"   • Discount: {self.product_data.get('discount_percentage', 'N/A')}")
        print(
            f"   • Savings: ₹{self.product_data.get('savings_amount', 'N/A')}")

        # What: Display product specifications
        # Why: Users need to see fabric, fit, collar, sleeve, pattern, and occasion details
        # How: Extract specification fields directly from the flat structure
        print(f"🔹 Specifications:")
        spec_fields = ['fabric', 'fit', 'closure',
                       'collar', 'sleeve', 'pattern', 'occasion']
        for field in spec_fields:
            value = self.product_data.get(field, '')
            if value:
                print(f"   • {field.title()}: {value}")

        # What: Display size availability information
        # Why: Users need to see which sizes are in stock vs out of stock
        # How: Check each size field in the flat structure for true/false availability
        print(f"🔹 Size & Availability:")
        size_fields = ['XS-36', 'S-38', 'M-40',
                       'L-42', 'XL-44', 'XXL-46', '3XL-48']
        in_stock = [
            size for size in size_fields if self.product_data.get(size, False)]
        out_of_stock = [
            size for size in size_fields if size in self.product_data and not self.product_data.get(size, False)]
        print(f"   • In Stock: {', '.join(in_stock) if in_stock else 'N/A'}")
        print(
            f"   • Out of Stock: {', '.join(out_of_stock) if out_of_stock else 'N/A'}")

        # What: Display image information
        # Why: Users need to know how many product images were found
        # How: Count the length of the product_images array
        product_images = self.product_data.get('product_images', [])
        print(f"🔹 Images: {len(product_images)} found")
        if self.product_data.get('main_image'):
            print(f"   • Main Image: {self.product_data.get('main_image')}")

        print("="*60)


def main():
    """Main function with URL automation"""
    # Example usage - can be modified to accept command line arguments

    # Test with URL
    test_url = "https://thehouseofrare.com/products/breath-rust"

    try:
        print("🚀 Testing URL scraping automation with flat JSON structure...")
        scraper = ProductScraper(test_url)
        product_data = scraper.scrape_all_data()
        output_file = scraper.save_to_json()
        scraper.print_summary()
        print(f"\n✅ Success! Data saved to: {output_file}")

    except Exception as e:
        print(f"\n❌ Error: {e}")


def scrape_product_url(url):
    """
    Convenience function to scrape any thehouseofrare.com product URL

    Args:
        url (str): Product URL from thehouseofrare.com

    Returns:
        dict: Extracted product data in flat structure
    """
    try:
        scraper = ProductScraper(url)
        product_data = scraper.scrape_all_data()
        output_file = scraper.save_to_json()

        print(f"✅ Successfully scraped: {url}")
        print(f"📁 Data saved to: {output_file}")

        return product_data

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        raise


if __name__ == "__main__":
    main()
