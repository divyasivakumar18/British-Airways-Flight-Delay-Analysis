"""
British Airways Flight Delay Analysis & Operational Performance Dashboard
Enterprise-Grade Interactive Business Intelligence Web Application
Built with Streamlit & Plotly
"""

import os
import sys
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# Add src to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from analysis import (
    compute_overall_kpis,
    compute_pareto_root_causes,
    compute_airport_performance_score,
    compute_route_risk_score,
    compute_advanced_statistics
)

st.set_page_config(
    page_title="British Airways Flight Delay Analysis & BI Dashboard",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for British Airways Executive Branding
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #0d131f;
        color: #e2e8f0;
    }
    
    .stMetric {
        background-color: #1a2333;
        border: 1px solid #2d3b55;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .kpi-val {
        color: #f8fafc;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 4px 0;
    }
    
    .kpi-sub {
        font-size: 0.8rem;
        color: #38bdf8;
    }
    
    .ba-badge {
        background: linear-gradient(90deg, #075AAA 0%, #EB2226 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    .section-card {
        background-color: #151d2c;
        border: 1px solid #243048;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'flight_features.csv')
    if not os.path.exists(data_path):
        data_path = 'data/processed/flight_features.csv'
    df = pd.read_csv(data_path)
    df['flight_date'] = pd.to_datetime(df['flight_date'])
    return df

df_raw = load_data()

# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnfbjLOHaHODu6ssPjI51pXe1m-TQCXjYwPjtNQ33fDw&s=10", width=190)
    st.markdown("### **Operational BI Portal**")
    st.markdown("<span class='ba-badge'>BA FLIGHT OPERATIONS</span>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation
    app_page = st.radio(
        "**Navigation Panel**",
        [
            "?? Executive Overview",
            "?? Delay Root Cause & Pareto",
            "?? Airport Performance Scores",
            "??? Route Risk & Network",
            "?? Temporal Bottlenecks & Scheduling"
        ]
    )
    
    st.markdown("---")
    st.markdown("#### **Global Filters**")
    
    # Months Filter
    all_months = df_raw['month_name'].unique().tolist()
    selected_months = st.multiselect("Months", options=all_months, default=all_months)
    
    # Haul Type Filter
    haul_types = ['All'] + sorted(df_raw['haul_type'].unique().tolist())
    selected_haul = st.selectbox("Flight Haul", options=haul_types, index=0)
    
    # Origin Airport Filter
    origin_list = ['All'] + sorted(df_raw['origin_airport'].unique().tolist())
    selected_origin = st.selectbox("Origin Airport", options=origin_list, index=0)
    
    # Destination Airport Filter
    dest_list = ['All'] + sorted(df_raw['dest_airport'].unique().tolist())
    selected_dest = st.selectbox("Destination Airport", options=dest_list, index=0)
    
    # Peak / Off-Peak Filter
    peak_filter = st.selectbox("Operational Period", options=['All', 'Peak', 'Off-Peak'], index=0)

# Filter dataset dynamically
filtered_df = df_raw.copy()

if selected_months:
    filtered_df = filtered_df[filtered_df['month_name'].isin(selected_months)]
if selected_haul != 'All':
    filtered_df = filtered_df[filtered_df['haul_type'] == selected_haul]
if selected_origin != 'All':
    filtered_df = filtered_df[filtered_df['origin_airport'] == selected_origin]
if selected_dest != 'All':
    filtered_df = filtered_df[filtered_df['dest_airport'] == selected_dest]
if peak_filter != 'All':
    filtered_df = filtered_df[filtered_df['peak_period'] == peak_filter]

# Compute KPIs
kpis = compute_overall_kpis(filtered_df)

with st.sidebar:
    st.markdown("---")
    st.caption(f"**Filtered Scope:** {kpis['total_flights']:,} / {len(df_raw):,} flights ({kpis['total_flights']/len(df_raw)*100:.1f}%)")


# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==============================================================================
if app_page == "?? Executive Overview":
    st.title("?? British Airways Operational Performance Overview")
    st.markdown("Executive business intelligence monitoring flight delay rates, on-time performance (OTP), cancellations, and network stability across the global schedule.")
    
    # Top KPI Row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Flights", f"{kpis['total_flights']:,}", f"{kpis['operated_flights']:,} Operated")
    c2.metric("Delay Rate", f"{kpis['delay_rate_operated_pct']}%", f"{kpis['delayed_flights']:,} Delayed", delta_color="inverse")
    c3.metric("On-Time (OTP)", f"{kpis['on_time_performance_otp']}%", "Standard <=15 min")
    c4.metric("Cancellation Rate", f"{kpis['cancellation_rate_pct']}%", f"{kpis['cancelled_flights']:,} Cancelled", delta_color="inverse")
    c5.metric("Avg Dep Delay", f"{kpis['avg_departure_delay_min']} m", f"Med: {kpis['median_departure_delay_min']} m")
    c6.metric("Total Delay Hours", f"{kpis['total_arrival_delay_minutes']/60:,.0f} hrs", f"Max: {kpis['max_arrival_delay_min']} m")
    
    st.markdown("---")
    
    row1_c1, row1_c2 = st.columns([7, 5])
    
    with row1_c1:
        st.subheader("?? Monthly Flight Volume vs Delay Rate Trend")
        monthly_grp = filtered_df.groupby(['month', 'month_name']).agg(
            total_flights=('flight_number', 'count'),
            delayed_flights=('delay_status', lambda x: (x == 'Delayed').sum()),
            operated_flights=('is_cancelled', lambda x: (x == 0).sum())
        ).reset_index()
        monthly_grp['delay_rate_pct'] = (monthly_grp['delayed_flights'] / monthly_grp['operated_flights'] * 100).round(2)
        
        fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
        fig_trend.add_trace(
            go.Bar(
                x=monthly_grp['month_name'],
                y=monthly_grp['total_flights'],
                name="Flight Volume",
                marker_color='#075AAA',
                opacity=0.85
            ),
            secondary_y=False
        )
        fig_trend.add_trace(
            go.Scatter(
                x=monthly_grp['month_name'],
                y=monthly_grp['delay_rate_pct'],
                name="Delay Rate (%)",
                mode='lines+markers',
                line=dict(color='#EB2226', width=3),
                marker=dict(size=8, color='#FF6B6B')
            ),
            secondary_y=True
        )
        fig_trend.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151d2c",
            plot_bgcolor="#151d2c",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=30, b=20),
            height=380
        )
        fig_trend.update_yaxes(title_text="Scheduled Flight Count", secondary_y=False, gridcolor="#243048")
        fig_trend.update_yaxes(title_text="Delay Rate (%)", secondary_y=True, gridcolor="#243048")
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with row1_c2:
        st.subheader("?? Flight Operational Status Breakdown")
        status_counts = filtered_df['delay_status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        fig_donut = px.pie(
            status_counts,
            names='Status',
            values='Count',
            hole=0.55,
            color='Status',
            color_discrete_map={
                'On Time': '#10B981',
                'Delayed': '#EB2226',
                'Cancelled': '#F59E0B',
                'Diverted': '#6366F1'
            }
        )
        fig_donut.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151d2c",
            plot_bgcolor="#151d2c",
            margin=dict(l=20, r=20, t=30, b=20),
            height=380,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    # Row 2
    row2_c1, row2_c2 = st.columns([6, 6])
    with row2_c1:
        st.subheader("?? Delay Severity Distribution")
        sev_order = ['Early / Ahead', 'On Time / Minor (1-15 min)', 'Short Delay (16-30 min)', 
                     'Moderate Delay (31-60 min)', 'Major Delay (61-120 min)', 'Severe Delay (120+ min)', 'Cancelled', 'Diverted']
        sev_df = filtered_df['delay_severity'].value_counts().reindex(sev_order).dropna().reset_index()
        sev_df.columns = ['Severity', 'Count']
        sev_df['Pct'] = (sev_df['Count'] / sev_df['Count'].sum() * 100).round(2)
        
        fig_sev = px.bar(
            sev_df,
            x='Severity',
            y='Count',
            text='Pct',
            color='Severity',
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        fig_sev.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_sev.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151d2c",
            plot_bgcolor="#151d2c",
            showlegend=False,
            margin=dict(l=20, r=20, t=30, b=20),
            height=340
        )
        st.plotly_chart(fig_sev, use_container_width=True)
        
    with row2_c2:
        st.subheader("?? Haul Type Performance Comparison")
        haul_summary = filtered_df.groupby('haul_type').agg(
            total_flights=('flight_number', 'count'),
            operated=('is_cancelled', lambda x: (x == 0).sum()),
            delayed=('delay_status', lambda x: (x == 'Delayed').sum()),
            avg_arr_delay=('arrival_delay', 'mean'),
            avg_recovery=('delay_recovery_min', 'mean')
        ).reset_index()
        haul_summary['delay_rate_pct'] = (haul_summary['delayed'] / haul_summary['operated'] * 100).round(2)
        haul_summary['avg_arr_delay'] = haul_summary['avg_arr_delay'].round(2)
        haul_summary['avg_recovery'] = haul_summary['avg_recovery'].round(2)
        
        fig_haul = px.bar(
            haul_summary,
            x='haul_type',
            y='delay_rate_pct',
            color='haul_type',
            text='delay_rate_pct',
            color_discrete_map={'Short-Haul': '#3B82F6', 'Medium-Haul': '#10B981', 'Long-Haul': '#8B5CF6'},
            title="Delay Rate by Flight Haul"
        )
        fig_haul.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_haul.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151d2c",
            plot_bgcolor="#151d2c",
            showlegend=False,
            height=340,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_haul, use_container_width=True)


