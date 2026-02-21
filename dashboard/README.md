# IPL 2025 Interactive Dashboard

An interactive Streamlit dashboard for IPL 2025 analytics, featuring real-time data visualization, team performance analysis, player statistics, and match prediction capabilities.

## 🚀 Features

### 📊 **Overview Dashboard**
- **Season Summary**: Total matches, players, teams, and ML model status
- **Match Timeline**: Interactive timeline of matches throughout the season
- **Recent Matches**: Latest match results and performances

### 🏆 **Team Analysis**
- **Performance Comparison**: Win rates, run rates, wickets taken
- **Team Selection**: Detailed statistics for any IPL team
- **Key Metrics**: Wins, toss success, runs scored, bowling performance

### 👥 **Player Analysis**
- **Top Performers**: Leading run-scorers and wicket-takers
- **Player Search**: Individual player statistics and form analysis
- **Career Stats**: Batting and bowling averages, strike rates

### 🔮 **Match Prediction**
- **ML Prediction**: Trained Random Forest model for match outcomes
- **Team Selection**: Choose any two teams for prediction
- **Confidence Scores**: Probability breakdown for each team

### 📈 **Advanced Analytics**
- **Venue Performance**: Match statistics by stadium
- **Toss Impact**: Analysis of toss decisions on match outcomes
- **Head-to-Head**: Team vs team historical performance
- **Player Form**: Individual player performance trends

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Main IPL2025 ETL project running
- SQLite database populated with data

### Setup
```bash
# Navigate to dashboard directory
cd dashboard

# Install dashboard dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

## 🎯 Usage

### 1. **Load Data**
- Click "🔄 Load/Refresh Data" in the sidebar
- Data loads from the main project database
- Status indicators show loading progress

### 2. **Navigate Pages**
- Use the sidebar dropdown to switch between analysis pages
- Each page provides different insights and visualizations

### 3. **Interactive Features**
- **Team Selection**: Choose teams for detailed analysis
- **Player Search**: Find specific player statistics
- **Match Prediction**: Select teams and conditions for predictions
- **Time Filters**: Analyze specific periods or venues

## 📊 Dashboard Pages

### 📊 Overview
- **Key Metrics**: At-a-glance season statistics
- **Match Timeline**: Visual representation of match schedule
- **Recent Results**: Latest match outcomes and player performances

### 🏆 Team Analysis
- **Performance Charts**: Comparative team metrics
- **Detailed Stats**: Individual team breakdowns
- **Rankings**: Teams by various performance indicators

### 👥 Player Analysis
- **Performance Rankings**: Top batsmen and bowlers
- **Individual Stats**: Detailed player profiles
- **Form Analysis**: Recent performance trends

### 🔮 Match Prediction
- **ML Interface**: Interactive prediction tool
- **Probability Display**: Win chances for each team
- **Confidence Metrics**: Model reliability indicators

### 📈 Advanced Analytics
- **Venue Insights**: Stadium-specific performance
- **Toss Analysis**: Decision impact on outcomes
- **Team Comparisons**: Head-to-head statistics
- **Form Tracking**: Player performance over time

## 🎨 Visualizations

### **Interactive Charts**
- **Bar Charts**: Team performance comparisons
- **Line Graphs**: Timeline and form analysis
- **Pie Charts**: Distribution analysis
- **Progress Bars**: Prediction probabilities

### **Real-time Updates**
- **Data Refresh**: Reload data without restarting
- **Session State**: Maintains user selections
- **Responsive Design**: Works on all screen sizes

## 🔧 Technical Details

### **Data Sources**
- **SQLite Database**: Main project database
- **ETL Pipeline**: Real-time data processing
- **ML Model**: Trained Random Forest classifier

### **Technologies**
- **Streamlit**: Interactive web framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations

### **Performance**
- **Fast Loading**: Optimized data queries
- **Memory Efficient**: Smart data caching
- **Responsive UI**: Smooth user experience

## 🚨 Troubleshooting

### **Common Issues**

1. **Data Loading Errors**
   - Ensure ETL pipeline has been run
   - Check database file exists
   - Verify data permissions

2. **Model Not Trained**
   - Run KPI analysis first
   - Check ML model files exist
   - Refresh data in dashboard

3. **Visualization Issues**
   - Update Plotly version
   - Check browser compatibility
   - Clear browser cache

### **Debug Mode**
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📱 Mobile Support

The dashboard is fully responsive and works on:
- **Desktop**: Full feature set
- **Tablet**: Optimized layout
- **Mobile**: Compact interface

## 🔒 Security

- **Local Deployment**: Data stays on your machine
- **No External Calls**: All processing is local
- **Secure Authentication**: If deployed with authentication

## 🚀 Deployment

### **Local Development**
```bash
streamlit run app.py
```

### **Production Deployment**
```bash
# Install dependencies
pip install -r requirements.txt

# Set port
streamlit run app.py --server.port 8501

# External access
streamlit run app.py --server.address 0.0.0.0
```

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

## 🎯 Features in Development

- **Live Match Updates**: Real-time score integration
- **Advanced Predictions**: More sophisticated ML models
- **Social Sharing**: Export and share insights
- **Custom Filters**: Advanced data filtering options
- **API Integration**: External data sources

## 📞 Support

For dashboard issues:
1. Check the troubleshooting section
2. Verify data pipeline is working
3. Ensure all dependencies are installed
4. Check browser console for errors

---

**Built with Streamlit for interactive IPL 2025 analytics!** 🏏
