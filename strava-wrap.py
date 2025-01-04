import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import random


# Page Title and Layout Configuration
st.set_page_config(
    page_title="Strava Wrapped",
    layout="centered",
    initial_sidebar_state="expanded",  # Collapsed for a cleaner look on load
    page_icon="🏃",
)

# Page Title
st.title("Your Strava Wrapped 2024")

# Sidebar File Upload with Instructions
with st.sidebar:
    st.subheader("📄 Instructions for File Upload")
    st.markdown(
        """<div style='line-height: 1.6;'>
        <ol>
            <li>Go to <a href='https://www.strava.com/settings/profile' target='_blank'>Strava Settings Profile</a>.</li>
            <li>Select <strong>My Account</strong>.</li>
            <li>Scroll down and click <strong>Get Started</strong> under <em>Download or Delete Your Account</em>.</li>
            <li>Under option 2, click <strong>Request Your Archive</strong>.</li>
            <li>Check your email and download the ZIP file. Extract and use the <code>activities.csv</code> file.</li>
        </ol>
        </div>""",
        unsafe_allow_html=True
    )

    st.subheader("📤 Upload Your Strava Activity File")
    data_file = st.file_uploader("Upload your Strava activity file (CSV)", type=["csv"])

if data_file is not None:
    # Check if the uploaded file is named 'activities.csv'
    if data_file.name == "activities.csv":
        # Read CSV file
        try:
            data = pd.read_csv(data_file)
            # st.success("'activities.csv' uploaded successfully!")
            # st.write("Preview of your data:", data.head())

            # Calculate metrics for 'Your Most Activity 2024'
            data["start_date"] = pd.to_datetime(data["Activity Date"], errors='coerce')
            data_2024 = data[data["start_date"].dt.year == 2024]
            data_2023 = data[data["start_date"].dt.year == 2023]

            # Most frequent activity type in 2024
            if "Activity Type" in data_2024.columns:
                most_common_activity_type = data_2024["Activity Type"].mode()[0]
                most_common_count_2024 = len(data_2024[data_2024["Activity Type"] == most_common_activity_type])
                most_common_count_2023 = len(data_2023[data_2023["Activity Type"] == most_common_activity_type])

                # Calculate % change from 2023
                percent_change = ((most_common_count_2024 - most_common_count_2023) / most_common_count_2023 * 100) if most_common_count_2023 > 0 else None

                # Calculate total hours spent on the most common activity type
                if "Elapsed Time" in data_2024.columns:
                    total_elapsed_time_2024 = data_2024[data_2024["Activity Type"] == most_common_activity_type]["Elapsed Time"].sum()
                    total_hours_2024 = total_elapsed_time_2024 / 60 / 60  # Assuming 'Elapsed Time' is in minutes

                    total_elapsed_time_2023 = data_2023[data_2023["Activity Type"] == most_common_activity_type]["Elapsed Time"].sum()
                    total_hours_2023 = total_elapsed_time_2023 / 60 / 60

                    # Calculate % change in hours spent
                    percent_change_hours = ((total_hours_2024 - total_hours_2023) / total_hours_2023 * 100) if total_hours_2023 > 0 else None
                else:
                    total_hours_2024 = 0
                    percent_change_hours = None

                # Calculate distance metrics
                if "Distance" in data.columns:
                    total_distance_2024 = data_2024["Distance"].sum()
                    total_distance_2023 = data_2023["Distance"].sum()

                    percent_change_distance = ((total_distance_2024 - total_distance_2023) / total_distance_2023 * 100) if total_distance_2023 > 0 else None

                    # Calculate Average Pace (min/km) by averaging row values
                    valid_rows = data_2024[(data_2024["Moving Time"] > 0) & (data_2024["Distance"] > 0)]
                    valid_rows["Pace_min_per_km"] = valid_rows["Moving Time"] / 60 / valid_rows["Distance"]
                    avg_pace = valid_rows["Pace_min_per_km"].mean() if not valid_rows.empty else None

                    # Calculate Best Pace (min/km)
                    best_pace = valid_rows["Pace_min_per_km"].min() if not valid_rows.empty else None

                else:
                    total_distance_2024 = 0
                    percent_change_distance = None
                    avg_pace = None
                    best_pace = None

            
                # 'Your Most Activity 2024' section
                st.markdown("""
<span style="font-weight:bold; font-size:18px;">Strava Unwrapped:</span> 
<span style="font-size:16px; color:gray;">Time Spent Activity Dominates Your Workout Routine</span>
""", unsafe_allow_html=True)
                with st.container():
                    col1, col2, col3 = st.columns([1.5, 1, 1], gap="small")

                    with col1:
                        # Display Image with styled frame
                        image_mapping = {
                            "Run": "https://img.freepik.com/free-photo/running-sport-man-runner-sprinting-outdoor-scenic-nature-fit-muscular-male-athlete-training-trail-running-marathon-run-sporty-fit-athletic-man-working-out-compression-clothing-sprint_155003-14195.jpg",
                            "Weight Training": "https://img.freepik.com/free-photo/athletic-young-woman-doing-fitness-workout-with-dumbbell_1423-225.jpg",
                            "Walk": "https://img.freepik.com/free-photo/cropped-rear-shot-athletic-girl-wearing-pink-sneakers-while-hiking-jogging-pavement-outdoors-woman-jogger-with-fit-beautiful-legs-doing-workout_273609-6285.jpg",
                            "Workout": "https://img.freepik.com/free-photo/young-fitness-woman-sportswear-posing-sitting-with-dumbbells-white_176420-7796.jpg",
                            "Ride": "https://img.freepik.com/free-photo/professional-cyclist-women_23-2149703292.jpg",
                            "HIIT": "https://img.freepik.com/free-photo/active-young-woman-sportswear-jumping-air-sporty-female-athlete-with-strong-resistance-doing-cardio-workout-hiit-training_662251-891.jpg"
                        }
                        image_url = image_mapping.get(most_common_activity_type, "https://img.freepik.com/free-photo/running-sport-man-runner-sprinting-outdoor-scenic-nature-fit-muscular-male-athlete-training-trail-running-marathon-run-sporty-fit-athletic-man-working-out-compression-clothing-sprint_155003-14195.jpg")
                        st.markdown(
                            f"""<div style='background-color: #F4E869 ; border-radius: 20px; padding: 10px;'>
                            <img src='{image_url}' style='width: 100%; border-radius: 20px;'>
                            <p style='text-align: center; margin-top: 16px;'>Your Top Activity was {most_common_activity_type} 🎉</p>
                            </div>""",
                            unsafe_allow_html=True
                        )

                    with col2:
                        st.metric(f"Total {most_common_activity_type}", f"{most_common_count_2024} times")
                        st.metric("% Change from 2023", f"{percent_change:.2f}%")
                        st.metric("Total Hours Spent", f"{total_hours_2024:.2f} hrs")
                        st.metric("% Change in Hours", f"{percent_change_hours:.2f}%")

                    with col3:
                        st.metric("Total Distance", f"{total_distance_2024:.2f} km")
                        st.metric("% Change in Distance", f"{percent_change_distance:.2f}%")
                        st.metric("Average Pace", f"{avg_pace:.2f} min/km" if avg_pace else "N/A")
                        st.metric("Best Pace", f"{best_pace:.2f} min/km" if best_pace else "N/A")

                st.markdown("---")

            else:
                st.warning("No activity type data available for 2024.")

            #"Your Time Spent on Activities in 2024"
            st.markdown("""
<span style="font-weight:bold; font-size:18px;">Activity Breakdown:</span> 
<span style="font-size:16px; color:gray;">Percentage of Time Spent on Different Types of Workouts</span>
""", unsafe_allow_html=True)
            if "Activity Type" in data.columns and "Elapsed Time" in data.columns:
                activity_time = data.groupby("Activity Type")["Elapsed Time"].sum().reset_index()
                activity_time["Elapsed Time (hrs)"] = activity_time["Elapsed Time"] / 3600  # Convert from seconds to hours

                # Calculate total elapsed time and percentages
                total_elapsed_time = activity_time["Elapsed Time (hrs)"].sum()
                activity_time["Percentage"] = (activity_time["Elapsed Time (hrs)"] / total_elapsed_time) * 100

                # Get key properties for colours and labels
                ring_colors = ['#ff5733', '#33ff57', '#5733ff', '#f4c542', '#42f4c5', '#c542f4', '#f44278', '#ff8c33', '#33d1ff', '#ff33a8', '#a8ff33', '#3357ff', '#ff3333', '#33ffcc', '#ff33cc']
                data_len = len(activity_time)

                # Begin creating the figure
                fig = plt.figure(figsize=(4, 4), linewidth=6,
                                 edgecolor='#ffffff', 
                                 facecolor='#ffffff')

                rect = [0.1, 0.1, 0.6, 0.6]

                # Add axis for radial backgrounds
                ax_polar_bg = fig.add_axes(rect, polar=True, frameon=False)
                ax_polar_bg.set_theta_zero_location('N')
                ax_polar_bg.set_theta_direction(1)

                # Loop through each entry in the dataframe and plot a grey
                # ring to create the background for each one
                for i in range(data_len):
                    ax_polar_bg.barh(i, 2 * np.pi, 
                                     color='grey', 
                                     alpha=0.1)
                # Hide all axis items
                ax_polar_bg.axis('off')

                # Add axis for radial chart for each entry in the dataframe
                ax_polar = fig.add_axes(rect, polar=True, frameon=False)
                ax_polar.set_theta_zero_location('N')
                ax_polar.set_theta_direction(1)

                # Loop through each entry in the dataframe and create a coloured 
                # ring for each entry
                for i, row in activity_time.iterrows():
                    angle = row["Elapsed Time (hrs)"] / total_elapsed_time * 2 * np.pi  # Proportional to total elapsed time
                    ax_polar.barh(i, angle, color=ring_colors[i % len(ring_colors)])

                    # Add labels on the right-hand side
                for i, row in activity_time.iterrows():
                    ax_polar.text(
                        2 * np.pi + 0.001,  # Position text outside the radial chart
                        i,  # Corresponding radial position
                        f"{row['Activity Type']}\n{row['Percentage']:.1f}%",  # Text to display
                        ha='left', va='center', color='grey', fontsize=6
                    )
                # Hide all grid elements
                ax_polar.grid(False)
                ax_polar.tick_params(axis='both', left=False, bottom=False, 
                                     labelbottom=False, labelleft=False)

                st.pyplot(fig)

            else:
                with st.container():
                    st.markdown("Placeholder for radial/circular bar chart representing activity time (hrs). Each bar corresponds to an Activity Type based on Elapsed Time.")
                    # Add markdown line at the end of the section
            st.markdown("---")

            #"Your Trends Spend Time Activity in 2024"
            st.markdown("""
<span style="font-weight:bold; font-size:18px;">Tracking Your Fitness Journey:</span> 
<span style="font-size:16px; color:gray;">Key Activity Trends in 2024</span>
""", unsafe_allow_html=True)
            try:
                if "Activity Type" in data_2024.columns and "Elapsed Time" in data_2024.columns:
                    # Prepare data for line chart
                    trends_data = data_2024.groupby(["start_date", "Activity Type"]).agg(
                        total_elapsed_time=("Elapsed Time", "sum")
                    ).reset_index()

                    # Pivot data for plotting
                    trends_pivot = trends_data.pivot(index="start_date", columns="Activity Type", values="total_elapsed_time").fillna(0)

                    # Convert seconds to hours
                    trends_pivot = trends_pivot / 3600

                    # Dropdown for Activity Type selection
                    activity_types = trends_pivot.columns.tolist()
                    selected_activities = st.multiselect("Select activity types to display:", options=activity_types, default=activity_types)

                    # Filter trends_pivot based on selection
                    filtered_trends_pivot = trends_pivot[selected_activities]

                    # Define Andy Warhol-inspired color palette
                    andy_warhol_colors = ['#ff5733', '#33ff57', '#5733ff', '#f4c542', '#42f4c5', '#c542f4', '#f44278', 
                                        '#ff8c33', '#33d1ff', '#ff33a8', '#a8ff33', '#3357ff', '#ff3333', '#33ffcc', '#ff33cc']

                    # Plot the trends with Plotly for animation and interactivity
                    fig = px.line(
                        filtered_trends_pivot.reset_index(),
                        x="start_date",
                        y=selected_activities,
                        title="Your Trends Spend Time Activity in 2024",
                        labels={"start_date": "Date", "value": "Hours Spent", "variable": "Activity Type"},
                        color_discrete_sequence=andy_warhol_colors
                    )

                    # Highlight the most common activity type
                    if most_common_activity_type in selected_activities:
                        fig.add_annotation(
                            x=filtered_trends_pivot.index[-1],
                            y=filtered_trends_pivot[most_common_activity_type].iloc[-1],
                            text=f"Your Most Activity 2024 was {most_common_activity_type}",
                            showarrow=True,
                            arrowhead=2,
                            arrowcolor="orange",
                            font=dict(color="orange", size=12)
                        )

                    fig.update_traces(line_shape="hvh")
                    fig.update_xaxes(rangeslider_visible=True)

                    st.plotly_chart(fig)
                else:
                    st.warning("Activity Type or Elapsed Time data not available for trends.")
            except Exception as e:
                st.error(f"An error occurred while processing the trends line chart: {e}")
            st.markdown("---")

            #"Your Days Spot Activity in 2024"
            st.markdown("""
<span style="font-weight:bold; font-size:18px;">Your Active Days in 2024:</span> 
<span style="font-size:16px; color:gray;">Your 2024 Workout Time Breakdown at a Glance</span>
""", unsafe_allow_html=True)
            try:
                if "Activity Date" in data_2024.columns and "Activity ID" in data_2024.columns:
                    # Prepare data for the heatmap
                    data_2024["Elapsed Time (hours)"] = data_2024["Elapsed Time"] / 3600  # Convert seconds to hours
                    activity_counts = data_2024.groupby("start_date").agg(
                        count_activity=("Activity ID", "count"),
                        total_elapsed_time=("Elapsed Time (hours)", "sum"),
                        activity_types=("Activity Type", lambda x: ", ".join(x))
                    ).reset_index()
                    activity_counts["day"] = activity_counts["start_date"].dt.day
                    activity_counts["month"] = activity_counts["start_date"].dt.month

                    # Aggregate duplicate values
                    aggregated_data = activity_counts.groupby(["month", "day"]).agg(
                        count_activity=("count_activity", "sum"),
                        total_elapsed_time=("total_elapsed_time", "sum")
                    ).reset_index()

                    # Create the pivot table for heatmap
                    heatmap_data = aggregated_data.pivot(index="month", columns="day", values="total_elapsed_time").fillna(0)

                    # Generate heatmap
                    plt.figure(figsize=(12, 8))
                    ax = sns.heatmap(heatmap_data, cmap="Greens", linewidths=0.5, linecolor="gray", cbar=False)
                    plt.title("Your Days Spot Activity in 2024", fontsize=16)
                    plt.xlabel("Day of Month")
                    plt.ylabel("Month")
                    st.pyplot(plt)

                    # Interactivity using Streamlit widgets
                    st.markdown("""
<span style="font-weight:bold; font-size:18px;">Pick Date:</span> 
<span style="font-size:16px; color:gray;">Information in Calendar</span>
""", unsafe_allow_html=True)
                    selected_date = st.date_input(
                        "Select a date to view details:",
                        min_value=data_2024["start_date"].min(),
                        max_value=data_2024["start_date"].max()
                    )

                    # Ensure consistent date formats for comparison
                    selected_date = pd.to_datetime(selected_date).date()
                    activity_counts["start_date"] = activity_counts["start_date"].dt.date

                    # Check if the selected date has activities
                    if selected_date in activity_counts["start_date"].values:
                        details = activity_counts[activity_counts["start_date"] == selected_date]
                        st.markdown(f"**Activity Types:** {details['activity_types'].values[0]}")
                        st.markdown(f"**Spend Time:** {details['total_elapsed_time'].values[0]:.2f} Hours")
                    else:
                        st.markdown("No activity recorded for the selected date.")
                else:
                    st.warning("Activity Date or Activity ID data not available for 2024.")
            except Exception as e:
                st.error(f"An error occurred while processing the heatmap: {e}")
            st.markdown("---")


            #"Next Activity for Your Stay Fit"
            st.markdown("""
<span style="font-weight:bold; font-size:18px;">Stay Fit with a Surprise:</span> 
<span style="font-size:16px; color:gray;">Random Clicks for Fresh Workout Ideas Next Time</span>
""", unsafe_allow_html=True)
            try:
                # Generate random activity suggestion
                if "Activity Type" in data_2024.columns:
                    all_activities = data_2024["Activity Type"].unique().tolist()

                    if st.button("Suggest an Activity"):
                        suggested_activity = random.choice(all_activities)
                        st.markdown(f"### 🏋️ Your Next Activity: **{suggested_activity}**")
                    else:
                        st.markdown("Click the button above to get your next activity!")
                else:
                    st.warning("Activity Type data is not available for suggestions.")
            except Exception as e:
                st.error(f"An error occurred while processing the activity suggestion: {e}")

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")
    else:
        st.error("Please upload a file named 'activities.csv'.")
