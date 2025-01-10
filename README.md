# Demo app
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://strava-upwrapped.streamlit.app/)

# Project Summary

**Strava Wrapped 2024** is an interactive Streamlit application designed to provide users with a comprehensive summary of their Strava activities throughout the year. By uploading their Strava activity file, users can visualize key metrics, trends, and personal achievements in 2024.

The app generates a personalized fitness report with metrics such as total distance, time spent on different activities, pace, and workout trends. It also includes features like active days heatmaps, activity type breakdowns, and random activity suggestions to encourage users to stay fit and explore new workouts.

## Features

1. **File Upload and Instructions:**

    - Clear step-by-step guide to download and upload the required activities.csv file from Strava.
    - Option to use an in-built example file for demonstration purposes.
      ![image](https://github.com/user-attachments/assets/cd618fc4-bfec-4c4f-a555-7109ef37a07e)


2. **Personalized Activity Metrics:**

    - Displays the most common activity type in 2024 with comparisons to 2023.

    - Shows total hours spent, total distance covered, average pace, and best pace.

    - Provides percentage changes in activity metrics compared to the previous year.
      ![image](https://github.com/user-attachments/assets/788c36be-95f9-49e5-bd03-d76edec32914)


3. **Activity Breakdown:**

    - Radial chart showing the percentage of time spent on different activity types.
      ![image](https://github.com/user-attachments/assets/818a1549-aeab-47ed-bb7e-44537f1a804a)


4. **Trends Visualization:**

    - Interactive line chart showing activity trends over time with filters for specific activity types.
      ![image](https://github.com/user-attachments/assets/3aad2477-c1cf-4076-9de2-5a53b0ca7425)


5. **Active Days Heatmap:**

    - Heatmap displaying daily activity levels throughout the year.

    - Allows users to pick a date and view detailed information about the activities on that day.
      ![image](https://github.com/user-attachments/assets/7621a998-9a08-4915-855f-207ee1c469cd)


6. **Random Activity Suggestions:**

    - Fun feature to suggest random activities to keep users motivated and engaged.
      ![image](https://github.com/user-attachments/assets/125426bf-37d6-4827-bb03-ae14abf3f7e6)

      


## How to Use

1. **Prepare Your Strava Data:**

    - Download your Strava activity archive as described in the sidebar instructions.

    - Extract the `activities.csv` file from the archive.

2. **Upload Your Data:**

    - Use the sidebar to upload your `activities.csv` file.

    - Alternatively, select the checkbox to use the example file.

3. **Explore Your Fitness Insights:**

    - View personalized metrics and activity breakdowns.

    - Interact with the trends chart and heatmap.

    - Get random activity suggestions for your next workout.


## Requirements

    - Python: 3.7+

    - Libraries:

      `streamlit`

      `pandas`

      `matplotlib`

      `numpy`

      `seaborn`

      `plotly`

      `random`


## Installation

1. Clone the repository:

`git clone https://github.com/yourusername/strava-wrapped-2024.git`

2. Navigate to the project directory:

`cd strava-wrapped-2024`

3. Install the required libraries:

`pip install -r requirements.txt`

4. Run the Streamlit app:

`streamlit run app.py`



## Future Enhancements

1. Add support for more detailed metrics such as elevation gain and calorie burn.

2. Include social sharing features for users to share their Strava Wrapped reports.

3. Add a leaderboard to compare metrics with friends.
