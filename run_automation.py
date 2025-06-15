#!/usr/bin/env python3
"""
Automation Runner for Sitemap Processing
"""

from sitemap_extractor import SitemapExtractor
import time
import csv


def run_automation(sitemap_url):
    """Run the complete automation workflow"""

    print(f"🗂️ Running Sitemap Automation")
    print("=" * 50)
    print(f"🔗 Target URL: {sitemap_url}")
    print("⏳ Processing...")

    start_time = time.time()

    try:
        # Create extractor and load sitemap
        extractor = SitemapExtractor(sitemap_url)
        extractor.load_sitemap()

        # Extract product URLs
        product_urls = extractor.extract_product_urls()

        end_time = time.time()
        processing_time = end_time - start_time

        # Display results
        print(f"\n✅ EXTRACTION COMPLETED!")
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")
        print(f"📊 Found {len(product_urls)} product URLs")

        if product_urls:
            print(f"\n🔗 Sample Product URLs (first 10):")
            for i, url_data in enumerate(product_urls[:10], 1):
                url = url_data.get('url', str(url_data))
                print(f"   {i:2d}. {url}")

            if len(product_urls) > 10:
                # Save to CSV - Only Product URLs
                print(f"   ... and {len(product_urls) - 10} more products")
            csv_filename = f"automation_results_{int(time.time())}.csv"
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Product URL'])

                for url_data in product_urls:
                    url = url_data.get('url', str(url_data))
                    writer.writerow([url])

            print(f"\n📄 Results saved to: {csv_filename}")

        else:
            print(f"\n⚠️  No product URLs found")

        return product_urls

    except Exception as e:
        print(f"\n❌ Error during automation: {e}")
        return []


if __name__ == "__main__":
    # Run automation on the specified URL
    sitemap_url = "https://thehouseofrare.com/sitemap.xml"
    results = run_automation(sitemap_url)

    print(f"\n🎉 Automation completed!")
    print(f"📚 Total URLs extracted: {len(results)}")
