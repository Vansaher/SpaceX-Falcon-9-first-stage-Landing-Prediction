# SpaceX-Falcon-9-first-stage-Landing-Prediction
A real-time, interactive web application built with Dash and Plotly to analyze SpaceX launch data. This dashboard allows users to explore mission success rates, payload correlations, and launch site performance through a highly visual interface.

## 🚀 Overview
This project was developed as part of the SpaceX Falcon 9 First Stage Landing Prediction capstone. It provides a user-friendly way to filter through launch data and identify patterns that contribute to a successful first-stage landing.

### Key Features
- **Dynamic Summary Stats:** At-a-glance metrics for Total Launches, Success Rate, and Average Payload that update based on filters.
- **Launch Site Analysis:** Interactive donut charts showing the success/failure ratio for specific sites (LC-39A, SLC-4E, etc.).
- **Payload Correlation:** A scatter plot analyzing the relationship between Payload Mass and Mission Outcome, segmented by Booster Version.
- **Range Filtering:** A dual-handle slider to narrow down mission data by specific payload weight ranges.

## 📊 Dashboard Preview
| Component | Description |
| :--- | :--- |
| **Global Filters** | Dropdown for site selection and RangeSlider for payload mass. |
| **Success Pie Chart** | Visualizes success distribution across all sites or success/fail ratio for one site. |
| **Scatter Plot** | Shows if heavier payloads correlate with higher failure rates and highlights booster performance. |

## 🛠️ Installation & Usage
1. **Clone the repository:**
```bash
git clone [https://github.com/YourUsername/SpaceX-Falcon-9-Dashboard.git](https://github.com/YourUsername/SpaceX-Falcon-9-Dashboard.git)
cd SpaceX-Falcon-9-Dashboard
```
2. **Install dependencies:**
```bash
pip install pandas dash plotly
```
3. **Run the app**
```bash
python app.py
```
- The dashboard will be available at http://127.0.0.1:8050/ in your web browser.

## 📂 Project Structure
- spacex_dash_app.py: The main application script containing the layout and callback logic.
- spacex_launch_dash.csv: The processed dataset containing launch records.
- README.md: Project documentation.

## 💡 Insights Derived
- **VAFB SLC-4E** and **KSC LC-39A** have historically higher success rates compared to other sites.
- Success rates tend to be higher for payloads within the **2,000kg - 5,000kg** range.
- The FT **(Full Thrust)** booster version shows the most consistent success across various payload masses.

Developed by **Javan Herlambang** as part of **IBM Data Science Professional Certificate** course on Coursera.
