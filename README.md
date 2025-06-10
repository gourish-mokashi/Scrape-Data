# 🕷️ Product Scraper for thehouseofrare.com

**Simple Python tool to get product information from thehouseofrare.com**

This tool helps you automatically collect product details like prices, sizes, images, and specifications from the thehouseofrare.com website. You can scrape one product at a time or hundreds of products in bulk.

## ✨ What This Tool Can Do

- 🔗 **Single Product Scraping**: Get details from one product page
- 📋 **Bulk Scraping**: Automatically scrape hundreds of products from sitemaps
- ⚡ **Fast Processing**: Takes only 1-2 seconds per product
- 📊 **Multiple Formats**: Saves data as JSON and CSV files
- 🧹 **Auto Cleanup**: Removes temporary files automatically
- 🛡️ **Safe Scraping**: Built-in delays to be respectful to the website

## 💻 What You Need

- Python 3.6 or newer
- Internet connection
- Two Python packages: `requests` and `beautifulsoup4`

### Install Required Packages

```bash
pip install requests beautifulsoup4
```

That's it! Now you're ready to use the scraper.

## 📦 What Information Does It Collect?

The scraper gets these details from each product:

### 🏷️ Basic Info

- Product name (like "WATERCOLOUR EFFECT FLORAL PRINT SHIRT")
- Product page title
- Direct link to the product page

### 💰 Price Details

- Original price (before discount)
- Sale price (current price)
- How much discount percentage (like "60% off")
- Money saved amount

### 👔 Product Details

- **Fabric**: Cotton, Polyester, etc.
- **Fit**: Regular, Slim, Oversized
- **Closure**: Button, Zipper
- **Collar**: Spread, Classic, etc.
- **Sleeve**: Full sleeve, Half sleeve
- **Pattern**: Solid, Striped, Floral, etc.
- **Occasion**: Casual, Formal, Party

### 📏 Size Information

- Which sizes are available (XS, S, M, L, XL, XXL, 3XL)
- Which sizes are in stock vs out of stock
- Real-time availability status

### 📸 Images

- Main product image
- All additional product images
- Direct links to high-quality images

## 🚀 How to Use This Tool

There are two main ways to use this scraper:

### 🎯 Method 1: Single Product Scraping

**When to use**: When you want details from just one product

**How it works**: Give the tool a product URL, and it will get all the information from that page.

#### Python Code Example:

```python
from product_scraper_automated import scrape_product_url

# Scrape one product
url = "https://thehouseofrare.com/products/breath-rust"
product_data = scrape_product_url(url)

# Print the product name and price
print(f"Product: {product_data['basic_information']['main_title']}")
print(f"Price: ₹{product_data['pricing_information']['sale_price']}")
```

#### What happens:

1. The tool visits the product page
2. Waits for all content to load (including JavaScript)
3. Extracts all product information
4. Saves it as a JSON file
5. Returns the data to your program

### ⚡ Method 2: Bulk Scraping (Recommended for Multiple Products)

**When to use**: When you want to scrape many products automatically

**How it works**: The tool gets a list of all products from the website's sitemap, then scrapes them one by one.

#### Python Code Example:

```python
from bulk_scraper import fast_bulk_scrape

# Scrape 10 products automatically
report = fast_bulk_scrape(
    sitemap_url="https://thehouseofrare.com/sitemap.xml",
    max_products=10,
    output_dir="my_scraped_products"
)

# Check the results
print(f"Successfully scraped: {report['scraping_summary']['successful_scrapes']} products")
print(f"Success rate: {report['scraping_summary']['success_rate']}")
print(f"Average time per product: {report['scraping_summary']['average_time_per_product']}")
```

#### What happens:

1. Gets list of all products from thehouseofrare.com sitemap
2. Scrapes each product (1-2 seconds per product)
3. Saves individual JSON files temporarily
4. Creates combined files: `all_products.json` and `all_products.csv`
5. Deletes individual files to keep things clean
6. Shows you a detailed report

## 💡 Simple Examples for Beginners

