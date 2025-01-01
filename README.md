# KeyHeat

KeyHeat is a privacy-focused keyboard behavior analyzer and heatmap generator. It tracks typing rhythms and key usage frequency to provide insights into typing habits without storing the actual content of what is typed.

## Overview

The application is designed to be lightweight, offline-only, and strictly privacy-preserving. It achieves this by splitting data collection into two uncorrelated streams:
1.  **Key Counts**: Stores purely the frequency of key presses (e.g., how many times "A" was pressed) without any timestamp information.
2.  **Rhythm Logs**: Stores purely the timestamps of key presses without identifying which key was pressed.

This architecture ensures that it is mathematically impossible to reconstruct the original text from the stored logs.

## Features

*   **Heatmap Visualization**: Generates a visual color-coded QWERTY keyboard map showing frequency-based intensity.
*   **Rhythm Analysis**: Estimates Words Per Minute (WPM), identifies typing bursts vs. pauses, and calculates active typing time.
*   **Privacy-First Architecture**: Zero text storage. Data is split into isolated count and timestamp files.
*   **Dashboard**: A local interactive dashboard built with Streamlit to control logging and view analytics.

## Technical Stack

*   **Language**: Python
*   **Input Handling**: pynput (for non-intrusive background key logging)
*   **Visualization**: Matplotlib, Seaborn
*   **Dashboard**: Streamlit

## Installation

1.  Clone the repository or download the source code.
2.  Install the required dependencies using pip:

    ```bash
    pip install streamlit pynput pandas matplotlib seaborn
    ```

## Usage

1.  Navigate to the project directory in your terminal.
2.  Run the Streamlit application:

    ```bash
    streamlit run app.py
    ```

3.  The dashboard will open in your default web browser.
4.  Use the "START Logging" button in the sidebar to begin tracking.
5.  Type naturally in any other application.
6.  Return to the dashboard and click "Refresh View" (or wait for interaction) to verify the heatmap and metrics are updating.
7.  Click "STOP Logging" when finished.

## Data Structure

The application creates two local JSON files in the root directory:

*   `key_data.json`: Contains a dictionary of key labels and their total counts.
*   `rhythm_data.json`: Contains a list of UNIX timestamps representing key press events.

## License

This project is open-source and available for personal use and modification.
