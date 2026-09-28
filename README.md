# ✈️ Air Tracker - Flight Analytics

An interactive Flight Analytics Dashboard developed using MySQL, Python, Pandas, Plotly and Streamlit.

## 📌 Project Overview

The Flight Analytics project analyzes flight operations data stored in a MySQL database and presents the results through an interactive Streamlit dashboard.

The dashboard helps analyze:

- Total number of flights
- Flight status
- Delayed flights
- Cancelled flights
- Airline performance
- Airport activity
- Destination airports
- Average delay by airport
- Detailed flight records

## 🎯 Project Objectives

The main objectives of this project are:

1. Store flight data in a relational MySQL database.
2. Retrieve and analyze data using SQL.
3. Perform data analysis using Python and Pandas.
4. Create interactive visualizations using Plotly.
5. Develop an interactive dashboard using Streamlit.
6. Provide useful insights into flight operations and delays.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and application development |
| MySQL | Database management |
| Pandas | Data manipulation and analysis |
| Plotly | Interactive charts |
| Streamlit | Dashboard development |
| SQLAlchemy | Database connectivity |
| Git | Version control |
| GitHub | Project repository |

## 📊 Dashboard Features

### Flight Overview

The dashboard displays key performance indicators:

- Total Flights
- Delayed Flights
- Cancelled Flights
- Delay Percentage

### Flight Status Analysis

Flights are analyzed according to:

- Cancelled
- Delayed
- Departed
- Landed
- Scheduled

### Airline Performance

The dashboard compares the number of flights operated by different airlines.

### Airport Analysis

The dashboard provides:

- Top destination airports
- Average delay by airport
- Airport-wise flight activity

### Flight Details

Users can view detailed flight records including:

- Flight ID
- Flight Number
- Airline Code
- Aircraft Registration
- Origin Airport
- Destination Airport
- Scheduled information

## 🔎 Interactive Filters

The dashboard provides filters for:

- Airline
- Flight Status
- Origin Airport
- Destination Airport

These filters allow users to explore specific portions of the flight dataset.

## 🗄️ Database

The project uses MySQL as the backend database.

Main tables include:

- `flights`
- `airport`
- `aircraft`
- `airport_delays`

The Streamlit application retrieves the data from MySQL and performs analysis using Pandas.

## 📈 Key Dashboard KPIs

The current dashboard displays:

- **Total Flights:** 300
- **Delayed Flights:** 57
- **Cancelled Flights:** 16
- **Delay Percentage:** 19.00%

These values are generated from the project database and may change when the underlying data changes.

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/rockeerocky337/Flight_Analytics_Project.git
