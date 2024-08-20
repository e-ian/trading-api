from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import pandas as pd
import os
from .config import Config

api_blueprint = Blueprint('forex_tickers', __name__)

@api_blueprint.route('/ticker_data', methods=['POST'])
def get_ticker_data():
    req_data = request.get_json()

    # Extract and validate request data
    time_str = req_data.get('time')
    ticker = req_data.get('ticker')

    if not time_str:
        return jsonify({'error': 'time is required'}), 400
    if not ticker:
        return jsonify({'error': 'ticker is required'}), 400

    try:
        # Parse the time in RFC 3339 format
        time = datetime.fromisoformat(time_str.rstrip('Z'))
        date = time.date()
        time_period = time.time()

        # Construct file path based on the ticker and date
        file_date_str = date.strftime('%d.%m.%Y')
        folder_name = f"{ticker}=X"
        file_name = f"{file_date_str}_5m.csv"
        file_path = os.path.join(Config.DATA_PATH, folder_name, file_name)
        print('filee', file_path)

        if not os.path.isfile(file_path):
            return jsonify({'error': f'No data file found for ticker {ticker} and date {date.strftime("%d-%m-%Y")}'}) , 404

        # Read and process the CSV file
        df = pd.read_csv(file_path)

        if 'Datetime' not in df.columns:
            return jsonify({'error': 'The CSV file does not contain a "Datetime" column'}), 500

        df['Datetime'] = pd.to_datetime(df['Datetime'], format='%d.%m.%Y %H:%M:%S.%f')

        search_time = datetime.combine(date, time_period)
        previous_minute = search_time - timedelta(minutes=5)

        filtered_df = df[(df['Datetime'] >= previous_minute) & (df['Datetime'] < search_time)]

        if filtered_df.empty:
            return jsonify({'error': 'No data available for the given date and time period'}), 404
        
        # If there's exactly one record, return it as a JSON object
        if len(filtered_df) == 1:
            result = filtered_df.iloc[0].to_dict()
            return jsonify(result)

        result = filtered_df.to_dict(orient='records')
        return jsonify(result)

    except ValueError:
        return jsonify({'error': 'Invalid time format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