# ==============================================================================
# PAGE 2: DELAY ROOT CAUSE & PARETO ANALYSIS
# ==============================================================================
elif app_page == "?? Delay Root Cause & Pareto":
    st.title("?? Delay Root Cause & Pareto (80/20) Analytics")
    st.markdown("Detailed breakdown of flight disruption sources, identifying the **vital few** delay categories responsible for over 80% of total delay minutes.")
    
    pareto_df = compute_pareto_root_causes(filtered_df)
    
    col1, col2 = st.columns([7, 5])
    
    with col1:
        st.subheader("?? Delay Root Cause Pareto Curve (80/20 Rule)")
        fig_p = make_subplots(specs=[[{"secondary_y": True}]])
        fig_p.add_trace(
            go.Bar(
                x=pareto_df['delay_cause'],
                y=pareto_df['total_delay_minutes'],
                name="Delay Minutes",
                marker_color='#075AAA',
                text=pareto_df['pct_of_total_minutes'].apply(lambda x: f"{x:.1f}%"),
                textposition="outside"
            ),
            secondary_y=False
        )
        fig_p.add_trace(
            go.Scatter(
                x=pareto_df['delay_cause'],
                y=pareto_df['cumulative_pct'],
                name="Cumulative Share (%)",
                mode='lines+markers',
                line=dict(color='#EB2226', width=3),
                marker=dict(size=9, color='#FF6B6B')
            ),
            secondary_y=True
        )
        # 80% Benchmark Line
        fig_p.add_hline(y=80, line_dash="dash", line_color="#F59E0B", annotation_text="80% Pareto Threshold", secondary_y=True)
        
        fig_p.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151d2c",
            plot_bgcolor="#151d2c",
            hovermode="x unified",
            height=420,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig_p.update_yaxes(title_text="Total Delay Minutes", secondary_y=False, gridcolor="#243048")
        fig_p.update_yaxes(title_text="Cumulative Percentage (%)", range=[0, 105], secondary_y=True, gridcolor="#243048")
        st.plotly_chart(fig_p, use_container_width=True)
        
    with col2:
        st.subheader("?? Cause Impact Matrix")
        st.dataframe(
            pareto_df[['delay_cause', 'total_delay_minutes', 'pct_of_total_minutes', 'cumulative_pct', 'avg_delay_per_incident']],
            column_config={
                "delay_cause": "Primary Delay Driver",
                "total_delay_minutes": st.column_config.NumberColumn("Total Delay (Min)", format="%,.0f"),
                "pct_of_total_minutes": st.column_config.NumberColumn("Share %", format="%.2f%%"),
                "cumulative_pct": st.column_config.NumberColumn("Cumulative %", format="%.2f%%"),
                "avg_delay_per_incident": st.column_config.NumberColumn("Avg / Flight (Min)", format="%.1f m"),
            },
            hide_index=True,
            use_container_width=True,
            height=320
        )
        st.info("?? **Pareto Insight:** Late-Arriving Aircraft and Airline Carrier operations account for over **60% of all delay minutes**, showing that rotational turnaround management is BA's highest leverage opportunity.")

    st.markdown("---")
    st.subheader("⚡ Delay Propagation: Departure Delay vs Arrival Delay")
    scatter_sample = filtered_df[(filtered_df['is_cancelled'] == 0) & (filtered_df['is_diverted'] == 0)].dropna(subset=['departure_delay', 'arrival_delay'])
    if len(scatter_sample) > 3000:
        scatter_sample = scatter_sample.sample(3000, random_state=42)
    
    # Render scatter plot with robust trendline
    try:
        fig_prop = px.scatter(
            scatter_sample,
            x='departure_delay',
            y='arrival_delay',
            color='haul_type',
            trendline='ols',
            opacity=0.6,
            labels={'departure_delay': 'Departure Delay (Minutes)', 'arrival_delay': 'Arrival Delay (Minutes)'},
            color_discrete_map={'Short-Haul': '#38BDF8', 'Medium-Haul': '#34D399', 'Long-Haul': '#F43F5E'},
            title="Delay Propagation & In-Flight Absorption Regression"
        )
    except Exception:
        fig_prop = px.scatter(
            scatter_sample,
            x='departure_delay',
            y='arrival_delay',
            color='haul_type',
            opacity=0.6,
            labels={'departure_delay': 'Departure Delay (Minutes)', 'arrival_delay': 'Arrival Delay (Minutes)'},
            color_discrete_map={'Short-Haul': '#38BDF8', 'Medium-Haul': '#34D399', 'Long-Haul': '#F43F5E'},
            title="Delay Propagation & In-Flight Absorption Regression"
        )
        if len(scatter_sample) > 1:
            slope, intercept = np.polyfit(scatter_sample['departure_delay'], scatter_sample['arrival_delay'], 1)
            x_vals = np.linspace(float(scatter_sample['departure_delay'].min()), float(scatter_sample['departure_delay'].max()), 100)
            y_vals = slope * x_vals + intercept
            fig_prop.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode='lines',
                    name=f'OLS Fit (y = {slope:.2f}x + {intercept:.1f})',
                    line=dict(color='#F59E0B', width=3, dash='dash')
                )
            )

    fig_prop.add_shape(type="line", x0=-20, y0=-20, x1=300, y1=300, line=dict(color="#94A3B8", dash="dot"))
    fig_prop.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151d2c",
        plot_bgcolor="#151d2c",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_prop, use_container_width=True)


