# Product Scraping Automation Examples
# ===================================
# This file shows examples of how to use the scraping tools

# Example 1: Individual Product Scraping
# What: This shows how to scrape data from a single product page
# Why: Sometimes you only need information from one specific product
# How: Import the scrape_product_url function and pass it a product URL

"""
# Importing the individual product scraping function (flat structure version)
# What: This brings in the function that can scrape one product at a time with flat JSON output
# Why: We need this function to extract data from individual product pages in the new flat format
# How: We import scrape_product_url from our flat structure product_scraper_automated file
from product_scraper_automated_flat import scrape_product_url

# Scrape a single product by providing its URL
# What: This calls the scraping function with a specific product URL
# Why: We want to get detailed information about this particular product
# How: We pass the product URL to scrape_product_url() which returns a data dictionary
data = scrape_product_url("https://thehouseofrare.com/products/product-name")

# The 'data' variable now contains all the product information in a structured format
# You can access different parts like:
# - data['basic_information']['main_title'] for the product name
# - data['pricing_information']['sale_price'] for the current price
# - data['size_availability'] for size availability information
"""

# Example 2: Bulk Scraping from Sitemap (Currently Active)
# What: This shows how to scrape many products automatically from a sitemap
# Why: This is much faster than scraping products one by one manually
# How: Import the bulk scraping function and pass it a sitemap URL with limits

# Importing the bulk scraping function
# What: This brings in the function that can scrape hundreds of products at once
# Why: We need this function to efficiently collect data from many products
# How: We import fast_bulk_scrape from our bulk_scraper file
from bulk_scraper import fast_bulk_scrape

# Perform bulk scraping from a sitemap URL
# What: This automatically extracts URLs from a sitemap and scrapes each product
# Why: We want to collect data from multiple products efficiently
# How: We call fast_bulk_scrape() with the sitemap URL and set a limit of 10 products
report = fast_bulk_scrape(
    "https://thehouseofrare.com/sitemap_products_2.xml?from=6811711995975&to=7085628620871",
    max_products=10
)

# The 'report' variable now contains:
# - Information about how many products were successfully scraped
# - Timing statistics (how long it took)
# - File locations where the data was saved
# - Any errors that occurred during scraping

# After this runs, you'll find files like:
# - scraped_products/all_products.json (all data in JSON format)
# - scraped_products/all_products.csv (all data in spreadsheet format)
# - scraped_products/scraping_report.json (detailed statistics)
