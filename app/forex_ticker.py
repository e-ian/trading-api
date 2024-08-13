from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
import pandas as pd
from .config import Config
import os

api_blueprint = Blueprint('forex_tickers', __name__)

# DATA_FOLDER = 'data/EURUSD=X'


@api_blueprint.route('/ticker_data', methods=['POST'])
def get_ticker_data():
    req_data = request.get_json()
    date_str = req_data.get('date')
    time_period_str = req_data.get('time_period')

    if not time_period_str:
        return jsonify({'error': 'time_period is required'}), 400

    try:
        # Parse date and time_period
        if date_str:
            # Interpret the date as day.month.year
            date = datetime.strptime(date_str, '%d.%m.%Y').date()
            session['date'] = date_str
        else:
            if 'date' in session:
                date = datetime.strptime(session['date'], '%d.%m.%Y').date()
            else:
                date = datetime.now().date()

        # Convert time_period to datetime.time
        time_period = datetime.strptime(time_period_str, '%H:%M').time()
        
    except ValueError:
        return jsonify({'error': 'Invalid date or time format'}), 400

    # Construct the filename based on the date only
    file_name = f"{date.strftime('%d.%m.%Y')}_5m.csv"
    file_path = os.path.join(Config.DATA_PATH, file_name)

    if not os.path.isfile(file_path):
        return jsonify({'error': f'No data file found for {date_str}'}), 404

    try:
        df = pd.read_csv(file_path)

        if 'Datetime' not in df.columns:
            return jsonify({'error': 'The CSV file does not contain a "Datetime" column'}), 500

        df['Datetime'] = pd.to_datetime(df['Datetime'], format='%d.%m.%Y %H:%M:%S.%f')

        search_time = datetime.combine(date, time_period)
        previous_minute = search_time - timedelta(minutes=5)

        filtered_df = df[(df['Datetime'] >= previous_minute) & (df['Datetime'] < search_time)]

        if filtered_df.empty:
            return jsonify({'error': 'No data available for the given date and time period'}), 404

        result = filtered_df.to_dict(orient='records')
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500