#!/bin/bash

echo "🚀 Starting IPL 2025 Dashboard..."

# Check if data exists
if [ ! -f "data/db/IPL2025.db" ]; then
    echo "📊 Loading data first..."
    python src/etl_IPL2025_sqlite.py
    python src/kpi_IPL2025.py
fi

echo "🌐 Launching dashboard..."
echo "📱 Dashboard will open in your browser at: http://localhost:8501"
echo "⚠️  Keep this terminal running to maintain the dashboard"
echo "🛑 Press Ctrl+C to stop the dashboard"

# Start Streamlit dashboard
streamlit run dashboard/app.py --server.port 8501