# ==============================================================================
# PAGE 3: AIRPORT PERFORMANCE SCORES
# ==============================================================================
elif app_page == "?? Airport Performance Scores":
    st.title("?? Airport Operational Performance & Benchmark Scores")
    st.markdown("Multi-factor normalized operational scoring (0?100) evaluating station on-time reliability, delay rates, and cancellation frequencies.")
    
    airports_df = compute_airport_performance_score(filtered_df, min_flight_threshold=20)
    
    top_c1, top_c2 = st.columns([8, 4])
    with top_c1:
        st.subheader("?? Airport Performance Score Ranking")
        st.dataframe(
            airports_df[['rank', 'airport_code', 'airport_city', 'performance_score', 'performance_tier', 'delay_rate_pct', 'avg_departure_delay_min', 'on_time_performance_pct', 'cancellation_rate_pct', 'total_flights']],
            column_config={
                "rank": "Rank",
                "airport_code": "IATA",
                "airport_city": "City / Hub",
                "performance_score": st.column_config.ProgressColumn("Score (0-100)", min_value=0, max_value=100, format="%.1f"),
                "performance_tier": "Tier",
                "delay_rate_pct": st.column_config.NumberColumn("Delay Rate", format="%.1f%%"),
                "avg_departure_delay_min": st.column_config.NumberColumn("Avg Dep Delay", format="%.1f m"),
                "on_time_performance_pct": st.column_config.NumberColumn("OTP %", format="%.1f%%"),
                "cancellation_rate_pct": st.column_config.NumberColumn("Cancel %", format="%.2f%%"),
                "total_flights": st.column_config.NumberColumn("Flights", format="%,d")
            },
            hide_index=True,
            use_container_width=True,
            height=450
        )
        
    with top_c2:
        st.subheader("?? Tier Distribution")
        tier_counts = airports_df['performance_tier'].value_counts().reset_index()
        tier_counts.columns = ['Tier', 'Count']
        fig_tier = px.pie(
            tier_counts,
            names='Tier',
            values='Count',
            color='Tier',
            color_discrete_map={'Excellent': '#10B981', 'Good': '#3B82F6', 'Moderate': '#F59E0B', 'Needs Improvement': '#EF4444'}
        )
        fig_tier.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151d2c",
            plot_bgcolor="#151d2c",
            height=400,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_tier, use_container_width=True)

    st.markdown("---")
    st.subheader("?? Station Volume vs Delay Rate Positioning")
    fig_bubble = px.scatter(
        airports_df,
        x='total_flights',
        y='delay_rate_pct',
        size='avg_departure_delay_min',
        color='performance_tier',
        hover_name='airport_city',
        text='airport_code',
        labels={'total_flights': 'Total Flight Departures', 'delay_rate_pct': 'Delay Rate (%)', 'avg_departure_delay_min': 'Avg Delay (min)'},
        color_discrete_map={'Excellent': '#10B981', 'Good': '#3B82F6', 'Moderate': '#F59E0B', 'Needs Improvement': '#EF4444'}
    )
    fig_bubble.update_traces(textposition='top center')
    fig_bubble.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151d2c",
        plot_bgcolor="#151d2c",
        height=450,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_bubble, use_container_width=True)


