#!/usr/bin/env python3
"""
Simple Product Scraping Automation Examples (FIXED VERSION)
============================================================
This file shows examples of how to use the simple scraping tools
No AI or LLM functionality - just pattern-based scraping

Author: GitHub Copilot
"""

import sys
import os
from pathlib import Path

print("🔍 Simple Product Scraping Automation Examples")
print("=" * 50)

# Example 1: Individual Product Scraping
print("\n📦 Example 1: Simple Single Product Scraping")
try:
    from product_scraper_simple import scrape_product_url

    # Test URL from thehouseofrare.com
    test_url = "https://thehouseofrare.com/products/paintt-green"

    print(f"📦 Scraping: {test_url}")

    # Simple scraping without AI
    data = scrape_product_url(test_url, save_json=True)

    if data.get('product_name'):
        print(f"✅ Success: {data['product_name']}")
        print(f"💰 Price: ₹{data.get('current_price', 'Not found')}")
        print(f"📁 Saved to JSON file")
    else:
        print("⚠️ No data extracted")

except ImportError as e:
    print(f"⚠️ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

# Example 2: Simple Sitemap Extraction
print("\n🗺️ Example 2: Simple Sitemap Extraction")
try:
    from sitemap_extractor import SitemapExtractor

    sitemap_url = "https://thehouseofrare.com/sitemap.xml"
    print(f"🌐 Processing sitemap: {sitemap_url}")

    extractor = SitemapExtractor(sitemap_url)
    extractor.load_sitemap()

    # Extract product URLs (limit to first 5 for demo)
    products = extractor.extract_product_urls()
    products = products[:5]  # Limit for demo

    print(f"✅ Found {len(products)} product URLs (showing first 5)")
    if products:
        print(f"📄 Sample: {products[0]['product_name']}")
        print(f"🔗 URL: {products[0]['url']}")

except ImportError as e:
    print(f"⚠️ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

# Example 3: Simple Bulk Scraping
print("\n📦 Example 3: Simple Bulk Scraping")
try:
    from product_scraper_simple import scrape_multiple_urls
    from sitemap_extractor import SitemapExtractor

    # Simple workflow without AI
    sitemap_url = "https://thehouseofrare.com/sitemap.xml"

    print(f"Step 1: Extracting URLs from {sitemap_url}")
    extractor = SitemapExtractor(sitemap_url)
    extractor.load_sitemap()
    products = extractor.extract_product_urls()

    if products:
        # Limit to 3 products for demo
        urls = [p['url'] for p in products[:3]]
        print(f"Step 2: Simple scraping of {len(urls)} products")

        # Use simple pattern-based scraping
        results = scrape_multiple_urls(
            urls,
            delay=1.0,  # Rate limiting
            save_combined=True
        )

        successful = len([r for r in results if r.get('product_name')])
        print(f"✅ Successfully scraped {successful}/{len(results)} products")

        # Show sample results
        if results and results[0].get('product_name'):
            sample = results[0]
            print(f"📄 Sample Result: {sample['product_name']}")
            print(f"💰 Price: ₹{sample.get('current_price', 'N/A')}")
    else:
        print("⚠️ No URLs extracted from sitemap")

except ImportError as e:
    print(f"⚠️ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

# Example 4: Fast Bulk Scraper (using simple scraper)
print("\n⚡ Example 4: Fast Bulk Scraper")
try:
    from product_scraper_simple import scrape_multiple_urls
    from sitemap_extractor import SitemapExtractor

    # Fast bulk scraping from sitemap using simple scraper
    sitemap_url = "https://thehouseofrare.com/sitemap.xml"

    print(f"🚀 Fast bulk scraping from: {sitemap_url}")

    # Extract URLs using sitemap extractor
    extractor = SitemapExtractor(sitemap_url)
    extractor.load_sitemap()
    products = extractor.extract_product_urls()

    # Limit to 5 for demo
    urls = [p['url'] for p in products[:5]]

    # Process with the simple scraper's bulk functionality
    results = scrape_multiple_urls(
        urls,
        delay=1.0,
        save_combined=True
    )

    print(f"✅ Bulk scraping completed!")
    print(
        f"📊 Successfully scraped: {len([r for r in results if r.get('product_name')])} products")
    print(f"📁 Data saved to scraped_data/ directory")

except ImportError as e:
    print(f"⚠️ Bulk scraper not available: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

# Summary
print("\n🎯 Simple Scraping Features Summary:")
print("=" * 40)
print("✅ Basic Pattern-Based Scraping - No AI needed")
print("✅ Sitemap URL Extraction - Standard pattern matching")
print("✅ Bulk Processing - Fast and efficient")
print("✅ Rate Limiting - Respectful scraping")
print("✅ JSON Export - Simple data format")
print("✅ Error Handling - Robust operation")

print("\n📚 Ready for simple scraping!")
print("No API keys or complex setup required")
print("Works with standard HTML pattern matching")

print("\n📁 Output Files:")
print("- Individual product JSON files")
print("- Combined batch results in scraped_data/")
print("- Simple data structure (no nested objects)")

if __name__ == "__main__":
    print("\n🚀 Automation examples completed!")
