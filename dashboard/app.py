import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from etl_IPL2025_sqlite import IPLETLPipeline
from kpi_IPL2025 import IPLKPIAnalyzer

# Page configuration
st.set_page_config(
    page_title="IPL 2025 Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .team-logo {
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'team_kpis' not in st.session_state:
    st.session_state.team_kpis = None
if 'player_kpis' not in st.session_state:
    st.session_state.player_kpis = None
if 'venues_df' not in st.session_state:
    st.session_state.venues_df = pd.DataFrame()
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False

def load_data():
    """Load data and initialize analyzer"""
    try:
        etl = IPLETLPipeline()
        analyzer = IPLKPIAnalyzer()
        
        # Load data
        matches_df, deliveries_df, players_df, points_df, venues_df = analyzer.load_data()
        
        if matches_df is not None:
            st.session_state.matches_df = matches_df
            st.session_state.deliveries_df = deliveries_df
            st.session_state.players_df = players_df
            st.session_state.points_df = points_df
            st.session_state.venues_df = venues_df
            st.session_state.analyzer = analyzer
            st.session_state.data_loaded = True
            
            # Generate KPI report
            report = analyzer.generate_kpi_report(matches_df, deliveries_df, players_df, venues_df)
            st.session_state.team_kpis = report['team_kpis']
            st.session_state.player_kpis = report['player_kpis']
            st.session_state.venues_df = report.get('venues_df', pd.DataFrame())
            st.session_state.model_trained = report['model_trained']
            
            return True
        return False
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return False

def create_team_performance_chart(team_kpis):
    """Create team performance visualization"""
    if team_kpis is None or team_kpis.empty:
        return None
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=('Win Rate', 'Average Run Rate', 'Wickets Taken'),
        specs=[
            [{"type": "bar"} for _ in range(3)],  # Row 1: 3 bars
            [{"type": "bar"} for _ in range(3)]   # Row 2: 3 bars
        ]
    )
    
    # Win Rate
    fig.add_trace(
        go.Bar(x=team_kpis.index, y=team_kpis['win_rate']*100, 
                name='Win Rate (%)', marker_color='#1f77b4'),
        row=1, col=1
    )
    
    # Average Run Rate
    fig.add_trace(
        go.Bar(x=team_kpis.index, y=team_kpis['avg_run_rate'], 
                name='Run Rate', marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    # Wickets Taken
    fig.add_trace(
        go.Bar(x=team_kpis.index, y=team_kpis['wickets_taken'], 
                name='Wickets', marker_color='#2ca02c'),
        row=1, col=3
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Team Performance Analysis")
    return fig

def create_player_stats_chart(player_kpis):
    """Create player statistics visualization"""
    if player_kpis is None or player_kpis.empty:
        return None
    
    # Filter top players
    top_batsmen = player_kpis.nlargest(10, 'runs_scored')
    top_bowlers = player_kpis[player_kpis['wickets_taken'] > 0].nlargest(10, 'wickets_taken')
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Top Run Scorers', 'Top Wicket Takers'),
        specs=[
            [{"type": "bar"}, {"type": "bar"}]  # Single row with 2 columns
        ]
    )
    
    # Top Run Scorers
    fig.add_trace(
        go.Bar(x=top_batsmen['runs_scored'], y=top_batsmen.index, 
                orientation='h', name='Runs', marker_color='#1f77b4'),
        row=1, col=1
    )
    
    # Top Wicket Takers
    fig.add_trace(
        go.Bar(x=top_bowlers['wickets_taken'], y=top_bowlers.index, 
                orientation='h', name='Wickets', marker_color='#ff7f0e'),
        row=1, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Player Performance Analysis")
    return fig

def create_match_timeline(matches_df):
    """Create match timeline visualization"""
    if matches_df is None or matches_df.empty:
        return None
    
    # Convert date to datetime
    matches_df['date'] = pd.to_datetime(matches_df['date'])
    
    # Count matches per day
    daily_matches = matches_df.groupby(matches_df['date'].dt.date).size().reset_index()
    daily_matches.columns = ['date', 'matches']
    
    fig = px.line(
        daily_matches, x='date', y='matches',
        title='Match Timeline - IPL 2025',
        labels={'matches': 'Number of Matches', 'date': 'Date'}
    )
    fig.update_traces(line_color='#1f77b4', line_width=3)
    fig.update_layout(showlegend=False)
    
    return fig

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">🏏 IPL 2025 Analytics Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown("## 📊 Dashboard Controls")
    
    # Load data button
    if st.sidebar.button("🔄 Load/Refresh Data", type="primary"):
        with st.spinner("Loading data..."):
            if load_data():
                st.sidebar.success("✅ Data loaded successfully!")
                st.rerun()
            else:
                st.sidebar.error("❌ Failed to load data")
    
    # Check if data is loaded
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please load data using the button in the sidebar.")
        st.info("📋 Make sure you have run the ETL pipeline first:")
        st.code("python src/etl_IPL2025_sqlite.py")
        return
    
    # Navigation
    page = st.sidebar.selectbox(
        "📍 Choose Page",
        ["📊 Overview", "🏆 Team Analysis", "👥 Player Analysis", 
         "🔮 Match Prediction", "📈 Advanced Analytics"]
    )
    
    # Data summary in sidebar
    st.sidebar.markdown("### 📋 Data Summary")
    st.sidebar.metric("📅 Total Matches", len(st.session_state.matches_df))
    st.sidebar.metric("⚾ Total Deliveries", len(st.session_state.deliveries_df))
    st.sidebar.metric("👥 Total Players", len(st.session_state.players_df))
    st.sidebar.metric("🏆 Total Teams", len(st.session_state.points_df))
    if not st.session_state.venues_df.empty:
        st.sidebar.metric("🏟 Total Venues", len(st.session_state.venues_df))
    
    if page == "📊 Overview":
        st.markdown("## 📊 IPL 2025 Season Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📅 Total Matches", len(st.session_state.matches_df))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("👥 Players", len(st.session_state.players_df))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🏆 Teams", len(st.session_state.points_df))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("🤖 ML Model", "✅ Trained" if st.session_state.model_trained else "❌ Not Trained")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Match timeline
        st.markdown("### 📅 Match Timeline")
        timeline_fig = create_match_timeline(st.session_state.matches_df)
        if timeline_fig:
            st.plotly_chart(timeline_fig, use_container_width=True)
        
        # Recent matches
        st.markdown("### 🏏 Recent Matches")
        recent_matches = st.session_state.matches_df.tail(10)
        st.dataframe(
            recent_matches[['date', 'team1', 'team2', 'winner', 'venue', 'player_of_match']],
            use_container_width=True
        )
    
    elif page == "🏆 Team Analysis":
        st.markdown("## 🏆 Team Performance Analysis")
        
        if st.session_state.team_kpis is not None:
            # Team selection
            selected_team = st.selectbox(
                "Select Team",
                options=st.session_state.team_kpis.index.tolist(),
                index=0
            )
            
            # Team performance chart
            st.markdown("### 📊 Team Performance Comparison")
            team_fig = create_team_performance_chart(st.session_state.team_kpis)
            if team_fig:
                st.plotly_chart(team_fig, use_container_width=True)
            
            # Selected team details
            st.markdown(f"### 📋 {selected_team} Detailed Stats")
            team_stats = st.session_state.team_kpis.loc[selected_team]
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🏆 Win Rate", f"{team_stats['win_rate']:.1%}")
                st.metric("📈 Avg Run Rate", f"{team_stats['avg_run_rate']:.2f}")
                st.metric("🎯 Total Wins", int(team_stats['wins']))
            
            with col2:
                st.metric("⚾ Wickets Taken", int(team_stats['wickets_taken']))
                st.metric("🪙 Toss Win Rate", f"{team_stats['toss_win_rate']:.1%}")
                st.metric("📊 Total Runs", int(team_stats['total_runs_scored']))
    
    elif page == "👥 Player Analysis":
        st.markdown("## 👥 Player Performance Analysis")
        
        if st.session_state.player_kpis is not None:
            # Player statistics chart
            st.markdown("### 📊 Top Performers")
            player_fig = create_player_stats_chart(st.session_state.player_kpis)
            if player_fig:
                st.plotly_chart(player_fig, use_container_width=True)
            
            # Player search
            st.markdown("### 🔍 Player Search")
            selected_player = st.selectbox(
                "Select Player",
                options=st.session_state.player_kpis.index.tolist(),
                index=0
            )
            
            # Player details
            if selected_player in st.session_state.player_kpis.index:
                player_stats = st.session_state.player_kpis.loc[selected_player]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("🏏 Runs Scored", int(player_stats['runs_scored']))
                    st.metric("🎯 Batting Avg", f"{player_stats['batting_average']:.2f}")
                    st.metric("⚡ Strike Rate", f"{player_stats['strike_rate']:.2f}")
                
                with col2:
                    st.metric("⚾ Wickets", int(player_stats['wickets_taken']))
                    st.metric("🎯 Bowling Avg", f"{player_stats['bowling_average']:.2f}" if player_stats['bowling_average'] != float('inf') else "N/A")
                    st.metric("📊 Economy", f"{player_stats['economy_rate']:.2f}")
                
                with col3:
                    st.metric("🎯 Dismissals", int(player_stats['dismissals']))
                    st.metric("🤚 Catches", int(player_stats['dismissals']) if 'catches' in player_stats else 0)
                    st.metric("🧤 Stumpings", int(player_stats['dismissals']) if 'stumpings' in player_stats else 0)
            else:
                st.error(f"Player '{selected_player}' not found in the dataset")
    
    elif page == "🔮 Match Prediction":
        st.markdown("## 🔮 Match Winner Prediction")
        
        if st.session_state.model_trained and st.session_state.analyzer:
            st.markdown("### 🎯 Predict Match Winner")
            
            col1, col2 = st.columns(2)
            
            with col1:
                team1 = st.selectbox(
                    "Team 1",
                    options=st.session_state.matches_df['team1'].unique().tolist(),
                    index=0
                )
                toss_winner = st.selectbox(
                    "Toss Winner",
                    options=[team1] + [t for t in st.session_state.matches_df['team1'].unique().tolist() if t != team1],
                    index=0
                )
            
            with col2:
                team2 = st.selectbox(
                    "Team 2",
                    options=[t for t in st.session_state.matches_df['team1'].unique().tolist() if t != team1],
                    index=0
                )
                toss_decision = st.selectbox(
                    "Toss Decision",
                    options=["bat", "field"],
                    index=0
                )
            
            venue = st.selectbox(
                "Venue",
                options=st.session_state.matches_df['venue'].unique().tolist(),
                index=0
            )
            
            # Predict button
            if st.button("🔮 Predict Winner", type="primary"):
                with st.spinner("Analyzing match..."):
                    prediction = st.session_state.analyzer.predict_match_winner(
                        team1, team2, toss_winner, toss_decision, venue
                    )
                    
                    if prediction:
                        # Display prediction
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("### 🏆 Predicted Winner")
                            st.markdown(f'<h2 class="team-logo">{prediction["predicted_winner"]}</h2>', 
                                        unsafe_allow_html=True)
                            st.metric("🎯 Confidence", f"{prediction['confidence']:.1%}")
                        
                        with col2:
                            st.markdown("### 📊 Win Probabilities")
                            probs = prediction['probabilities']
                            for team, prob in probs.items():
                                st.progress(prob / 100, text=f"{team}: {prob:.1%}")
                            
                            # Detailed probabilities
                            st.markdown("### 📈 Detailed Breakdown")
                            probs_df = pd.DataFrame(list(probs.items()), columns=['Team', 'Probability'])
                            probs_df['Probability'] = probs_df['Probability'] * 100
                            st.dataframe(probs_df, use_container_width=True)
                    else:
                        st.error("❌ Prediction failed. Please try again.")
        else:
            st.warning("⚠️ ML model is not trained. Please run the KPI analysis first.")
    
    elif page == "📈 Advanced Analytics":
        st.markdown("## 📈 Advanced Analytics")
        
        # Analytics options
        analysis_type = st.selectbox(
            "Select Analysis",
            ["Venue Performance", "Toss Impact", "Team Head-to-Head", "Player Form Analysis"]
        )
        
        if analysis_type == "Venue Performance":
            st.markdown("### 🏟 Venue Performance Analysis")
            
            if not st.session_state.venues_df.empty:
                venue_stats = st.session_state.venues_df
                
                # Display venue statistics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("🏟 Total Venues", len(venue_stats))
                    st.metric("📊 Avg Capacity", f"{venue_stats['capacity'].mean():,.0f}" if 'capacity' in venue_stats.columns else "N/A")
                
                with col2:
                    # Venue selection
                    selected_venue = st.selectbox(
                        "Select Venue",
                        options=venue_stats['name'].tolist() if 'name' in venue_stats.columns else [],
                        index=0
                    )
                    
                    if selected_venue and 'name' in venue_stats.columns:
                        venue_info = venue_stats[venue_stats['name'] == selected_venue].iloc[0] if not venue_stats[venue_stats['name'] == selected_venue].empty else None
                        
                        if venue_info is not None:
                            st.markdown(f"### 📍 {selected_venue}")
                            
                            col2a, col2b = st.columns(2)
                            with col2a:
                                st.metric("🏟 City", venue_info.get('city', 'N/A'))
                                st.metric("👥 Capacity", f"{venue_info.get('capacity', 'N/A'):,}")
                                st.metric("⏰ Timezone", venue_info.get('timezone', 'N/A'))
                            
                            with col2b:
                                # Show matches at this venue
                                venue_matches = st.session_state.matches_df[
                                    st.session_state.matches_df['venue'] == selected_venue
                                ]
                                st.metric("📅 Matches Hosted", len(venue_matches))
                                
                                # Show teams with most wins at this venue
                                if not venue_matches.empty:
                                    venue_winners = venue_matches['winner'].value_counts()
                                    if len(venue_winners) > 0:
                                        st.metric("🏆 Most Successful", f"{venue_winners.index[0]} ({venue_winners.iloc[0]} wins)")
                                
                                st.dataframe(
                                    venue_matches[['date', 'team1', 'team2', 'winner', 'player_of_match']],
                                    use_container_width=True
                                )
                
                # Venue distribution chart
                if 'name' in venue_stats.columns:
                    fig = px.bar(
                        venue_stats, 
                        x='name', 
                        y='capacity' if 'capacity' in venue_stats.columns else len(venue_stats),
                        title="Matches per Venue",
                        labels={'name': 'Venue Name', 'capacity': 'Matches Hosted' if 'capacity' not in venue_stats.columns else 'Total Matches'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(venue_stats, use_container_width=True)
            else:
                st.info("📍 No venues data available. Please ensure ipl_2025_venues.csv is loaded.")
        
        elif analysis_type == "Toss Impact":
            st.markdown("### 🪙 Toss Impact Analysis")
            
            toss_analysis = st.session_state.matches_df.groupby('toss_decision').agg({
                'id': 'count',
                'winner': lambda x: x.eq(x.iloc[0]).sum()  # Won toss and match
            }).rename(columns={'id': 'matches', 'winner': 'won_both'})
            
            toss_analysis['win_rate'] = (toss_analysis['won_both'] / toss_analysis['matches']) * 100
            
            fig = px.pie(
                values=toss_analysis['matches'],
                names=toss_analysis.index,
                title="Toss Decision Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(toss_analysis.reset_index(), use_container_width=True)
        
        elif analysis_type == "Team Head-to-Head":
            st.markdown("### ⚔️ Team Head-to-Head Analysis")
            
            teams = st.session_state.matches_df['team1'].unique().tolist()
            team1_h2h = st.selectbox("Team 1", teams, index=0)
            team2_h2h = st.selectbox("Team 2", [t for t in teams if t != team1_h2h], index=0)
            
            h2h_matches = st.session_state.matches_df[
                ((st.session_state.matches_df['team1'] == team1_h2h) & 
                 (st.session_state.matches_df['team2'] == team2_h2h)) |
                ((st.session_state.matches_df['team1'] == team2_h2h) & 
                 (st.session_state.matches_df['team2'] == team1_h2h))
            ]
            
            if not h2h_matches.empty:
                st.info("No matches found between these teams.")
            else:
                h2h_stats = h2h_matches['winner'].value_counts()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📅 Total Matches", len(h2h_matches))
                    st.metric(f"🏆 {team1_h2h} Wins", h2h_stats.get(team1_h2h, 0))
                
                with col2:
                    st.metric(f"🏆 {team2_h2h} Wins", h2h_stats.get(team2_h2h, 0))
                    win_rate = (h2h_stats.get(team1_h2h, 0) / len(h2h_matches)) * 100
                    st.metric("📊 {team1_h2h} Win Rate", f"{win_rate:.1f}%")
                
                st.dataframe(
                    h2h_matches[['date', 'team1', 'team2', 'winner', 'venue']],
                    use_container_width=True
                )
        
        elif analysis_type == "Player Form Analysis":
            st.markdown("### 📈 Player Form Analysis")
            
            selected_player_form = st.selectbox(
                "Select Player",
                st.session_state.player_kpis.index.tolist(),
                index=0
            )
            
            # Get player's match-by-match performance
            player_deliveries = st.session_state.deliveries_df[
                st.session_state.deliveries_df['batsman'] == selected_player_form
            ]
            
            if not player_deliveries.empty:
                st.info("No delivery data found for this player.")
            else:
                # Calculate runs per match
                player_form = player_deliveries.groupby('match_id')['batsman_runs'].sum().reset_index()
                player_form.columns = ['match_id', 'runs']
                
                # Add cumulative runs
                player_form['cumulative_runs'] = player_form['runs'].cumsum()
                
                fig = px.line(
                    player_form, 
                    x='match_id', y='runs',
                    title=f"{selected_player_form} - Runs per Match",
                    labels={'runs': 'Runs Scored', 'match_id': 'Match Number'}
                )
                
                # Add cumulative runs line
                fig.add_scatter(
                    x=player_form['match_id'], 
                    y=player_form['cumulative_runs'],
                    mode='lines',
                    name='Cumulative Runs',
                    line=dict(color='red')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Form statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Matches", len(player_form))
                    st.metric("🏏 Total Runs", player_form['runs'].sum())
                
                with col2:
                    st.metric("🎯 Average", f"{player_form['runs'].mean():.1f}")
                    st.metric("🏆 Highest", player_form['runs'].max())
                
                with col3:
                    st.metric("🎯 50s", (player_form['runs'] >= 50).sum())
                    st.metric("🏆 100s", (player_form['runs'] >= 100).sum())

if __name__ == "__main__":
    main()
