# 🌦️ Weather Data Analysis

A modern desktop application for exploring, visualizing, and analyzing weather datasets. Built with **Python**, **Tkinter**, **Pandas**, and **Matplotlib**, it provides a dark-themed GUI with a dashboard, searchable data table, summary statistics, and weather-condition comparisons.

## ✨ Features

### 📊 Dashboard
- View the total number of records and dataset columns.
- Review average temperature, average humidity, and missing-value counts.
- See quick insights such as the most common weather condition, mean visibility, and temperature extremes.
- Explore charts for:
  - Weather-condition frequency
  - Temperature distribution
  - Average temperature by weather condition

### 🔎 Data Explorer
- Browse dataset records in a scrollable table.
- Search across rows to filter matching records.
- Export filtered results to a new CSV file.

### 📈 Analysis Lab
- View summary statistics for dataset columns.
- Inspect missing values, missing-value percentages, non-null counts, and data types.
- Compare average numeric measurements by weather condition.

### 📂 CSV Support
- Load a dataset using the **Open CSV** button.
- If `Weather_Dataset.csv` is in the same folder as the Python script (or the current working directory), the app attempts to load it automatically.
- Reset the app using **Reset System**. Resetting unloads the data from the application; it does **not** delete the original CSV file.

### 🎨 Modern GUI
- Dark navy interface with turquoise accents.
- Sidebar navigation and dashboard metric cards.
- Embedded Matplotlib charts and scrollable tables.

## 🧰 Built With

- **Python 3**
- **Tkinter** — desktop GUI (usually included with Python)
- **Pandas** — loading and analyzing CSV data
- **Matplotlib** — charts embedded in the GUI

## 📁 Project Structure

```text
Weather-Data-Analysis/
├── Weather Data Analysis.py
├── Weather_Dataset.csv          # Your dataset (optional, add your own)
└── README.md
```

> The CSV dataset is not bundled with this project by default. Use your own weather dataset, or select a CSV file from inside the application.

## ⚙️ Installation

### 1. Install Python

Install Python 3 from the official Python website. During installation on Windows, enable **Add Python to PATH**.

### 3. Install dependencies

```bash
python -m pip install pandas matplotlib
```

### 4. Add your dataset

Place `Weather_Dataset.csv` beside the Python script for automatic loading, or open the application and choose **Open CSV** to select a file.

The application works with CSV files. For the best results, use a dataset with weather measurements such as temperature, humidity, visibility, and a weather-condition column.

## 🗃️ Dataset Columns

The app recognizes common column names including:

| Measurement | Example column names |
|---|---|
| Temperature | `Temp_C`, `Temperature`, `Temperature_C` |
| Relative humidity | `Rel Hum_%`, `Relative Humidity`, `Humidity` |
| Visibility | `Visibility_km`, `Visibility` |
| Weather condition | `Weather`, `Weather Condition`, `Conditions` |

Other columns can also be displayed in the data explorer and included in general summary statistics. Some dashboard charts and insights require the corresponding measurement columns to be present.

Column names vary between datasets. If a chart says a required column was not found, check the column names in your CSV and adjust them to match one of the recognized names above.

## 🖱️ How to Use

1. Start the application.
2. Load your CSV using **Open CSV** if it was not loaded automatically.
3. Select **Dashboard** to view overview cards, quick insights, and charts.
4. Select **Data Explorer** to search records and export filtered rows.
5. Select **Analysis** to review summary statistics and missing values.
6. Select **Reset System** to unload the current dataset and return to the initial dashboard. Confirm the reset when prompted.

## 📦 Exporting Data

In **Data Explorer**, enter a search term to filter records. Click **Export filtered CSV** to save the matching rows to a new CSV file. The original dataset is not modified.

## ⚠️ Notes

- This is a **dataset analysis tool**, not a live weather forecast application.
- Analysis results are calculated from the CSV file currently loaded.
- Large datasets may take longer to display. The data explorer displays up to 1,500 matching rows in the table at a time.
- Matplotlib is required for charts. If it is missing, install it with `python -m pip install matplotlib`.

