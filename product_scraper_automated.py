#!/usr/bin/env python3
"""
E-commerce Product Data Scraper - URL Automation Version
=======================================================
This script extracts product information from thehouseofrare.com webpages.
It can work with both live URLs and local HTML files, organizing the data 
into a structured JSON format.

Features:
- Direct URL scraping from thehouseofrare.com
- Dynamic content loading with wait strategies
- Local HTML file processing
- Comprehensive product data extraction
- JSON output generation

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
        # Helper method to check if a source string is a URL or file path
        self.product_data = {}
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

    def _wait_for_dynamic_content(self, soup, max_retries=3):
        """
        Wait for dynamic content to load by checking for key elements

        Args:
            soup: BeautifulSoup object
            max_retries: Maximum number of retries

        Returns:
            bool: True if content appears to be loaded
        """
        retry_count = 0
        while retry_count < max_retries:
            # Check for key product elements that indicate page is fully loaded
            key_elements = [
                soup.find('input', {'name': 'Size'}),
                soup.find('input', {'name': 'fabric'}),
                soup.find('div', class_='compare-price-wrapper'),
                soup.find('script', string=lambda x: x and 'moeApp.product' in x)
            ]

            loaded_elements = sum(1 for element in key_elements if element)

            if loaded_elements >= 3:  # At least 3 out of 4 key elements found
                logger.info(
                    f"Dynamic content loaded successfully ({loaded_elements}/4 elements found)")
                return True

            logger.info(
                f"Waiting for dynamic content... ({loaded_elements}/4 elements loaded)")
            time.sleep(1)  # Wait 1 second before retry
            retry_count += 1

        logger.warning("Dynamic content may not be fully loaded")
        return False

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

                # Make request with retries for dynamic content
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        response = requests.get(
                            self.source, headers=headers, timeout=30)
                        response.raise_for_status()

                        html_content = response.text
                        logger.info(
                            f"Successfully fetched content from URL: {self.source}")
                        break

                    except requests.exceptions.RequestException as e:
                        if attempt == max_attempts - 1:
                            raise
                        logger.warning(
                            f"Attempt {attempt + 1} failed: {e}. Retrying...")
                        time.sleep(2)

            else:
                # Load from file (existing functionality)
                file_path = Path(self.source)
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                logger.info(f"Successfully loaded HTML file: {file_path}")

            self.soup = BeautifulSoup(html_content, 'html.parser')

            # Wait for dynamic content if loading from URL
            if self.is_url:
                self._wait_for_dynamic_content(self.soup)

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

                    # Extract product ID
                    id_match = re.search(r'"id":\s*"(\d+)"', script.string)
                    if id_match:
                        basic_info['product_id'] = id_match.group(1)

                    # Extract handle
                    handle_match = re.search(
                        r'"handle":\s*"([^"]+)"', script.string)
                    if handle_match:
                        basic_info['product_handle'] = handle_match.group(1)

                    # Extract vendor
                    vendor_match = re.search(
                        r'"vendor":\s*"([^"]+)"', script.string)
                    if vendor_match:
                        basic_info['brand'] = vendor_match.group(1)

                    # Extract product type
                    type_match = re.search(
                        r'"product_type":\s*"([^"]+)"', script.string)
                    if type_match:
                        basic_info['product_type'] = type_match.group(1)

            # Extract main product name from h1 and h2 tags
            main_title = self.soup.find('h1', class_='main-title')
            if main_title:
                title_span = main_title.find('span')
                if title_span:
                    basic_info['main_title'] = title_span.get_text().strip()

            sub_title = self.soup.find('h2', class_='sub-title')
            if sub_title:
                basic_info['sub_title'] = sub_title.get_text().strip()

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
                        pricing_info['original_price_formatted'] = price_text

                # Sale price
                regular_price = price_wrapper.find(
                    'span', class_='regular-price')
                if regular_price:
                    price_text = regular_price.get_text().strip()
                    price_match = re.search(r'₹\s*([\d,]+)', price_text)
                    if price_match:
                        pricing_info['sale_price'] = int(
                            price_match.group(1).replace(',', ''))
                        pricing_info['sale_price_formatted'] = price_text

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

            # Extract currency
            pricing_info['currency'] = 'INR'

            logger.info("Successfully extracted pricing information")

        except Exception as e:
            logger.error(f"Error extracting pricing info: {e}")

        return pricing_info

    def extract_product_specifications(self):
        """Extract product specifications and attributes"""
        specifications = {}

        try:
            # Extract from specification input fields (text inputs, not hidden)
            spec_names = ['fabric', 'fit', 'closure',
                          'collar', 'sleeve', 'pattern', 'occasion']

            for spec_name in spec_names:
                spec_input = self.soup.find('input', {'name': spec_name})
                if spec_input:
                    value = spec_input.get('value', '').strip()
                    if value:
                        specifications[spec_name] = value
                    elif spec_name == 'pattern':
                        # Default for empty pattern
                        specifications[spec_name] = 'SOLID'

            # Extract from product description
            description_content = self.soup.find(
                'div', class_='content-wrapper')
            if description_content:
                description_text = description_content.get_text()

                # Extract specific details from description
                if 'Cotton' in description_text:
                    specifications['material_type'] = 'Cotton'
                if 'Regular collar' in description_text:
                    specifications['collar_type'] = 'Regular collar'
                if 'Short sleeve' in description_text or 'Half Sleeve' in description_text:
                    specifications['sleeve_length'] = 'Half Sleeve'
                if 'Button fastening' in description_text:
                    specifications['closure_type'] = 'Button'
                if 'Tailored Fit' in description_text:
                    specifications['fit_type'] = 'Tailored Fit'

            # Extract color from variants
            color_options = self.soup.find_all('div', class_='color-title')
            colors = []
            for color in color_options:
                color_text = color.get_text().strip()
                if color_text:
                    colors.append(color_text)
            if colors:
                specifications['available_colors'] = colors

            logger.info("Successfully extracted product specifications")

        except Exception as e:
            logger.error(f"Error extracting specifications: {e}")

        return specifications

    def extract_size_availability(self):
        """Extract size options and availability"""
        size_info = {}

        try:
            sizes = []
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

                    sizes.append(size_value)
                    size_availability[size_value] = is_available

            if sizes:
                size_info['available_sizes'] = sizes
                size_info['size_availability'] = size_availability
                size_info['in_stock_sizes'] = [size for size,
                                               available in size_availability.items() if available]
                size_info['out_of_stock_sizes'] = [
                    size for size, available in size_availability.items() if not available]

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
                        # Clean and extract URLs - handle multiple image formats
                        image_urls_raw = images_match.group(1)
                        urls = re.findall(
                            r'"([^"]*\.(jpg|jpeg|png|webp)[^"]*)"', image_urls_raw, re.IGNORECASE)
                        for url_match in urls:
                            # Get the full URL from the tuple
                            url = url_match[0]
                            # Remove escaped slashes from JSON
                            clean_url = url.replace('\\/', '/')

                            if clean_url.startswith('//'):
                                image_urls.append('https:' + clean_url)
                            elif clean_url.startswith('/'):
                                image_urls.append(
                                    'https://thehouseofrare.com' + clean_url)
                            else:
                                # Method 2: Extract from img tags with product-related alt text
                                image_urls.append(clean_url)
            if not image_urls:
                product_images = self.soup.find_all(
                    'img', alt=re.compile(r'.*', re.IGNORECASE))
                for img in product_images:
                    src = img.get('src') or img.get('data-src')
                    if src and ('product' in src.lower() or 'cdn.shopify' in src):
                        # Clean escaped slashes
                        clean_src = src.replace('\\/', '/')

                        if clean_src.startswith('//'):
                            clean_src = 'https:' + clean_src
                        elif clean_src.startswith('/'):
                            clean_src = 'https://thehouseofrare.com' + clean_src
                        image_urls.append(clean_src)

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
                images['total_images'] = len(unique_images)

            logger.info(
                f"Successfully extracted {len(unique_images)} product images")

        except Exception as e:
            logger.error(f"Error extracting images: {e}")

        return images

    def extract_ratings_reviews(self):
        """Extract ratings and review information"""
        ratings_info = {}

        try:
            # Extract from JSON-LD structured data (most reliable)
            scripts = self.soup.find_all('script', type='application/ld+json')
            for script in scripts:
                if script.string:
                    try:
                        data = json.loads(script.string)
                        if isinstance(data, dict) and data.get('@type') == 'Product':
                            aggregate_rating = data.get('aggregateRating', {})
                            if aggregate_rating:
                                ratings_info['average_rating'] = float(
                                    aggregate_rating.get('ratingValue', 0))
                                ratings_info['total_reviews'] = int(
                                    aggregate_rating.get('reviewCount', 0))
                                ratings_info['rating_scale'] = '5.0'
                    except json.JSONDecodeError:
                        continue

            # Fallback: Extract from script data
            if not ratings_info:
                scripts = self.soup.find_all('script')
                for script in scripts:
                    if script.string and 'window.yotpo' in script.string:
                        # Extract average rating
                        rating_pattern = r'"average_score":\s*(\d+\.?\d*)'
                        rating_match = re.search(rating_pattern, script.string)
                        if rating_match:
                            ratings_info['average_rating'] = float(
                                rating_match.group(1))

                        # Extract total reviews
                        reviews_pattern = r'"reviews_count":\s*(\d+)'
                        reviews_match = re.search(
                            reviews_pattern, script.string)
                        if reviews_match:
                            ratings_info['total_reviews'] = int(
                                reviews_match.group(1))

            logger.info("Successfully extracted ratings information")

        except Exception as e:
            logger.error(f"Error extracting ratings: {e}")

        return ratings_info

    def _filter_unwanted_fields(self, data):
        """
        Remove unwanted fields from the product data

        Args:
            data (dict): Product data dictionary

        Returns:
            dict: Filtered product data without unwanted fields
        """
        # Fields to exclude from JSON output
        unwanted_fields = {
            'original_price_formatted',
            'sale_price_formatted',
            'currency',
            'current_color',
            'available_sizes',
            'in_stock_sizes',
            'out_of_stock_sizes',
            'total_images',
            'rating_scale'
        }

        filtered_data = {}

        for category_key, category_data in data.items():
            if isinstance(category_data, dict):
                # Filter out unwanted fields from this category
                filtered_category = {
                    key: value for key, value in category_data.items()
                    if key not in unwanted_fields
                }
                filtered_data[category_key] = filtered_category
            else:
                # Keep non-dict values as is
                filtered_data[category_key] = category_data

        logger.info(
            f"Filtered out unwanted fields: {', '.join(unwanted_fields)}")
        return filtered_data

    def scrape_all_data(self):
        """Scrape all product data and organize into categories"""
        logger.info("Starting product data extraction...")

        # Load HTML content
        self.load_html()

        # Extract all data categories
        self.product_data = {
            'basic_information': self.extract_basic_info(),
            'pricing_information': self.extract_pricing_info(),
            'product_specifications': self.extract_product_specifications(),
            'size_and_availability': self.extract_size_availability(),
            'product_images': self.extract_product_images(),
            'ratings_and_reviews': self.extract_ratings_reviews()
        }

        # Filter out unwanted fields
        self.product_data = self._filter_unwanted_fields(self.product_data)

        logger.info("Product data extraction completed successfully")
        return self.product_data

    def save_to_json(self, filename=None):
        """Save extracted data to JSON file"""
        try:
            if not filename:
                # Generate filename from product handle or source
                handle = self.product_data.get('basic_information', {}).get(
                    'product_handle', 'product')
                filename = f"{handle}_product_data.json"

            if self.is_url:
                output_path = Path.cwd() / filename
            else:
                source_path = Path(self.source)
                output_path = source_path.parent / filename

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
        print("\n" + "="*60)
        print("📊 PRODUCT DATA EXTRACTION SUMMARY")
        print("="*60)

        basic = self.product_data.get('basic_information', {})
        pricing = self.product_data.get('pricing_information', {})
        specs = self.product_data.get('product_specifications', {})
        sizes = self.product_data.get('size_and_availability', {})
        images = self.product_data.get('product_images', {})
        ratings = self.product_data.get('ratings_and_reviews', {})

        print(f"🔹 Product Information:")
        print(f"   • Name: {basic.get('main_title', 'N/A')}")
        print(f"   • Brand: {basic.get('brand', 'N/A')}")
        print(f"   • Type: {basic.get('product_type', 'N/A')}")
        print(f"   • ID: {basic.get('product_id', 'N/A')}")

        print(f"🔹 Pricing:")
        print(f"   • Original: ₹{pricing.get('original_price', 'N/A')}")
        print(f"   • Sale: ₹{pricing.get('sale_price', 'N/A')}")
        print(f"   • Discount: {pricing.get('discount_percentage', 'N/A')}")
        print(f"   • Savings: ₹{pricing.get('savings_amount', 'N/A')}")

        print(f"🔹 Specifications:")
        for key, value in specs.items():
            if value and key not in ['available_colors']:
                print(f"   • {key.title()}: {value}")

        print(f"🔹 Size & Availability:")
        size_availability = sizes.get('size_availability', {})
        in_stock = [size for size,
                    available in size_availability.items() if available]
        out_of_stock = [size for size,
                        available in size_availability.items() if not available]
        print(f"   • In Stock: {', '.join(in_stock) if in_stock else 'N/A'}")
        print(
            f"   • Out of Stock: {', '.join(out_of_stock) if out_of_stock else 'N/A'}")

        print(f"🔹 Images: {len(images.get('product_images', []))} found")

        print(f"🔹 Ratings:")
        print(f"   • Average: {ratings.get('average_rating', 'N/A')}/5.0")
        print(f"   • Reviews: {ratings.get('total_reviews', 'N/A')}")

        print("="*60)


def main():
    """Main function with URL automation"""
    # Example usage - can be modified to accept command line arguments

    # Test with URL
    test_url = "https://thehouseofrare.com/products/breath-rust"

    try:
        print("🚀 Testing URL scraping automation...")
        scraper = ProductScraper(test_url)
        product_data = scraper.scrape_all_data()
        output_file = scraper.save_to_json()
        scraper.print_summary()
        print(f"\n✅ Success! Data saved to: {output_file}")

    except Exception as e:
        print(f"\n❌ Error: {e}")

        # Fallback to HTML file if available
        html_file = r"c:\Users\Gourish\OneDrive - REVA University\Desktop\Sraped data\view-source_https___thehouseofrare.com_products_breath-rust.html"
        if Path(html_file).exists():
            print(f"\n🔄 Falling back to HTML file: {html_file}")
            try:
                scraper = ProductScraper(html_file)
                product_data = scraper.scrape_all_data()
                output_file = scraper.save_to_json()
                scraper.print_summary()
                print(
                    f"\n✅ Success with HTML file! Data saved to: {output_file}")
            except Exception as e2:
                print(f"\n❌ HTML file error: {e2}")


def scrape_product_url(url):
    """
    Convenience function to scrape any thehouseofrare.com product URL

    Args:
        url (str): Product URL from thehouseofrare.com

    Returns:
        dict: Extracted product data
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
