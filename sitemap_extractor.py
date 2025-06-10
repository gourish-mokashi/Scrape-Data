#!/usr/bin/env python3
"""
Sitemap URL Extractor for thehouseofrare.com
===========================================
Extracts product URLs from XML sitemap files.

This module is essential for bulk_scraper.py to function properly.
It handles XML parsing and URL extraction from sitemaps.

Author: GitHub Copilot
"""

# Importing the requests module
# What: This brings in a library for making HTTP requests to websites
# Why: We need to download XML sitemap files from the internet
# How: We'll use requests.get() to fetch sitemap content from URLs
import requests

# Importing xml.etree.ElementTree as ET
# What: This brings in Python's built-in XML parsing and processing tools
# Why: Sitemaps are XML files, so we need tools to read and navigate XML structure
# How: We'll use ET.fromstring() to parse XML and find URL elements within it
import xml.etree.ElementTree as ET

# Importing the re module (regular expressions)
# What: This brings in Python's pattern matching and text searching tools
# Why: We need to filter URLs using patterns (like finding only shirt products)
# How: We'll use re.search() to check if URLs match specific patterns
import re

# Importing the logging module
# What: This brings in Python's system for recording what the program is doing
# Why: We need to track progress when processing large sitemaps with thousands of URLs
# How: We'll use logger.info() to show progress and logger.error() for problems
import logging

# Importing urljoin and urlparse from urllib.parse module
# What: This brings in URL manipulation and analysis tools
# Why: We need to combine URL parts and validate that URLs are properly formatted
# How: We'll use these to work with sitemap URLs and extract domain information
from urllib.parse import urljoin, urlparse

# Setting up the logging system
# What: This configures how Python will record information about what the program is doing
# Why: We want to track progress when downloading and processing sitemaps
# How: We set the level to INFO (shows progress messages) and define the message format
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Creating a logger object for this specific file
# What: This creates a logger that we can use throughout this file to record events
# Why: We want to track sitemap processing progress and any errors that occur
# How: logger.info() will record progress, logger.error() will record problems
logger = logging.getLogger(__name__)


