#!/bin/bash

echo "🕷 IPL 2025 ESPNcricinfo Scraper"
echo "=================================="

# Check if dependencies are installed
echo "📦 Checking dependencies..."
python -c "import requests, bs4, selenium" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
fi

# Check if ChromeDriver is available
echo "🌐 Checking ChromeDriver..."
if ! command -v chromedriver &> /dev/null; then
    echo "⚠️ ChromeDriver not found. Please install:"
    echo "  macOS: brew install chromedriver"
    echo "  Linux: sudo apt-get install chromium-chromedriver"
    echo "  Windows: Download from https://chromedriver.chromium.org/"
    exit 1
fi

# Create output directory
mkdir -p data/raw

echo "🚀 Starting scraper..."
python ipl_espncricinfo_scraper.py "$@"

echo ""
echo "✅ Scraping completed!"
echo "📁 Files created:"
if [ -f "data/raw/matches.csv" ]; then
    echo "  ✓ data/raw/matches.csv"
fi
if [ -f "data/raw/points_table.csv" ]; then
    echo "  ✓ data/raw/points_table.csv"
fi
if [ -f "data/raw/players.json" ]; then
    echo "  ✓ data/raw/players.json"
fi

echo ""
echo "🔄 Next steps:"
echo "  1. Review scraped data"
echo "  2. Run ETL pipeline: cd .. && python src/etl_IPL2025_sqlite.py"
echo "  3. Launch dashboard: ./run_dashboard.sh"