# ==============================================================================
# PAGE 4: ROUTE RISK & NETWORK INTELLIGENCE
# ==============================================================================
elif app_page == "??? Route Risk & Network":
    st.title("??? Route Risk Intelligence & Network Performance")
    st.markdown("Dynamic risk assessment across BA scheduled city pairs identifying high-volatility, delay-prone corridors.")
    
    routes_df = compute_route_risk_score(filtered_df, min_flight_threshold=15)
    
    col1, col2 = st.columns([7, 5])
    with col1:
        st.subheader("?? Top 15 Highest-Risk Scheduled Routes")
        top_risk = routes_df.head(15)
        fig_r = px.bar(
            top_risk,
            y='route',
            x='risk_score',
            color='risk_category',
            orientation='h',
            text='risk_score',
            color_discrete_map={'Critical': '#DC2626', 'High': '#EA580C', 'Medium': '#FBBF24', 'Low': '#10B981'}
        )
        fig_r.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_r.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151d2c",
            plot_bgcolor="#151d2c",
            yaxis=dict(autorange="reversed"),
            height=460,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_r, use_container_width=True)
        
    with col2:
        st.subheader("??? Risk Category Summary")
        st.dataframe(
            routes_df[['route', 'haul_type', 'risk_score', 'risk_category', 'delay_rate_pct', 'avg_arrival_delay_min', 'cancellation_rate_pct']].head(20),
            column_config={
                "route": "Route",
                "haul_type": "Haul",
                "risk_score": st.column_config.ProgressColumn("Risk Score", min_value=0, max_value=100, format="%.1f"),
                "risk_category": "Category",
                "delay_rate_pct": st.column_config.NumberColumn("Delay Rate", format="%.1f%%"),
                "avg_arrival_delay_min": st.column_config.NumberColumn("Avg Arr Delay", format="%.1f m"),
                "cancellation_rate_pct": st.column_config.NumberColumn("Cancel %", format="%.2f%%")
            },
            hide_index=True,
            use_container_width=True,
            height=460
        )

    st.markdown("---")
    st.subheader("?? Route Distance vs Delay Severity")
    fig_dist = px.scatter(
        routes_df,
        x='distance_km',
        y='avg_arrival_delay_min',
        size='total_flights',
        color='haul_type',
        hover_name='route',
        labels={'distance_km': 'Route Distance (km)', 'avg_arrival_delay_min': 'Avg Arrival Delay (min)'},
        color_discrete_map={'Short-Haul': '#38BDF8', 'Medium-Haul': '#34D399', 'Long-Haul': '#F43F5E'}
    )
    fig_dist.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151d2c",
        plot_bgcolor="#151d2c",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_dist, use_container_width=True)


