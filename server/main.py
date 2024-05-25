from flask import Flask, jsonify, request
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/run-script', methods=['GET'])
def get_fare():
    try:
        fare_type = {
            "0": "Adult card fare",
            "1": "Senior citizen card fare",
            "2": "Student card fare",
            "3": "Workfare transport concession card fare",
            "4": "Persons with disabilities card fare"
        }

        # Get query parameters
        fare_type_key = request.args.get('type')
        distance = request.args.get('distance')

        if fare_type_key not in fare_type or not distance:
            return jsonify({"error": "Invalid type or distance parameter"}), 400
        
        distance = float(distance)

        # Read the CSV file
        dataset_path = os.path.join(os.path.dirname(__file__), '../dataset/Fares_cleaned.csv')
        df = pd.read_csv(dataset_path)
        df = df[df['fare_type'] == fare_type[fare_type_key]]

        # Check max distance
        if distance >= float(df.iloc[-1]['distance']):
            fare = df.iloc[-1]['fare_per_ride']
            return jsonify({"fare_per_ride": float(fare)})

        # Iterate for fare range
        for index, row in df.iterrows():
            if distance < float(row['distance']):
                fare = df.iloc[index - 1]['fare_per_ride']
                return jsonify({"fare_per_ride": float(fare)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
