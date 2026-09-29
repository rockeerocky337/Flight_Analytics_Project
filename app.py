import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

st.set_page_config(page_title="Air Tracker - Flight Analytics", page_icon="✈️", layout="wide")

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
    )

@st.cache_data
def load_data():
    connection = get_connection()
    try:
        flights = pd.read_sql("SELECT * FROM flights", connection)
        airports = pd.read_sql("SELECT * FROM airport", connection)
        aircraft = pd.read_sql("SELECT * FROM aircraft", connection)
        delays = pd.read_sql("SELECT * FROM airport_delays", connection)
        return flights, airports, aircraft, delays
    finally:
        connection.close()

try:
    flights, airports, aircraft, delays = load_data()
except Exception as e:
    st.error("Database connection failed. Check MySQL and .streamlit/secrets.toml.")
    st.code(str(e))
    st.stop()

st.title("✈️ Air Tracker - Flight Analytics")
st.caption("MySQL + Python + Pandas + Plotly + Streamlit")

st.sidebar.header("🔎 Filters")

def options(column):
    return sorted(flights[column].dropna().astype(str).unique().tolist())

airlines = options("airline_code")
statuses = options("status")
origins = options("origin_iata")
destinations = options("destination_iata")

selected_airlines = st.sidebar.multiselect("Airline", airlines, default=airlines)
selected_status = st.sidebar.multiselect("Flight Status", statuses, default=statuses)
selected_origins = st.sidebar.multiselect("Origin Airport", origins)
selected_destinations = st.sidebar.multiselect("Destination Airport", destinations)

filtered = flights.copy()
if selected_airlines:
    filtered = filtered[filtered["airline_code"].isin(selected_airlines)]
if selected_status:
    filtered = filtered[filtered["status"].isin(selected_status)]
if selected_origins:
    filtered = filtered[filtered["origin_iata"].isin(selected_origins)]
if selected_destinations:
    filtered = filtered[filtered["destination_iata"].isin(selected_destinations)]

total = len(filtered)
delayed = int((filtered["status"] == "Delayed").sum())
cancelled = int(filtered["status"].isin({"Cancelled", "Canceled"}).sum())
delay_pct = delayed / total * 100 if total else 0

st.subheader("📊 Flight Overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("✈️ Total Flights", total)
c2.metric("⏱️ Delayed Flights", delayed)
c3.metric("❌ Cancelled Flights", cancelled)
c4.metric("📈 Delay %", f"{delay_pct:.2f}%")

st.subheader("🛫 Flight Status Analysis")
status_data = filtered.groupby("status").size().reset_index(name="flight_count")
st.plotly_chart(px.bar(status_data, x="status", y="flight_count", title="Flights by Status"), use_container_width=True)

st.subheader("✈️ Airline Performance")
airline_data = filtered.groupby("airline_code").size().reset_index(name="flight_count").sort_values("flight_count", ascending=False)
st.plotly_chart(px.bar(airline_data, x="airline_code", y="flight_count", title="Flights by Airline"), use_container_width=True)

st.subheader("🛬 Top Destination Airports")
destination_data = filtered.groupby("destination_iata").size().reset_index(name="arriving_flights").sort_values("arriving_flights", ascending=False).head(10)
st.plotly_chart(px.bar(destination_data, x="destination_iata", y="arriving_flights", title="Top 10 Destination Airports"), use_container_width=True)

st.subheader("⏱️ Airport Delay Analysis")
delay_data = delays.sort_values("avg_delay_min", ascending=False)
st.plotly_chart(px.bar(delay_data, x="airport_iata", y="avg_delay_min", title="Average Delay by Airport"), use_container_width=True)

st.subheader("📋 Flight Details")
display_columns = ["flight_id", "flight_number", "airline_code", "aircraft_registration", "origin_iata", "destination_iata", "scheduled_departure", "actual_departure", "status"]
available = [c for c in display_columns if c in filtered.columns]
st.dataframe(filtered[available], use_container_width=True, hide_index=True)

st.divider()
st.caption("Air Tracker Flight Analytics | Recovered and corrected project")