### Example 1: Get Basic Product Info

```python
from product_scraper_automated import scrape_product_url

# Scrape a shirt
product = scrape_product_url("https://thehouseofrare.com/products/paintt-green")

# Print basic information
print("=== Product Information ===")
print(f"Name: {product['basic_information']['main_title']}")
print(f"Original Price: ₹{product['pricing_information']['original_price']}")
print(f"Sale Price: ₹{product['pricing_information']['sale_price']}")
print(f"Discount: {product['pricing_information']['discount_percentage']}")
print(f"Fabric: {product['product_specifications']['fabric']}")
```

### Example 2: Check Size Availability

```python
from product_scraper_automated import scrape_product_url

product = scrape_product_url("https://thehouseofrare.com/products/breath-rust")

print("=== Size Availability ===")
sizes = product['size_availability']
for size, available in sizes.items():
    status = "✅ Available" if available else "❌ Out of Stock"
    print(f"{size}: {status}")
```

### Example 3: Download Product Images

```python
from product_scraper_automated import scrape_product_url
import requests

product = scrape_product_url("https://thehouseofrare.com/products/luxur-blue")

print("=== Product Images ===")
images = product['product_images']['product_images']
print(f"Total images: {len(images)}")

# Download first image (optional)
if images:
    main_image_url = images[0]
    response = requests.get(main_image_url)
    with open("product_image.jpg", "wb") as f:
        f.write(response.content)
    print("Downloaded main image as 'product_image.jpg'")
```

### Example 4: Bulk Scrape with Custom Settings

```python
from bulk_scraper import FastBulkScraper

# Create a scraper instance
scraper = FastBulkScraper("https://thehouseofrare.com/sitemap.xml")

# Get only 5 products for testing
scraper.extract_product_urls(max_urls=5)

# Scrape them and save to custom folder
report = scraper.fast_scrape_products(output_dir="test_scraping")

print("=== Scraping Complete ===")
print(f"Total products: {report['scraping_summary']['total_urls']}")
print(f"Successful: {report['scraping_summary']['successful_scrapes']}")
print(f"Failed: {report['scraping_summary']['failed_scrapes']}")
```

## 📁 Project Files Explained

This project has 4 main files:

- **`product_scraper_automated.py`** - The main scraper that gets product information
- **`bulk_scraper.py`** - Tool for scraping many products at once
- **`sitemap_extractor.py`** - Helper that finds all product URLs from the website
- **`README.md`** - This instruction file

You mainly use the first two files. The others help them work.

## 📊 What Files Does It Create?

After scraping, you'll get these files:

### For Single Products:

```
product_data_20250610_143022.json  # Contains all product information
```

### For Bulk Scraping:

```
my_output_folder/
├── all_products.json              # All products in one JSON file
├── all_products.csv               # All products in Excel-friendly format
├── scraping_report.json           # Statistics and summary
└── (individual files automatically deleted)
```

## 🔍 Understanding the Output Data

When you scrape a product, you get a JSON file that looks like this:

```json
{
  "basic_information": {
    "page_title": "Rare Rabbit Men's Paintt Green Cotton Fabric Floral Print Full Sleeves",
    "main_title": "WATERCOLOUR EFFECT FLORAL PRINT SHIRT",
    "url": "https://thehouseofrare.com/products/paintt-green"
  },
  "pricing_information": {
    "original_price": 4199,
    "sale_price": 1679,
    "discount_percentage": "60%",
    "savings_amount": 2520
  },
  "product_specifications": {
    "fabric": "COTTON",
    "fit": "REGULAR",
    "closure": "BUTTON",
    "collar": "SPREAD COLLAR",
    "sleeve": "FULL SLEEVE",
    "pattern": "FLORAL PRINT",
    "occasion": "CASUAL"
  },
  "size_availability": {
    "XS-36": true,
    "S-38": true,
    "M-40": false,
    "L-42": true,
    "XL-44": true,
    "XXL-46": false,
    "3XL-48": false
  },
  "product_images": {
    "product_images": [
      "https://thehouseofrare.com/cdn/shop/products/IMG_0006_1.jpg",
      "https://thehouseofrare.com/cdn/shop/products/IMG_0005_1.jpg"
    ],
    "main_image": "https://thehouseofrare.com/cdn/shop/products/IMG_0006_1.jpg"
  }
}
```

