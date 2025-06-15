#!/usr/bin/env python3
"""
Bulk Web Scraping using Extracted Product URLs
"""

import csv
import json
import time
from product_scraper_automated import scrape_product_url


def main():
    """Run bulk scraping on extracted product URLs"""

    print("🕷️ BULK WEB SCRAPING - USING EXTRACTED PRODUCT LINKS")
    print("=" * 60)    # Read the extracted product URLs from automation results
    csv_file = "automation_results_1749986026.csv"
    product_urls = []

    print(f"📄 Reading product URLs from: {csv_file}")

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i < 25:  # Limit to first 25 products
                    product_urls.append(row['Product URL'])
                else:
                    break
    except FileNotFoundError:
        print(f"❌ Error: {csv_file} not found!")
        return

    print(f"🎯 Selected {len(product_urls)} products for scraping")
    print("🔄 Starting bulk web scraping...")
    print("⏳ This will take a few minutes (respectful delays included)")

    scraped_products = []
    failed_products = []
    start_time = time.time()

    for i, url in enumerate(product_urls, 1):
        # Extract product name from URL for display
        product_slug = url.split('/')[-1]
        display_name = product_slug.replace('-', ' ').title()

        print(f"\n[{i:2d}/{len(product_urls)}] Scraping: {display_name}")
        print(f"    🔗 URL: {url}")

        try:
            # Use the existing product scraper
            product_data = scrape_product_url(url, save_json=True)

            if product_data and product_data.get('product_name'):
                scraped_products.append(product_data)

                # Display extracted data
                name = product_data.get('product_name', 'Unknown')
                price = product_data.get('current_price', 'N/A')
                availability = product_data.get('availability', 'N/A')

                print(f"    ✅ SUCCESS: {name}")
                print(f"       💰 Price: ₹{price}")
                print(f"       📦 Status: {availability}")

            else:
                failed_products.append(url)
                print(f"    ⚠️  NO DATA: Could not extract product information")

        except Exception as e:
            failed_products.append(url)
            print(f"    ❌ ERROR: {str(e)[:60]}...")

        # Respectful delay between requests
        if i < len(product_urls):
            print(f"    ⏳ Waiting 2 seconds before next request...")
            time.sleep(2)

    end_time = time.time()
    total_time = end_time - start_time

    # Display final results
    print(f"\n" + "="*60)
    print(f"✅ BULK SCRAPING COMPLETED!")
    print(f"⏱️  Total processing time: {total_time:.2f} seconds")
    print(
        f"📊 Successful extractions: {len(scraped_products)}/{len(product_urls)} products")
    print(
        f"📈 Success rate: {(len(scraped_products)/len(product_urls))*100:.1f}%")
    print(
        f"⚡ Average time per product: {total_time/len(product_urls):.2f} seconds")

    # Save consolidated results to JSON
    if scraped_products:
        output_file = f"bulk_scraped_products_{int(time.time())}.json"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(scraped_products, f, indent=2, ensure_ascii=False)

            print(f"\n📄 Consolidated results saved to: {output_file}")

            # Display sample of scraped products
            print(f"\n🛍️  SCRAPED PRODUCTS SUMMARY:")
            print("-" * 40)

            for i, product in enumerate(scraped_products[:10], 1):
                name = product.get('product_name', 'N/A')
                price = product.get('current_price', 'N/A')
                print(f"{i:2d}. {name} - ₹{price}")

            if len(scraped_products) > 10:
                print(
                    f"    ... and {len(scraped_products) - 10} more products")

        except Exception as e:
            print(f"❌ Error saving consolidated results: {e}")

    # Show failed products if any
    if failed_products:
        print(f"\n⚠️  FAILED PRODUCTS ({len(failed_products)}):")
        for i, url in enumerate(failed_products[:5], 1):
            product_name = url.split('/')[-1].replace('-', ' ').title()
            print(f"   {i}. {product_name}")
        if len(failed_products) > 5:
            print(f"   ... and {len(failed_products) - 5} more")

    print(f"\n🎉 Bulk web scraping completed successfully!")

    return scraped_products


if __name__ == "__main__":
    results = main()
