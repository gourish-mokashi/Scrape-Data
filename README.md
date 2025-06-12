# Simple E-commerce Product Scraper

A clean, simple, and efficient product scraping system for thehouseofrare.com and other e-commerce websites.

## ✨ Features

- **Pattern-Based Scraping** - No AI complexity, just reliable HTML parsing
- **Universal Sitemap Support** - Extract product URLs from any website's sitemap
- **Bulk Processing** - Scrape multiple products efficiently
- **Rate Limiting** - Respectful scraping with delays
- **JSON Export** - Clean, simple data format
- **Error Handling** - Robust operation with proper logging

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Examples

```bash
python automation_simple_fixed.py
```

## 📁 Files

- **`product_scraper_simple.py`** - Main scraper class
- **`sitemap_extractor.py`** - Universal sitemap URL extraction
- **`bulk_scraper.py`** - Fast bulk scraping functionality
- **`automation_simple_fixed.py`** - Usage examples and demonstrations
- **`requirements.txt`** - Python dependencies

## 💡 Usage Examples

### Single Product

```python
from product_scraper_simple import scrape_product_url

data = scrape_product_url("https://thehouseofrare.com/products/paintt-green")
print(f"Product: {data['product_name']}")
print(f"Price: ₹{data['current_price']}")
```

### Bulk Scraping

```python
from product_scraper_simple import scrape_multiple_urls

urls = ["url1", "url2", "url3"]
results = scrape_multiple_urls(urls, delay=1.0, save_combined=True)
```

### Sitemap Extraction

```python
from sitemap_extractor import SitemapExtractor

extractor = SitemapExtractor("https://example.com/sitemap.xml")
extractor.load_sitemap()
products = extractor.extract_product_urls()
```

## 📊 Output Format

Simple JSON structure with all product data at the root level:

```json
{
  "product_name": "WATERCOLOUR EFFECT FLORAL PRINT SHIRT",
  "current_price": 1679,
  "original_price": 2799,
  "discount_percentage": "40% OFF",
  "fabric": "Cotton",
  "fit": "Regular",
  "XS_available": false,
  "S_available": true,
  "M_available": true,
  "product_images": ["image1.jpg", "image2.jpg"]
}
```

## 🔧 Requirements

- Python 3.7+
- requests
- beautifulsoup4
- lxml

## 📄 License

This project is for educational purposes only. Please respect website terms of service and implement appropriate rate limiting.