# Creating a class called SitemapExtractor
# What: This defines a blueprint for objects that can extract URLs from XML sitemap files
# Why: We need an organized way to download, parse, and extract product URLs from sitemaps
# How: We create a class that contains all methods needed for sitemap processing
class SitemapExtractor:
    """Extract product URLs from XML sitemaps"""

    # The __init__ method is a special function that runs when we create a new SitemapExtractor
    # What: This sets up the initial state of our sitemap extractor object
    # Why: We need to store the sitemap URL and prepare variables for storing extracted data
    # How: We save the sitemap URL and initialize empty variables for content and URLs
    def __init__(self, sitemap_url):
        """
        Initialize sitemap extractor

        Args:
            sitemap_url (str): URL of the sitemap XML file
        """
        # Store the sitemap URL for later use
        # What: This saves the sitemap URL so we can download it when needed
        # Why: We need to remember which sitemap file we're working with
        # How: We assign the input parameter to self.sitemap_url to keep it available
        self.sitemap_url = sitemap_url
        
        # Initialize an empty variable to store the downloaded sitemap content
        # What: This creates a placeholder for the XML content we'll download from the URL
        # Why: We need somewhere to store the raw sitemap data after downloading it
        # How: We set it to None initially, will be filled when we download the sitemap
        self.sitemap_content = None
        
        # Initialize empty list to store extracted product URLs with their details
        # What: This creates a container for product URLs and their associated information
        # Why: We need to store the URLs we extract along with metadata like product names
        # How: We start with an empty list that we'll fill with dictionaries containing URL data
        self.product_urls = []
        
        # Initialize empty list to store all URLs found in the sitemap
        # What: This creates a container for every URL found in the sitemap file
        # Why: We need to store all URLs first, then filter for just the product ones
        # How: We start with an empty list that we'll fill with all discovered URLs
        self.all_urls = []    # Method to download and load sitemap content from the internet
    # What: This downloads the XML sitemap file from the web and processes it
    # Why: We need to get the sitemap content before we can extract URLs from it
    # How: We use requests to download the XML, then determine how to process it
    def load_sitemap(self):
        """Load sitemap content from URL"""
        # Use try-except to handle any errors that might occur during download
        # What: This wraps our code in error handling to catch network or parsing problems
        # Why: Internet downloads can fail, so we need to handle errors gracefully
        # How: If anything goes wrong, we'll log the error and stop execution safely
        try:
            # Log that we're starting to download the sitemap
            # What: This records that we're beginning the download process
            # Why: We want to track progress and see what the program is doing
            # How: We use logger.info() to write an informational message
            logger.info(f"Fetching sitemap from URL: {self.sitemap_url}")

            # Set up headers to make our request look like it's coming from a real browser
            # What: This creates HTTP headers that identify our program as a regular web browser
            # Why: Some websites block requests that don't look like they come from real browsers
            # How: We create a dictionary with a User-Agent string that mimics Chrome browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Download the sitemap content from the URL
            # What: This makes an HTTP request to download the XML sitemap file
            # Why: We need to get the sitemap content before we can extract URLs from it
            # How: We use requests.get() with headers and a 30-second timeout
            response = requests.get(
                self.sitemap_url, headers=headers, timeout=30)
            
            # Check if the download was successful (no 404 errors, etc.)
            # What: This verifies that the web server returned the content successfully
            # Why: If there was an error (like 404 not found), we need to know and stop
            # How: raise_for_status() will throw an error if the HTTP status indicates failure
            response.raise_for_status()

            # Store the downloaded XML content in our object
            # What: This saves the text content of the sitemap file for processing
            # Why: We need to keep the XML data available for parsing and URL extraction
            # How: We assign response.text to self.sitemap_content for later use
            self.sitemap_content = response.text
            
            # Log that the download was successful
            # What: This records that we successfully downloaded the sitemap content
            # Why: We want to track our progress and confirm the download worked
            # How: We use logger.info() to write a success message
            logger.info("Successfully fetched sitemap XML content")

            # Check if this sitemap file contains links to other sitemap files
            # What: This determines if we have a sitemap index (list of sitemaps) or actual URLs
            # Why: Large websites often have multiple sitemap files, so we need to handle both cases
            # How: We call a helper method that analyzes the XML structure
            if self._is_sitemap_index():
                # If it's a sitemap index, log this information
                # What: This records that we found a sitemap index file
                # Why: Users should know that we're processing a collection of sitemaps
                # How: We use logger.info() to write an informational message
                logger.info(
                    "Detected sitemap index file - contains links to other sitemaps")
                
                # Process the sitemap index to find product sitemaps
                # What: This extracts the URLs of individual sitemap files from the index
                # Why: We need to get the actual product sitemaps from the index file
                # How: We call a method that parses the index and downloads product sitemaps
                self._process_sitemap_index()
            else:
                # If it's a regular sitemap, parse it directly
                # What: This processes the XML to extract individual URLs
                # Why: This sitemap contains actual URLs, not links to other sitemaps
                # How: We call a method that parses the XML and extracts all URLs
                self._parse_sitemap()        # If any error occurs during the sitemap loading process, handle it
        # What: This catches any errors that happened during download or processing
        # Why: We need to log errors and re-raise them so the calling code knows something failed
        # How: We catch the exception, log what went wrong, then raise it again
        except Exception as e:
            # Log the error with details about what went wrong
            # What: This records the error message for debugging purposes
            # Why: We need to know what failed so we can fix problems
            # How: We use logger.error() to write an error message with the exception details
            logger.error(f"Error loading sitemap: {e}")
            
            # Re-raise the exception so the calling code knows there was a problem
            # What: This passes the error up to whatever code called this method
            # Why: The calling code needs to know that loading failed so it can handle it
            # How: We use 'raise' to re-throw the exception
            raise

    # Helper method to check if the sitemap is an index file (contains links to other sitemaps)
    # What: This analyzes the XML structure to determine if it's an index or regular sitemap
    # Why: Index files need different processing than regular sitemaps with actual URLs
    # How: We parse the XML and check for specific tag names that indicate an index
    def _is_sitemap_index(self):
        """Check if this is a sitemap index file"""
        # Use try-except to handle any XML parsing errors
        # What: This wraps the XML parsing in error handling
        # Why: If the XML is malformed, parsing could fail
        # How: If parsing fails, we'll assume it's not an index and return False
        try:
            # Parse the XML content to get the root element
            # What: This converts the XML text into a structure we can analyze
            # Why: We need to examine the XML tags to determine the file type
            # How: ET.fromstring() parses the XML and returns the root element
            root = ET.fromstring(self.sitemap_content)
            
            # Check if the root tag indicates this is a sitemap index
            # What: This examines the XML tag names to identify the file type
            # Why: Index files have different root tags than regular sitemaps
            # How: We check if the root tag ends with 'sitemapindex' or has 'sitemap' children
            return root.tag.endswith('sitemapindex') or any(child.tag.endswith('sitemap') for child in root)
        except:
            # If XML parsing fails, assume it's not an index file
            # What: This handles any errors in XML parsing by returning False
            # Why: If we can't parse the XML, it's safer to treat it as a regular sitemap
            # How: We simply return False without raising an error
            return False

    def _process_sitemap_index(self):
        """Process a sitemap index file to find product sitemaps"""
        try:
            root = ET.fromstring(self.sitemap_content)

            # Find all sitemap URLs
            sitemap_urls = []
            for sitemap in root:
                if sitemap.tag.endswith('sitemap'):
                    loc_elem = sitemap.find(
                        './/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                    if loc_elem is not None:
                        sitemap_urls.append(loc_elem.text)

            # Filter for product sitemaps
            product_sitemaps = [
                url for url in sitemap_urls if 'product' in url.lower()]

            if not product_sitemaps:
                # If no specific product sitemaps, take the first few sitemaps
                # Just take the first one for now
                product_sitemaps = sitemap_urls[:1]

            logger.info(
                f"Processing first product sitemap: {product_sitemaps[0]}")
            logger.info(
                f"Total product sitemaps available: {len(product_sitemaps)}")

            # Process the first product sitemap
            if product_sitemaps:
                self._load_and_parse_sitemap(product_sitemaps[0])

        except Exception as e:
            logger.error(f"Error processing sitemap index: {e}")
            raise

    def _load_and_parse_sitemap(self, sitemap_url):
        """Load and parse a specific sitemap"""
        try:
            logger.info(f"Fetching sitemap from URL: {sitemap_url}")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(sitemap_url, headers=headers, timeout=30)
            response.raise_for_status()

            content = response.text
            logger.info("Successfully fetched sitemap XML content")

            # Parse this sitemap
            self._parse_sitemap(content)

        except Exception as e:
            logger.error(f"Error loading sitemap {sitemap_url}: {e}")
            raise

    def _parse_sitemap(self, content=None):
        """Parse sitemap XML content"""
        try:
            if content is None:
                content = self.sitemap_content

            root = ET.fromstring(content)

            # Parse URLs with namespaces
            urls = []
            for url_elem in root:
                if url_elem.tag.endswith('url'):
                    loc_elem = url_elem.find(
                        './/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                    if loc_elem is not None:
                        urls.append(loc_elem.text)

            self.all_urls = urls
            logger.info(f"Found {len(urls)} total URLs in sitemap")

        except Exception as e:
            logger.error(f"Error parsing sitemap XML: {e}")
            raise

    def extract_product_urls(self, url_pattern=None):
        """
        Extract product URLs from loaded sitemap

        Args:
            url_pattern (str): Optional regex pattern to filter URLs

        Returns:
            list: List of product URL dictionaries
        """
        if not self.all_urls:
            raise ValueError("No sitemap loaded. Call load_sitemap() first.")

        product_urls = []
        count = 0

        for url in self.all_urls:
            # Filter for product URLs
            if '/products/' in url:
                # Apply pattern filter if provided
                if url_pattern and not re.search(url_pattern, url):
                    continue

                # Extract product name from URL
                product_name = url.split(
                    '/products/')[-1] if '/products/' in url else 'unknown'

                product_data = {
                    'url': url,
                    'product_name': product_name
                }

                product_urls.append(product_data)
                count += 1

                # Progress indicator for large sitemaps
                if count % 100 == 0:
                    logger.info(f"Extracted {count} product URLs...")

        logger.info(f"Successfully extracted {len(product_urls)} product URLs")
        self.product_urls = product_urls

        if len(self.all_urls) > 1000:
            logger.info(
                f"Note: Only processed 1 of 6 available product sitemaps")

        return product_urls

    def get_product_urls_list(self):
        """
        Get simple list of product URLs

        Returns:
            list: List of URL strings
        """
        return [item['url'] for item in self.product_urls]


def extract_sitemap_urls(sitemap_url, url_pattern=None, max_urls=None):
    """
    Convenience function to extract URLs from sitemap

    Args:
        sitemap_url (str): Sitemap URL
        url_pattern (str): Optional regex pattern to filter URLs
        max_urls (int): Maximum number of URLs to return

    Returns:
        tuple: (list of URLs, None)  # Second value kept for compatibility
    """
    try:
        extractor = SitemapExtractor(sitemap_url)
        extractor.load_sitemap()
        url_data = extractor.extract_product_urls(url_pattern)

        # Extract just URLs
        urls = [item['url'] for item in url_data]

        # Limit if specified
        if max_urls and len(urls) > max_urls:
            urls = urls[:max_urls]

        return urls, None

    except Exception as e:
        logger.error(f"Error extracting sitemap URLs: {e}")
        raise


if __name__ == "__main__":
    # Test the extractor
    print("🧪 Testing Sitemap Extractor")
    print("=" * 40)

    try:
        sitemap_url = "https://thehouseofrare.com/sitemap.xml"

        extractor = SitemapExtractor(sitemap_url)
        extractor.load_sitemap()
        products = extractor.extract_product_urls()

        print(f"✅ Successfully extracted {len(products)} product URLs")

        # Show first few URLs
        for i, product in enumerate(products[:5]):
            print(f"{i+1}. {product['url']}")

        if len(products) > 5:
            print(f"... and {len(products) - 5} more")

    except Exception as e:
        print(f"❌ Error: {e}")
