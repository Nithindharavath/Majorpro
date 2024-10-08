import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set up folder for file uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # This creates the uploads folder if it doesn't exist

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

    # Display a preview of the dataset
    st.write("### Preview of the Dataset")
    st.dataframe(df)  # This will show the dataset in an interactive table

    # Select chart type
    chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram"])

    # Initialize selected_columns and selected_column to avoid NameError
    selected_columns = []
    selected_column = ""

    # Select columns for the chart based on chart type
    if chart_type == 'Pie Chart':
        # For Pie Chart, select only one column (must be categorical)
        selected_column = st.selectbox("Select Column for Pie Chart", df.columns.tolist())
    else:
        # Filter numeric columns for charts that require numerical data
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

        if not numeric_columns:
            st.error("No numeric columns found in the dataset. Please upload a dataset with numeric data.")
        else:
            selected_columns = st.multiselect("Select Columns for Visualization", numeric_columns)

    # Generate the selected chart
    if chart_type != 'Pie Chart' and selected_columns:
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
                st.error("Scatter plot requires exactly two numeric columns.")
        elif chart_type == 'Histogram':
            df[selected_columns].plot(kind='hist', ax=ax, bins=10)

        st.pyplot(fig)

    elif chart_type == 'Pie Chart':
        # Generate Pie Chart for one selected categorical column
        if selected_column:
            df[selected_column].value_counts().plot(kind='pie', ax=plt.gca(), autopct='%1.1f%%')
            st.pyplot(plt)

    # Display insights or analysis
    st.write("### Insights:")
    st.write(f"- Total number of rows: {df.shape[0]}")
    st.write(f"- Total number of columns: {df.shape[1]}")
    st.write(f"- Basic statistics for selected numeric columns:")
    if chart_type != 'Pie Chart' and selected_columns:
        st.write(df[selected_columns].describe())