# ==============================================================================
# PAGE 5: TEMPORAL BOTTLENECKS & SCHEDULING
# ==============================================================================
elif app_page == "?? Temporal Bottlenecks & Scheduling":
    st.title("?? Temporal Bottlenecks & Flight Bank Scheduling")
    st.markdown("Hour-by-hour and day-of-week heatmaps revealing rotational compounding delay effects across the flight schedule.")
    
    st.subheader("?? Operational Heatmap: Day of Week ? Departure Hour Delay Rate")
    
    # Pivot Day of Week x Dep Hour
    heatmap_data = filtered_df[filtered_df['is_cancelled'] == 0].groupby(['day_name', 'dep_hour']).agg(
        delay_rate=('delay_status', lambda x: (x == 'Delayed').mean() * 100)
    ).reset_index()
    
    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    heatmap_pivot = heatmap_data.pivot(index='day_name', columns='dep_hour', values='delay_rate').reindex(day_order)
    
    fig_heat = px.imshow(
        heatmap_pivot,
        labels=dict(x="Scheduled Departure Hour (24h)", y="Day of Week", color="Delay Rate (%)"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        color_continuous_scale="Reds",
        aspect="auto"
    )
    fig_heat.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151d2c",
        plot_bgcolor="#151d2c",
        height=400,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown("---")
    
    row_c1, row_c2 = st.columns(2)
    
    with row_c1:
        st.subheader("? Hourly Compounding Delay Curve")
        hourly_perf = filtered_df[filtered_df['is_cancelled'] == 0].groupby('dep_hour').agg(
            avg_dep_delay=('departure_delay', 'mean'),
            avg_arr_delay=('arrival_delay', 'mean'),
            delay_rate=('delay_status', lambda x: (x == 'Delayed').mean() * 100)
        ).reset_index()
        
        fig_hourly = go.Figure()
        fig_hourly.add_trace(go.Scatter(x=hourly_perf['dep_hour'], y=hourly_perf['avg_dep_delay'], name="Avg Dep Delay (min)", line=dict(color="#38BDF8", width=3)))
        fig_hourly.add_trace(go.Scatter(x=hourly_perf['dep_hour'], y=hourly_perf['avg_arr_delay'], name="Avg Arr Delay (min)", line=dict(color="#F43F5E", width=3)))
        fig_hourly.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151d2c",
            plot_bgcolor="#151d2c",
            xaxis_title="Departure Hour",
            yaxis_title="Average Delay (Minutes)",
            height=350,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_hourly, use_container_width=True)
        
    with row_c2:
        st.subheader("?? Seasonal Disruption & Weather Profile")
        seasonal_grp = filtered_df.groupby('season').agg(
            total_flights=('flight_number', 'count'),
            delay_rate=('delay_status', lambda x: (x == 'Delayed').mean() * 100),
            cancel_rate=('is_cancelled', lambda x: x.mean() * 100),
            weather_delay_mins=('weather_delay', 'sum')
        ).reindex(['Winter', 'Spring', 'Summer', 'Autumn']).reset_index()
        
        fig_season = px.bar(
            seasonal_grp,
            x='season',
            y='delay_rate',
            text='delay_rate',
            color='season',
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_season.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_season.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151d2c",
            plot_bgcolor="#151d2c",
            showlegend=False,
            yaxis_title="Delay Rate (%)",
            height=350,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_season, use_container_width=True)
