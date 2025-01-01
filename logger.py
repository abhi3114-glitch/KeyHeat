import pynput.keyboard
import time
import json
import threading
import os
from datetime import datetime

# File paths
COUNTS_FILE = "key_data.json"
RHYTHM_FILE = "rhythm_data.json"

class KeyLogger:
    def __init__(self):
        self.key_counts = {}
        self.timestamps = []
        self.running = False
        self.listener = None
        self.lock = threading.Lock()
        self._load_data()

    def _load_data(self):
        """Load existing data to persist across sessions"""
        if os.path.exists(COUNTS_FILE):
            try:
                with open(COUNTS_FILE, 'r') as f:
                    self.key_counts = json.load(f)
            except:
                self.key_counts = {}
        
        if os.path.exists(RHYTHM_FILE):
             try:
                with open(RHYTHM_FILE, 'r') as f:
                    self.timestamps = json.load(f)
             except:
                 self.timestamps = []

    def _save_data(self):
        """Save data to independent files"""
        with self.lock:
            with open(COUNTS_FILE, 'w') as f:
                json.dump(self.key_counts, f)
            
            with open(RHYTHM_FILE, 'w') as f:
                json.dump(self.timestamps, f)

    def on_press(self, key):
        if not self.running:
            return

        try:
            # Normalize key name
            if hasattr(key, 'char') and key.char:
                key_name = key.char.upper()
            else:
                key_name = str(key).replace('Key.', '').upper()
        except Exception:
            return # Ignore unknown keys

        with self.lock:
            # 1. Update Counts (Identity only)
            self.key_counts[key_name] = self.key_counts.get(key_name, 0) + 1
            
            # 2. Update Timestamps (Time only, NO Identity)
            self.timestamps.append(time.time())

    def start(self):
        if not self.running:
            self.running = True
            self.listener = pynput.keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            self._auto_save()

    def stop(self):
        self.running = False
        if self.listener:
            self.listener.stop()
            self.listener = None
        self._save_data()

    def _auto_save(self):
        """Periodically save data every 10 seconds"""
        if self.running:
            self._save_data()
            threading.Timer(10, self._auto_save).start()

    def clear_data(self):
        with self.lock:
            self.key_counts = {}
            self.timestamps = []
            self._save_data()

if __name__ == "__main__":
    # For testing independently
    logger = KeyLogger()
    print("Starting logger for 10 seconds...")
    logger.start()
    time.sleep(10)
    logger.stop()
    print("Stopped. Check json files.")
