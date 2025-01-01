import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from logger import KeyLogger
from analyzer import Analyzer
import time

st.set_page_config(page_title="KeyHeat", layout="wide")

# Persistent Logger control
if 'logger' not in st.session_state:
    st.session_state.logger = KeyLogger()

def toggle_logger():
    if st.session_state.logger.running:
        st.session_state.logger.stop()
    else:
        st.session_state.logger.start()

# Initialize objects
logger = st.session_state.logger
analyzer = Analyzer()

# --- UI ---
st.title("🔥 KeyHeat - Keyboard Behavior Analytics")
st.markdown("Tracks rhythm and frequency without storing what you type.")

# Sidebar Controls
with st.sidebar:
    st.header("Controls")
    
    # Start/Stop Button
    btn_label = "STOP Logging" if logger.running else "START Logging"
    btn_color = "primary" if not logger.running else "secondary"
    st.button(btn_label, type=btn_color, on_click=toggle_logger)
    
    st.divider()
    if st.button("Clear Log Data"):
        logger.clear_data()
        st.rerun()
    
    st.divider()
    st.markdown("**Status**")
    if logger.running:
        st.success("Create some heat! (Logging Active)")
    else:
        st.warning("Logger Paused")

# Main Dashboard
col1, col2 = st.columns([2, 1])

# Data Fetching
key_df = analyzer.get_heatmap_data()
rhythm_stats = analyzer.analyze_rhythm()

# --- HEATMAP VISUALIZATION ---
with col1:
    st.subheader("Keyboard Heatmap")
    
    if not key_df.empty:
        # Plotting
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Max count for normalization
        max_count = key_df['count'].max()
        if max_count == 0: max_count = 1
        
        # Color map
        cmap = plt.cm.plasma
        
        for _, row in key_df.iterrows():
            # Y is inverted in layout usually, but for plt we can just flip logic or axis
            # Let's assume layout y=0 is top. matplotlib y increases upwards.
            # So y_plot = -row['y']
            
            intensity = row['count'] / max_count
            color = cmap(intensity)
            
            # Key shape
            rect = patches.Rectangle(
                (row['x'], -row['y'] - row['h']), # Bottom-left corner
                row['w'], row['h'], 
                linewidth=1, edgecolor='white', facecolor=color,
                joinstyle='round',
                capstyle='round'
            )
            ax.add_patch(rect)
            
            # Label
            # Adjust color based on background
            text_color = 'white' if intensity < 0.5 else 'black'
            ax.text(
                row['x'] + row['w']/2, 
                -row['y'] - row['h']/2, 
                row['label'], 
                ha='center', va='center', fontsize=8, color=text_color, fontweight='bold'
            )

        ax.set_xlim(-0.5, 15)
        ax.set_ylim(-5.5, 1)
        st.pyplot(fig)
    else:
        st.info("No data available yet.")

# --- METRICS ---
with col2:
    st.subheader("Live Metrics")
    
    m1, m2 = st.columns(2)
    m1.metric("WPM (Est.)", rhythm_stats['estimated_wpm'])
    m2.metric("Keystrokes", rhythm_stats['total_keystrokes'])
    
    m3, m4 = st.columns(2)
    m3.metric("Active Mins", rhythm_stats['active_minutes'])
    m4.metric("Burst Score", rhythm_stats['burst_score'])

    st.markdown("### Typing Rhythm")
    timestamps = rhythm_stats.get('timestamps', [])
    if len(timestamps) > 2:
        # Plot intervals
        ts_series = pd.Series(timestamps)
        # Binned activity (keystrokes per minute/second)
        # Let's show keystrokes over the last N events or time
        
        # Simple: Intervals histogram or line chart of momentary speed
        deltas = ts_series.diff().dropna()
        # Filter insane outliers
        deltas = deltas[deltas < 2.0] 
        
        if not deltas.empty:
             st.line_chart(deltas, height=200)
             st.caption("Inter-key intervals (lower = faster)")
    else:
        st.write("Start typing to see rhythm analysis.")

# Auto-refresh logic (Simple rerunning script every few secs if active?)
# Streamlit doesn't auto-rerun by default without interaction or a component.
# We will rely on manual refresh or the user interacting with the app.
# Adding a manual refresh button in sidebar just in case.
with st.sidebar:
    if st.button("Refresh View"):
        st.rerun()

