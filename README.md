# 🗂️ Simple Scraping System - Usage Guide

## ✨ **QUICK START**

### **1. Install Dependencies:**
```powershell
pip install -r requirements.txt
```

### **2. Sitemap Extraction:**
```python
from sitemap_extractor import SitemapExtractor

# Extract product URLs from sitemap
extractor = SitemapExtractor("https://example.com/sitemap.xml")
extractor.load_sitemap()
product_urls = extractor.extract_product_urls()

print(f"Found {len(product_urls)} product URLs:")
for url_data in product_urls:
    print(url_data['url'])
```

### **3. Individual Product Scraping:**
```python
from product_scraper_simple import scrape_product_url

# Scrape individual product
data = scrape_product_url("https://example.com/products/item", save_json=True)
print(f"Product: {data.get('product_name')}")
print(f"Price: {data.get('current_price')}")
```

### **4. Bulk Scraping:**
```python
from bulk_scraper import BulkScraper

# Bulk scrape multiple products
scraper = BulkScraper("https://example.com/sitemap.xml")
results = scraper.scrape_products(max_products=100)
print(f"Scraped {len(results)} products")
```

## 🎯 **EXAMPLE OUTPUTS**

### **Input:** `https://thehouseofrare.com/sitemap.xml`
**Output:** `product_urls_thehouseofrare_com.csv`
```csv
https://thehouseofrare.com/products/item-1
https://thehouseofrare.com/products/item-2
https://thehouseofrare.com/products/item-3
```

## 🔧 **KEY FEATURES**

### **🔍 Smart Detection:**
- Automatically detects product URL patterns
- Supports multiple sitemap formats
- Handles sitemap index files

### **� Clean Output:**
- CSV format for easy processing
- Duplicate removal
- Domain validation

### **�️ Robust Processing:**
- Error handling for malformed XML
- Network timeout handling
- Automatic retry on failures

## 🚀 **ADVANCED USAGE**

### **Custom Filtering:**
```python
from sitemap_extractor import SitemapExtractor

extractor = SitemapExtractor("https://example.com/sitemap.xml")

# Extract with custom filters
product_urls = extractor.extract_product_urls(
    min_urls=10,          # Minimum URLs to extract
    max_urls=1000,        # Maximum URLs to extract
    pattern_filters=['product', 'item', 'shop']  # Custom patterns
)
```

### **Bulk Processing:**
```python
from sitemap_extractor import SitemapExtractor

sitemaps = [
    "https://site1.com/sitemap.xml",
    "https://site2.com/sitemap.xml",
    "https://site3.com/sitemap.xml"
]

for sitemap_url in sitemaps:
    extractor = SitemapExtractor(sitemap_url)
    csv_file = extractor.extract_to_csv()
    print(f"Processed: {csv_file}")
```

## 📊 **SUCCESS METRICS**

- ✅ **Fast Processing**: Results in seconds
- ✅ **High Accuracy**: Pattern-based URL detection
- ✅ **Universal Support**: Works with any sitemap format
- ✅ **Clean Output**: Ready-to-use CSV files
- ✅ **Error Handling**: Robust and reliable

---

**🎉 Your simple sitemap extractor is ready to use!**
