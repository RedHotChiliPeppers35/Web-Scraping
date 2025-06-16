# eMAG Bags Model & Color Scraper
A Python web scraping tool that collects model numbers and color codes from the first 10 pages of the "Bags for Women" category on eMAG.ro. The script uses Selenium with undetected-chromedriver to bypass basic anti-bot protections and parses the product detail pages for reliable product code data.

Features
Scrapes product detail URLs from the first 10 category pages

Visits each product’s page and extracts:

1. Product URL
The direct link to the product’s detail page on eMAG.

2. Model Number
Parsed from the product code on the detail page (<span class="product-code-display hidden-xs">).

3. Color Code
Parsed alongside the model number (e.g., 213BA0063000-990 → model: 213BA0063000, color: 990).

4. Product Title
Text from the image’s alt attribute or the product name in the HTML.

Example: "JACQUEMUS, Geanta de piele cu bareta de umar si logo Le Bambino, Negru"

5. Product Image URL
The src attribute of the product image.

6. Price
Usually extracted from a tag like <p class="product-new-price">.

7. Brand
Sometimes available in the product title or as a data attribute.

Could be parsed from the product name, or sometimes as a separate badge or label.

