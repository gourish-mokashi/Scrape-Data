#!/usr/bin/env python3
"""
Simple E-commerce Product Data Scraper
======================================
This script extracts product information from thehouseofrare.com webpages
and outputs it in a simple JSON structure.

Features:
- Direct URL scraping from thehouseofrare.com
- Dynamic content loading with wait strategies
- Local HTML file processing
- Simple JSON output structure
- Individual size availability fields

Author: GitHub Copilot
"""

import json
import re
import requests
import time
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ProductScraper:
    """Simple scraper class for extracting product information from HTML files or URLs"""

    def __init__(self, source):
        """
        Initialize the scraper with either a file path or URL

        Args:
            source (str): Path to HTML file or URL to scrape
        """
        self.source = source
        self.is_url = self._is_url(source)
        self.soup = None
        self.product_data = {}

    def _is_url(self, source):
        """Check if the source is a URL"""
        try:
            result = urlparse(source)
            return all([result.scheme, result.netloc])
        except:
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

    def create_simple_structure(self, nested_data):
        """Create a simple JSON structure from the nested product data"""
        simple_data = {}

        # Extract basic information fields to root level
        basic_info = nested_data.get('basic_information', {})
        simple_data['page_title'] = basic_info.get('page_title', '')
        simple_data['product_name'] = basic_info.get('main_title', '')
        simple_data['url'] = self.source if self.is_url else ''

        # Extract pricing information to root level
        pricing_info = nested_data.get('pricing_information', {})
        simple_data['original_price'] = pricing_info.get('original_price', 0)
        simple_data['current_price'] = pricing_info.get('sale_price', 0)
        simple_data['discount_percentage'] = pricing_info.get(
            'discount_percentage', '')
        simple_data['savings_amount'] = pricing_info.get('savings_amount', 0)

        # Extract product specifications to root level
        specs = nested_data.get('product_specifications', {})
        simple_data['fabric'] = specs.get('fabric', '')
        simple_data['fit'] = specs.get('fit', '')
        simple_data['closure'] = specs.get('closure', '')
        simple_data['collar'] = specs.get('collar', '')
        simple_data['sleeve'] = specs.get('sleeve', '')
        simple_data['pattern'] = specs.get('pattern', '')
        simple_data['occasion'] = specs.get('occasion', '')

        # Extract size availability as individual size fields
        size_info = nested_data.get('size_and_availability', {})
        size_availability = size_info.get('size_availability', {})

        # Add size availability fields for each standard size
        for size_code in ['XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL']:
            is_available = size_availability.get(size_code, False)
            simple_data[f'{size_code}_available'] = is_available

        # Extract image information to root level
        images_info = nested_data.get('product_images', {})
        simple_data['product_images'] = images_info.get('product_images', [])
        simple_data['main_image'] = images_info.get('main_image', '')

        logger.info("Successfully created simple JSON structure")
        return simple_data

    def scrape_all_data(self):
        """Scrape all product data and organize into simple structure"""
        logger.info("Starting product data extraction...")

        # Load and parse the HTML content from URL or file
        self.load_html()

        # Extract all data categories using existing extraction methods
        nested_data = {
            'basic_information': self.extract_basic_info(),
            'pricing_information': self.extract_pricing_info(),
            'product_specifications': self.extract_product_specifications(),
            'size_and_availability': self.extract_size_availability(),
            'product_images': self.extract_product_images()
        }

        # Convert nested structure to simple structure
        self.product_data = self.create_simple_structure(nested_data)

        logger.info("Product data extraction completed successfully")
        return self.product_data

    def save_to_json(self, filename=None):
        """Save extracted data to JSON file"""
        try:
            if not filename:
                # Generate a filename from the product URL or source
                if self.is_url:
                    # Extract product handle from URL path
                    url_parts = self.source.rstrip('/').split('/')
                    handle = url_parts[-1] if url_parts else 'product'
                else:
                    handle = 'product'

                timestamp = time.strftime('%Y%m%d_%H%M%S')
                filename = f"product_data_{timestamp}.json"

            # Determine where to save the JSON file
            if self.is_url:
                output_path = Path.cwd() / filename
            else:
                source_path = Path(self.source)
                output_path = source_path.parent / filename

            # Write the product data to a JSON file
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

        # Display basic product information
        print(f"🔹 Product Information:")
        print(f"   • Page Title: {self.product_data.get('page_title', 'N/A')}")
        print(
            f"   • Product Name: {self.product_data.get('product_name', 'N/A')}")
        print(f"   • URL: {self.product_data.get('url', 'N/A')}")

        # Display pricing information
        print(f"🔹 Pricing:")
        print(
            f"   • Original: ₹{self.product_data.get('original_price', 'N/A')}")
        print(
            f"   • Current: ₹{self.product_data.get('current_price', 'N/A')}")
        print(
            f"   • Discount: {self.product_data.get('discount_percentage', 'N/A')}")
        print(
            f"   • Savings: ₹{self.product_data.get('savings_amount', 'N/A')}")

        # Display product specifications
        print(f"🔹 Specifications:")
        spec_fields = ['fabric', 'fit', 'closure',
                       'collar', 'sleeve', 'pattern', 'occasion']
        for field in spec_fields:
            value = self.product_data.get(field, '')
            if value:
                print(f"   • {field.title()}: {value}")

        # Display size availability information
        print(f"🔹 Size & Availability:")
        size_fields = ['XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL']
        in_stock = [size for size in size_fields if self.product_data.get(
            f'{size}_available', False)]
        out_of_stock = [size for size in size_fields if f'{size}_available' in self.product_data and not self.product_data.get(
            f'{size}_available', False)]
        print(f"   • In Stock: {', '.join(in_stock) if in_stock else 'N/A'}")
        print(
            f"   • Out of Stock: {', '.join(out_of_stock) if out_of_stock else 'N/A'}")

        # Display image information
        product_images = self.product_data.get('product_images', [])
        print(f"🔹 Images: {len(product_images)} found")
        if self.product_data.get('main_image'):
            print(f"   • Main Image: {self.product_data.get('main_image')}")

        print("="*60)


