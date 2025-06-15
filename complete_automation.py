#!/usr/bin/env python3
"""
Complete Automation Script for thehouseofrare.com
Run this script to execute the complete automation process:
1. Extract product URLs from sitemap
2. Scrape product data from URLs
"""

import os
import subprocess
import sys
import time


def run_command(command, description):
    """Run a command and display progress"""
    print(f"\n🔄 {description}")
    print("=" * 60)

    try:
        result = subprocess.run(command, shell=True,
                                capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {str(e)}")
        return False


def main():
    """Run the complete automation process"""

    print("🚀 COMPLETE AUTOMATION FOR THEHOUSEOFRARE.COM")
    print("=" * 60)
    print("This script will:")
    print("1. Extract product URLs from sitemap.xml")
    print("2. Scrape detailed product data")
    print("3. Generate consolidated reports")
    print("=" * 60)

    # Step 1: Extract sitemap URLs
    print("\n📋 STEP 1: EXTRACTING PRODUCT URLS FROM SITEMAP")
    success1 = run_command("python run_automation.py",
                           "Sitemap URL extraction")

    if not success1:
        print("❌ Failed at Step 1. Exiting.")
        return

    # Step 2: Scrape product data
    print("\n🕷️ STEP 2: SCRAPING PRODUCT DATA")
    success2 = run_command("python bulk_web_scraper.py", "Bulk web scraping")

    if not success2:
        print("❌ Failed at Step 2. Exiting.")
        return

    # Final summary
    print("\n" + "=" * 60)
    print("🎉 COMPLETE AUTOMATION FINISHED!")
    print("=" * 60)

    # List generated files
    print("\n📄 Generated Files:")
    files = []
    for file in os.listdir('.'):
        if file.startswith('automation_results_') and file.endswith('.csv'):
            files.append(f"• {file} - Product URLs from sitemap")
        elif file.startswith('bulk_scraped_products_') and file.endswith('.json'):
            files.append(f"• {file} - Consolidated product data")

    for file in files:
        print(file)

    print("\n🎯 Summary:")
    print("• Sitemap extraction: ✅ Completed")
    print("• Product data scraping: ✅ Completed")
    print("• Data consolidation: ✅ Completed")
    print("\n🔧 Ready for production use!")


if __name__ == "__main__":
    main()