### Understanding Each Section:

- **basic_information**: Product name, page title, and direct URL
- **pricing_information**: All price details including discounts
- **product_specifications**: Fabric, fit, style details
- **size_availability**: `true` = available, `false` = out of stock
- **product_images**: Links to all product photos

## 📈 CSV Output Format

The CSV file has these columns (great for Excel):

| Column               | Example                                          | Description           |
| -------------------- | ------------------------------------------------ | --------------------- |
| product_name         | WATERCOLOUR EFFECT FLORAL PRINT SHIRT            | Product name          |
| url                  | https://thehouseofrare.com/products/paintt-green | Direct link           |
| original_price       | 4199                                             | Price before discount |
| sale_price           | 1679                                             | Current selling price |
| discount_percentage  | 60%                                              | How much discount     |
| savings_amount       | 2520                                             | Money saved           |
| fabric               | COTTON                                           | Material type         |
| fit                  | REGULAR                                          | Fit style             |
| closure              | BUTTON                                           | How it closes         |
| collar               | SPREAD COLLAR                                    | Collar type           |
| sleeve               | FULL SLEEVE                                      | Sleeve length         |
| pattern              | FLORAL PRINT                                     | Design pattern        |
| occasion             | CASUAL                                           | When to wear          |
| main_image           | https://...                                      | Main product image    |
| product_images_count | 9                                                | How many images       |

## ⚙️ How the Tool Works (Technical Details)

### Speed and Performance

- **Fast**: Takes only 1-2 seconds per product
- **Respectful**: Waits 0.8 seconds between requests to not overload the website
- **Reliable**: Automatically retries if something fails
- **Smart**: Waits for JavaScript content to load completely

### Safety Features