def scrape_product_url(url, save_json=True):
    """
    Convenience function to scrape any thehouseofrare.com product URL

    Args:
        url (str): Product URL from thehouseofrare.com
        save_json (bool): Whether to save results to JSON

    Returns:
        dict: Extracted product data in simple structure
    """
    try:
        scraper = ProductScraper(url)
        product_data = scraper.scrape_all_data()

        if save_json:
            output_file = scraper.save_to_json()
            logger.info(f"Data saved to: {output_file}")

        return product_data

    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return {}


def scrape_multiple_urls(urls, delay=1.0, save_individual=False, save_combined=True):
    """
    Scrape multiple product URLs with rate limiting

    Args:
        urls (list): List of product URLs
        delay (float): Delay between requests in seconds
        save_individual (bool): Save each product to separate JSON
        save_combined (bool): Save all products to one JSON file

    Returns:
        list: List of extracted product data
    """
    results = []

    logger.info(f"Starting batch scrape of {len(urls)} URLs")

    for i, url in enumerate(urls):
        try:
            scraper = ProductScraper(url)
            product_data = scraper.scrape_all_data()
            results.append(product_data)

            if save_individual:
                scraper.save_to_json()

            logger.info(f"Scraped {i+1}/{len(urls)}: {url}")

            # Rate limiting
            if i < len(urls) - 1:  # Don't sleep after last item
                time.sleep(delay)

        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            results.append({})  # Add empty dict to maintain list order

    if save_combined:
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f"batch_scrape_results_{timestamp}.json"

        output_path = Path("scraped_data")
        output_path.mkdir(exist_ok=True)

        with open(output_path / filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved combined results to: {output_path / filename}")

    return results


def main():
    """Main function with URL automation"""
    # Test with URL
    test_url = "https://thehouseofrare.com/products/breath-rust"

    try:
        print("🚀 Testing simple URL scraping automation...")
        scraper = ProductScraper(test_url)
        product_data = scraper.scrape_all_data()
        output_file = scraper.save_to_json()
        scraper.print_summary()
        print(f"\n✅ Success! Data saved to: {output_file}")

    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
