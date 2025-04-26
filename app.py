import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("My First Streamlit App")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    # Read the file
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data")
    st.write(df)

    # Select columns to plot
    column = st.selectbox("Select a column to visualize", df.columns)

    st.subheader(f"Histogram of {column}")
    fig = px.histogram(df, x=column)
    st.plotly_chart(fig)
else:
    st.info("Please upload a CSV file to get started.")
