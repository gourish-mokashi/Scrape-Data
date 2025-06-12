#!/usr/bin/env python3
"""
Universal Sitemap URL Extractor
===============================
Extracts product URLs from XML sitemap files from ANY website.

This module now supports any e-commerce website's sitemap structure.
It intelligently detects product URLs using multiple strategies.

Features:
- Universal sitemap support for any website
- Intelligent product URL detection
- Multiple sitemap format support (standard XML, sitemap index, etc.)
- Automatic domain validation and URL normalization
- Flexible filtering and pattern matching

Author: GitHub Copilot
"""

import requests
import xml.etree.ElementTree as ET
import re
import logging
from urllib.parse import urljoin, urlparse

# Setting up the logging system
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SitemapExtractor:
    """Extract product URLs from XML sitemaps universally"""

    def __init__(self, sitemap_url):
        """
        Initialize sitemap extractor for any website

        Args:
            sitemap_url (str): URL of the sitemap XML file
        """
        self.sitemap_url = sitemap_url

        # Extract and store the base domain from the sitemap URL
        parsed_url = urlparse(sitemap_url)
        self.base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.domain_name = parsed_url.netloc.lower()

        # Initialize containers
        self.sitemap_content = None
        self.product_urls = []
        self.all_urls = []

        # Common product URL patterns for different e-commerce platforms
        self.common_product_patterns = [
            r'/products?/',      # Shopify, many custom sites
            r'/product/',        # WooCommerce, Magento
            r'/item/',          # eBay, some custom sites
            r'/p/',             # Some minimalist sites
            r'/shop/',          # Shop pages
            r'/buy/',           # Purchase pages
            r'/store/',         # Store pages
            r'/catalog/',       # Catalog pages
            r'-p-\d+',          # Product with ID pattern
            r'/\d+\.html',      # Numeric product pages
        ]

    def load_sitemap(self):
        """Load sitemap content from URL"""
        try:
            logger.info(f"Fetching sitemap from URL: {self.sitemap_url}")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(
                self.sitemap_url, headers=headers, timeout=30)
            response.raise_for_status()
            self.sitemap_content = response.text

            logger.info("Successfully fetched sitemap XML content")

            # Check if this is a sitemap index or regular sitemap
            if self._is_sitemap_index():
                logger.info(
                    "Detected sitemap index file - contains links to other sitemaps")
                self._process_sitemap_index()
            else:
                self._parse_sitemap()

        except Exception as e:
            logger.error(f"Error loading sitemap: {e}")
            raise

    def _is_sitemap_index(self):
        """Check if this is a sitemap index file"""
        try:
            root = ET.fromstring(self.sitemap_content)
            return root.tag.endswith('sitemapindex') or any(child.tag.endswith('sitemap') for child in root)
        except:
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
        Extract product URLs from loaded sitemap using universal detection

        What: This extracts product URLs from any website's sitemap using intelligent detection
        Why: We want to support any e-commerce website, not just specific ones like houseofrare.com
        How: We delegate to the universal extraction method which uses multiple detection strategies

        Args:
            url_pattern (str): Optional regex pattern to filter URLs

        Returns:
            list: List of product URL dictionaries with 'url', 'product_name', and 'domain'
        """
        logger.info("Using universal product URL extraction for any website")

        if not self.all_urls:
            logger.warning("No URLs loaded yet. Call load_sitemap() first.")
            return []

        # Use the universal extraction method
        return self.extract_universal_product_urls(url_pattern=url_pattern)

    def get_product_urls_list(self):
        """
        Get simple list of product URLs

        Returns:
            list: List of URL strings
        """
        return [item['url'] for item in self.product_urls]

    def detect_product_url_patterns(self, sample_size=100):
        """
        Intelligently detect product URL patterns from the sitemap

        What: This analyzes URLs in the sitemap to identify product page patterns
        Why: Different websites use different URL structures for product pages
        How: We examine URL patterns and identify the most common product URL structure

        Args:
            sample_size (int): Number of URLs to analyze for pattern detection

        Returns:
            list: Detected product URL patterns
        """
        if not self.all_urls:
            logger.warning("No URLs loaded yet. Call load_sitemap() first.")
            return []

        # Sample URLs for pattern analysis
        sample_urls = self.all_urls[:sample_size]
        detected_patterns = []

        # Count pattern occurrences
        pattern_counts = {}
        for pattern in self.common_product_patterns:
            count = sum(1 for url in sample_urls if re.search(
                pattern, url, re.IGNORECASE))
            if count > 0:
                pattern_counts[pattern] = count

        # Sort by frequency and select most common patterns
        sorted_patterns = sorted(
            pattern_counts.items(), key=lambda x: x[1], reverse=True)

        # Take patterns that appear in at least 5% of URLs
        threshold = max(1, sample_size * 0.05)
        detected_patterns = [pattern for pattern,
                             count in sorted_patterns if count >= threshold]

        logger.info(f"Detected {len(detected_patterns)} product URL patterns")
        for pattern, count in sorted_patterns[:3]:
            logger.info(f"  Pattern '{pattern}': {count} matches")

        return detected_patterns

    def extract_universal_product_urls(self, custom_patterns=None, url_pattern=None):
        """
        Universal product URL extraction for any website

        What: This extracts product URLs from any website's sitemap using intelligent detection
        Why: We want to support any e-commerce website, not just specific ones
        How: We use multiple strategies to identify product URLs across different platforms

        Args:
            custom_patterns (list): Custom regex patterns specific to the website
            url_pattern (str): Additional filter pattern

        Returns:
            list: List of dictionaries containing product URL data
        """
        if not self.all_urls:
            logger.warning("No URLs loaded yet. Call load_sitemap() first.")
            return []

        product_urls = []

        # Use custom patterns if provided, otherwise detect automatically
        if custom_patterns:
            patterns_to_use = custom_patterns
            logger.info(
                f"Using {len(custom_patterns)} custom product patterns")
        else:
            patterns_to_use = self.detect_product_url_patterns()
            if not patterns_to_use:
                # Fallback to all common patterns if detection fails
                patterns_to_use = self.common_product_patterns
                logger.info("Using fallback common product patterns")

        logger.info(f"Scanning {len(self.all_urls)} URLs for products...")

        for url in self.all_urls:
            # Skip non-HTTP URLs
            if not url.startswith(('http://', 'https://')):
                continue

            # Validate URL belongs to the same domain
            if not self._is_valid_domain_url(url):
                continue

            # Check if URL matches any product pattern
            is_product_url = False
            for pattern in patterns_to_use:
                if re.search(pattern, url, re.IGNORECASE):
                    is_product_url = True
                    break

            # Additional filtering if pattern provided
            if url_pattern and not re.search(url_pattern, url, re.IGNORECASE):
                continue

            if is_product_url:
                # Extract product identifier from URL
                product_name = self._extract_product_name(url)

                product_data = {
                    'url': url,
                    'product_name': product_name,
                    'domain': self.domain_name
                }

                product_urls.append(product_data)

        logger.info(f"Successfully extracted {len(product_urls)} product URLs")
        self.product_urls = product_urls
        return product_urls

    def _is_valid_domain_url(self, url):
        """Check if URL belongs to the same domain as the sitemap"""
        try:
            parsed_url = urlparse(url)
            return parsed_url.netloc.lower() == self.domain_name
        except:
            return False

    def _extract_product_name(self, url):
        """Extract product name/identifier from URL"""
        try:
            # Remove domain and clean up
            path = urlparse(url).path

            # Common product name extraction strategies
            strategies = [
                # Shopify style
                lambda p: p.split('/products/')[-1].split('?')[0],
                # WooCommerce style
                lambda p: p.split('/product/')[-1].split('?')[0],
                lambda p: p.split(
                    '/item/')[-1].split('?')[0],      # Item style
                # Short style
                lambda p: p.split('/p/')[-1].split('?')[0],
                # Last segment
                lambda p: p.split('/')[-1].split('?')[0],
            ]

            for strategy in strategies:
                try:
                    name = strategy(path)
                    if name and name != path and len(name) > 0:
                        # Clean up the name
                        name = name.replace('-', ' ').replace('_', ' ').strip()
                        return name[:50]  # Limit length
                except:
                    continue

            return 'unknown'
        except:
            return 'unknown'


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
    print("🧪 Testing Universal Sitemap Extractor")
    print("=" * 50)

    try:
        # Test with different websites
        test_sites = [
            "https://thehouseofrare.com/sitemap.xml",
            "https://example-shop.com/sitemap.xml"  # Can be changed to any site
        ]

        for sitemap_url in test_sites[:1]:  # Test first one
            print(f"\n🔍 Testing: {sitemap_url}")

            extractor = SitemapExtractor(sitemap_url)
            extractor.load_sitemap()
            products = extractor.extract_product_urls()

            print(f"✅ Successfully extracted {len(products)} product URLs")

            # Show first few URLs
            for i, product in enumerate(products[:5]):
                print(f"{i+1}. {product['product_name']}: {product['url']}")

            if len(products) > 5:
                print(f"... and {len(products) - 5} more")

    except Exception as e:
        print(f"❌ Error: {e}")
