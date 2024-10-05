import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set up folder for file uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.title("Data Visualization App")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    # Save the uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Read the Excel file
    df = pd.read_excel(filepath)
    st.write("### Preview of the Dataset", df)

    # Select columns for the chart
    selected_columns = st.multiselect("Select Columns to Visualize", df.columns.tolist(), default=df.columns.tolist())

    # Select chart types
    chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])

    # If columns are selected, generate the chart
    if selected_columns:
        st.write(f"### {chart_type} for selected columns")

        fig, ax = plt.subplots()

        if chart_type == 'Bar Chart':
            df[selected_columns].plot(kind='bar', ax=ax)
        elif chart_type == 'Line Chart':
            df[selected_columns].plot(kind='line', ax=ax)
        elif chart_type == 'Scatter Plot':
            if len(selected_columns) == 2:
                df.plot(kind='scatter', x=selected_columns[0], y=selected_columns[1], ax=ax)
            else:
                st.error("Scatter plot requires exactly two columns.")

        st.pyplot(fig)

        # Display insights or analysis
        st.write("### Insights:")
        st.write(f"- Total number of rows: {df.shape[0]}")
        st.write(f"- Total number of columns: {df.shape[1]}")
        st.write(f"- Basic statistics for selected columns:")
        st.write(df[selected_columns].describe())