- Only works with thehouseofrare.com (won't scrape other websites)
- Uses realistic browser headers to look like a normal visitor
- Has timeout protection (won't wait forever)
- Handles errors gracefully and continues with other products

### What Makes It Smart

- **Dynamic Content**: Waits for price, size, and image information to load
- **Auto Cleanup**: Removes temporary files after creating combined files
- **Progress Tracking**: Shows you exactly what's happening while it works
- **Error Handling**: If one product fails, it continues with the others

## 🚨 Important Rules and Tips

### ✅ What You Should Do

- Use reasonable delays between requests (the tool does this automatically)
- Check that product URLs are correct before scraping
- Start with small numbers (like 5-10 products) to test
- Make sure you have good internet connection

### ❌ What You Should NOT Do

- Don't set delays too low (respect the website)
- Don't try to scrape other websites (it won't work anyway)
- Don't run multiple scrapers at the same time
- Don't scrape thousands of products in one go without testing first

### 🔧 If Something Goes Wrong

**Problem**: "No module named 'requests'"
**Solution**: Install the packages with `pip install requests beautifulsoup4`

**Problem**: "Domain validation error"
**Solution**: Make sure your URL starts with https://thehouseofrare.com/

**Problem**: "Network timeout"
**Solution**: Check your internet connection and try again

**Problem**: Product information is missing
**Solution**: Some products might not have complete information - this is normal

**Problem**: Scraping is too slow
**Solution**: This is normal! The tool waits between requests to be respectful

## 📚 Real-World Usage Examples

### Example 1: Market Research

```python
# Get pricing information for similar products
from bulk_scraper import fast_bulk_scrape

# Scrape 50 shirts to analyze pricing
report = fast_bulk_scrape(
    sitemap_url="https://thehouseofrare.com/sitemap.xml",
    max_products=50,
    output_dir="market_research"
)

print(f"Collected pricing data for {report['scraping_summary']['successful_scrapes']} products")
```

### Example 2: Inventory Tracking

```python
# Check size availability for specific products
from product_scraper_automated import scrape_product_url

products_to_check = [
    "https://thehouseofrare.com/products/breath-rust",
    "https://thehouseofrare.com/products/paintt-green",
    "https://thehouseofrare.com/products/luxur-blue"
]

for url in products_to_check:
    product = scrape_product_url(url)
    name = product['basic_information']['main_title']
    sizes = product['size_availability']

    available_sizes = [size for size, available in sizes.items() if available]
    print(f"{name}: Available in {len(available_sizes)} sizes")
```

### Example 3: Price Monitoring

```python
# Monitor prices of specific products
import json
from datetime import datetime
from product_scraper_automated import scrape_product_url

# List of products to monitor
urls = [
    "https://thehouseofrare.com/products/breath-rust",
    "https://thehouseofrare.com/products/paintt-green"
]

price_data = []

for url in urls:
    product = scrape_product_url(url)

    price_info = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'product': product['basic_information']['main_title'],
        'url': url,
        'original_price': product['pricing_information']['original_price'],
        'sale_price': product['pricing_information']['sale_price'],
        'discount': product['pricing_information']['discount_percentage']
    }

    price_data.append(price_info)

# Save price monitoring data
with open('price_history.json', 'w') as f:
    json.dump(price_data, f, indent=2)

print(f"Monitored prices for {len(price_data)} products")
```

## 🎓 Learning More

### For Beginners

1. Start by scraping just one product to see how it works
2. Try the bulk scraper with 5 products
3. Look at the JSON output to understand the data structure
4. Experiment with the CSV file in Excel or Google Sheets

### For Advanced Users

- Modify the delay settings in `bulk_scraper.py` if needed
- Add custom filtering logic in `sitemap_extractor.py`
- Extend the data extraction in `product_scraper_automated.py`
- Create your own analysis scripts using the output data

### Useful Resources

- **JSON Format**: Learn about JSON at https://www.json.org/
- **Python Basics**: If you're new to Python, try https://python.org/
- **CSV Files**: Open CSV files in Excel, Google Sheets, or any spreadsheet software

## 📊 Performance Statistics

Based on real testing:

- **Average speed**: 1.4-1.8 seconds per product
- **Success rate**: 99%+ for valid product URLs
- **Memory usage**: Very low (processes one product at a time)
- **File size**: JSON files are typically 2-5KB per product

## 🔄 Version History

- **v4.0** (Current) - Fast bulk scraping, optimized data format, auto cleanup
- **v3.0** - Added sitemap automation and bulk processing
- **v2.1** - Fixed image URL formatting issues
- **v2.0** - Added URL automation and dynamic content handling
- **v1.0** - Basic HTML file scraping

## 📞 Getting Help

If you need help:

1. **Check this README first** - Most questions are answered here
2. **Try the examples** - Copy and paste the code examples to see how they work
3. **Start small** - Test with 1-2 products before doing bulk scraping
4. **Check your internet connection** - Make sure you can access thehouseofrare.com normally

## 📜 Legal and Ethical Use

- This tool is for **educational and personal use only**
- **Respect the website** - Don't overload it with too many requests
- **Follow robots.txt** - Be a good internet citizen
- **Check terms of service** - Make sure your use complies with the website's rules
- **Use responsibly** - Don't use this data for anything harmful or commercial

## 🎯 Quick Start Guide

**For Complete Beginners:**

1. **Install Python** (if you don't have it)
2. **Install packages**: `pip install requests beautifulsoup4`
3. **Download these files** to a folder on your computer
4. **Try this simple code**:

```python
from product_scraper_automated import scrape_product_url

# Scrape one product
product = scrape_product_url("https://thehouseofrare.com/products/breath-rust")
print(f"Product: {product['basic_information']['main_title']}")
print(f"Price: ₹{product['pricing_information']['sale_price']}")
```

5. **Check the output files** that were created
6. **Try bulk scraping** with 5 products using the examples above

That's it! You're now ready to scrape product data efficiently and responsibly.

---

**Happy Scraping! 🕷️**

_Made with ❤️ for educational purposes_
