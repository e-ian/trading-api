from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
import pandas as pd
from .config import Config

api_blueprint = Blueprint('forex_tickers', __name__)

# Load CSV data
df = pd.read_csv(Config.DATA_PATH, parse_dates=['Datetime'])

@api_blueprint.route('/ticker_data', methods=['POST'])
def get_ticker_data():
    req_data = request.get_json()
    date_str = req_data.get('date')
    time_period = req_data.get('time_period')

    if not time_period:
        return jsonify({'error': 'time_period is required'}), 400

    try:
        if date_str:
            date = datetime.strptime(date_str, '%d.%m.%Y').date()
            session['date'] = date_str
        else:
            if 'date' in session:
                date = datetime.strptime(session['date'], '%d.%m.%Y').date()
            else:
                date = datetime.now().date()

        time_period = datetime.strptime(time_period, '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Invalid date or time format'}), 400

    # Combine date and time to get the search time
    search_time = datetime.combine(date, time_period)
    previous_minute = search_time - timedelta(minutes=5)

    # Filter data to get the minute preceding the requested time period
    filtered_df = df[(df['Datetime'] >= previous_minute) & (df['Datetime'] < search_time)]

    if filtered_df.empty:
        return jsonify({'error': 'No data available for the given date and time period'}), 404

    result = filtered_df.to_dict(orient='records')
    
    return jsonify(result)
