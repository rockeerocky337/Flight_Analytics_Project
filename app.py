import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, URL

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Air Tracker - Flight Analytics",
    page_icon="✈️",
    layout="wide"
)

# =========================================================
# MYSQL CONNECTION
# =========================================================

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )



# =========================================================
# LOAD DATA FROM MYSQL
# =========================================================

@st.cache_data
def load_data():

    connection = get_connection()

    flights = pd.read_sql_query(
        "SELECT * FROM flights",
        connection
    )

    airports = pd.read_sql_query(
        "SELECT * FROM airport",
        connection
    )

    aircraft = pd.read_sql_query(
        "SELECT * FROM aircraft",
        connection
    )

    delays = pd.read_sql_query(
        "SELECT * FROM airport_delays",
        connection
    )

    connection.dispose()

    return flights, airports, aircraft, delays


# =========================================================
# LOAD DATABASE
# =========================================================

try:

    flights, airports, aircraft, delays = load_data()

except Exception as e:

    st.error("Database connection failed.")
    st.error(str(e))
    st.stop()


# =========================================================
# HEADER
# =========================================================

st.title("✈️ Air Tracker - Flight Analytics")

st.write(
    "Interactive flight analytics dashboard powered by MySQL, "
    "Python, Pandas and Plotly."
)

st.success("MySQL database connected successfully!")


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Filters")

# Airline filter

airlines = sorted(flights["airline_code"].dropna().unique())

selected_airlines = st.sidebar.multiselect(
    "Airline",
    airlines,
    default=airlines
)

# Status filter

statuses = sorted(flights["status"].dropna().unique())

selected_status = st.sidebar.multiselect(
    "Flight Status",
    statuses,
    default=statuses
)

# Origin filter

origins = sorted(flights["origin_iata"].dropna().unique())

selected_origins = st.sidebar.multiselect(
    "Origin Airport",
    origins
)

# Destination filter

destinations = sorted(
    flights["destination_iata"].dropna().unique()
)

selected_destinations = st.sidebar.multiselect(
    "Destination Airport",
    destinations
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_flights = flights.copy()

if selected_airlines:

    filtered_flights = filtered_flights[
        filtered_flights["airline_code"].isin(selected_airlines)
    ]

if selected_status:

    filtered_flights = filtered_flights[
        filtered_flights["status"].isin(selected_status)
    ]

if selected_origins:

    filtered_flights = filtered_flights[
        filtered_flights["origin_iata"].isin(selected_origins)
    ]

if selected_destinations:

    filtered_flights = filtered_flights[
        filtered_flights["destination_iata"].isin(selected_destinations)
    ]


# =========================================================
# KPI SECTION
# =========================================================

st.subheader("📊 Flight Overview")

total_flights = len(filtered_flights)

delayed_flights = len(
    filtered_flights[
        filtered_flights["status"] == "Delayed"
    ]
)

cancelled_flights = len(
    filtered_flights[
        filtered_flights["status"].isin(
            ["Cancelled", "Canceled"]
        )
    ]
)

delay_percentage = (
    delayed_flights / total_flights * 100
    if total_flights > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "✈️ Total Flights",
        total_flights
    )

with col2:
    st.metric(
        "⏱️ Delayed Flights",
        delayed_flights
    )

with col3:
    st.metric(
        "❌ Cancelled Flights",
        cancelled_flights
    )

with col4:
    st.metric(
        "📈 Delay %",
        f"{delay_percentage:.2f}%"
    )


# =========================================================
# FLIGHT STATUS CHART
# =========================================================

st.subheader("🛫 Flight Status Analysis")

status_data = (
    filtered_flights
    .groupby("status")
    .size()
    .reset_index(name="flight_count")
)

fig_status = px.bar(
    status_data,
    x="status",
    y="flight_count",
    title="Flights by Status",
    labels={
        "status": "Flight Status",
        "flight_count": "Number of Flights"
    }
)

st.plotly_chart(
    fig_status,
    width="stretch"
)


# =========================================================
# AIRLINE ANALYSIS
# =========================================================

st.subheader("✈️ Airline Performance")

airline_data = (
    filtered_flights
    .groupby("airline_code")
    .size()
    .reset_index(name="flight_count")
    .sort_values(
        "flight_count",
        ascending=False
    )
)

fig_airline = px.bar(
    airline_data,
    x="airline_code",
    y="flight_count",
    title="Flights by Airline",
    labels={
        "airline_code": "Airline",
        "flight_count": "Number of Flights"
    }
)

st.plotly_chart(
    fig_airline,
    width="stretch"
)


# =========================================================
# TOP DESTINATION AIRPORTS
# =========================================================

st.subheader("🛬 Top Destination Airports")

destination_data = (
    filtered_flights
    .groupby("destination_iata")
    .size()
    .reset_index(name="arriving_flights")
    .sort_values(
        "arriving_flights",
        ascending=False
    )
    .head(10)
)

fig_destination = px.bar(
    destination_data,
    x="destination_iata",
    y="arriving_flights",
    title="Top 10 Destination Airports",
    labels={
        "destination_iata": "Airport",
        "arriving_flights": "Arriving Flights"
    }
)

st.plotly_chart(
    fig_destination,
    width="stretch"
)


# =========================================================
# AIRPORT DELAY ANALYSIS
# =========================================================

st.subheader("⏱️ Airport Delay Analysis")

delay_data = delays.copy()

delay_data = delay_data.sort_values(
    "avg_delay_min",
    ascending=False
)

fig_delay = px.bar(
    delay_data,
    x="airport_iata",
    y="avg_delay_min",
    title="Average Delay by Airport",
    labels={
        "airport_iata": "Airport",
        "avg_delay_min": "Average Delay (Minutes)"
    }
)

st.plotly_chart(
    fig_delay,
    width="stretch"
)


# =========================================================
# FLIGHT DATA TABLE
# =========================================================

st.subheader("📋 Flight Details")

display_columns = [
    "flight_id",
    "flight_number",
    "airline_code",
    "aircraft_registration",
    "origin_iata",
    "destination_iata",
    "scheduled_departure",
    "actual_departure",
    "status"
]

available_columns = [
    column
    for column in display_columns
    if column in filtered_flights.columns
]

st.dataframe(
    filtered_flights[available_columns],
    width="stretch",
    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Air Tracker Flight Analytics | "
    "MySQL + Python + Pandas + Streamlit + Plotly"
)