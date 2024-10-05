from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import BytesIO
import base64

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.xlsx'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('select_charts', filename=file.filename))
    return 'Invalid file type. Only .xlsx files are allowed.'

@app.route('/charts/<filename>', methods=['GET', 'POST'])
def select_charts(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if request.method == 'POST':
        df = pd.read_excel(filepath)
        chart_types = request.form.getlist('chart_types')
        selected_columns = request.form.getlist('columns')

        if not selected_columns:
            selected_columns = df.columns  # Default to all columns if none selected
        
        charts = generate_charts(df, chart_types, selected_columns)
        return render_template('charts.html', charts=charts)
    
    # Display form to select chart types and fields
    df = pd.read_excel(filepath)
    columns = df.columns
    return render_template('chart_select.html', columns=columns)

def generate_charts(df, chart_types, selected_columns):
    charts = []
    for chart_type in chart_types:
        fig, ax = plt.subplots()
        if chart_type == 'bar':
            df[selected_columns].plot(kind='bar', ax=ax)
        elif chart_type == 'line':
            df[selected_columns].plot(kind='line', ax=ax)
        elif chart_type == 'scatter':
            if len(selected_columns) == 2:
                df.plot(kind='scatter', x=selected_columns[0], y=selected_columns[1], ax=ax)
        
        # Save plot to base64
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        charts.append(chart_data)
        plt.close(fig)
    
    return charts

if __name__ == '__main__':
    app.run(debug=True)

