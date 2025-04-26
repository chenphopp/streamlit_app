import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.write("---")

# --- Plotly Chart: Number of pickups by hour ---
st.subheader('Number of pickups by hour (Plotly Chart)')
hist_df = pd.DataFrame({
    'hour': range(24),
    'pickups': np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
})
fig = px.bar(hist_df, x='hour', y='pickups', labels={'hour': 'Hour of day', 'pickups': 'Number of pickups'}, title='Number of pickups by hour')
st.plotly_chart(fig)

st.write("---")

# --- Date input ---
st.subheader("Filter by date")
selected_date = st.date_input("Choose a date", value=data[DATE_COLUMN].dt.date.iloc[0])

# Filter data by selected date
filtered_data_by_date = data[data[DATE_COLUMN].dt.date == selected_date]

# --- Hour slider ---
st.subheader("Filter by hour")
hour_to_filter = st.slider('Select hour', 0, 23, 17)

# Further filter by selected hour
filtered_data = filtered_data_by_date[filtered_data_by_date[DATE_COLUMN].dt.hour == hour_to_filter]

st.write("---")

# --- 2D Map ---
st.subheader('2D Map of pickups on %s at %s:00' % (selected_date, hour_to_filter))
if not filtered_data.empty:
    st.map(filtered_data)
else:
    st.warning("No data available for this date and hour.")

st.write("---")

# --- 3D Map with PyDeck ---
st.subheader('3D Map of pickups on %s at %s:00' % (selected_date, hour_to_filter))
if not filtered_data.empty:
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=filtered_data['lat'].mean(),
            longitude=filtered_data['lon'].mean(),
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=filtered_data,
                get_position='[lon, lat]',
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            )
        ]
    ))
else:
    st.warning("No data available for this date and hour.")

st.write("---")

# --- Button to increase page run counter ---
st.subheader("Page Run Counter")

# Initialize counter
if 'count' not in st.session_state:
    st.session_state.count = 0

# Button click increases counter
if st.button('Click to increase counter'):
    st.session_state.count += 1

st.success(f"This page has run {st.session_state.count} times.")
