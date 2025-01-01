import json
import os
import pandas as pd
import numpy as np
from layout import get_layout

COUNTS_FILE = "key_data.json"
RHYTHM_FILE = "rhythm_data.json"

class Analyzer:
    def __init__(self):
        pass

    def load_counts(self):
        if not os.path.exists(COUNTS_FILE):
            return {}
        try:
            with open(COUNTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}

    def load_timestamps(self):
        if not os.path.exists(RHYTHM_FILE):
            return []
        try:
            with open(RHYTHM_FILE, 'r') as f:
                return json.load(f)
        except:
            return []

    def get_heatmap_data(self):
        """Merges layout with current key counts"""
        key_counts = self.load_counts()
        layout = get_layout()
        
        data = []
        for k in layout:
            label = k['label']
            # Handle aliases (e.g., matching 'A' in layout to 'A' in counts)
            # Counts are UPPERCASE. Layout is UPPERCASE.
            count = key_counts.get(label, 0)
            
            # Special handling for SHIFT, CTRL, ALT which might be split into L/R in pynput
            # Layout has SHIFT and SHIFT_R. Pynput gives keys 'KEY.SHIFT' -> 'SHIFT'
            # If we don't find SHIFT_R in counts, maybe it was logged as SHIFT?
            # Actually logger keeps them distinct if pynput does.
            
            data.append({
                'label': label,
                'x': k['x'],
                'y': k['y'], # We might need to invert Y for plotting if using scatter
                'w': k['w'],
                'h': k['h'],
                'count': count
            })
        return pd.DataFrame(data)

    def analyze_rhythm(self):
        timestamps = self.load_timestamps()
        if not timestamps:
            return {
                'total_keystrokes': 0,
                'estimated_wpm': 0,
                'active_minutes': 0,
                'burst_score': 0
            }

        df = pd.DataFrame({'time': timestamps})
        df['delta'] = df['time'].diff()
        
        # Filter out large pauses (e.g., > 5 seconds) for WPM calculation
        # to get "Active WPM" vs "Session WPM"
        active_threshold = 5.0 
        valid_intervals = df[df['delta'] < active_threshold]
        
        total_active_time = valid_intervals['delta'].sum()
        total_keystrokes = len(timestamps)
        
        # WPM: (Total Keystrokes / 5) / (Active Minutes)
        if total_active_time > 0:
            active_minutes = total_active_time / 60.0
            wpm = (len(valid_intervals) / 5) / active_minutes
        else:
            wpm = 0
            active_minutes = 0

        # Burst Score: variance of intervals? 
        # High variance = bursty. Low variance = robotic/steady.
        burst_score = valid_intervals['delta'].std() * 10 if not valid_intervals.empty else 0

        return {
            'total_keystrokes': total_keystrokes,
            'estimated_wpm': round(wpm, 1),
            'active_minutes': round(active_minutes, 2),
            'burst_score': round(burst_score, 2),
            'timestamps': timestamps
        }

if __name__ == "__main__":
    a = Analyzer()
    print(a.get_heatmap_data().head())
    print(a.analyze_rhythm())
