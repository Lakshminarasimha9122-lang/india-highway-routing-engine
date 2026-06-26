from flask import Flask, render_template, jsonify, request
import sqlite3
import datetime

app = Flask(__name__)


# Initialize a lightweight local SQLite database to log real-time travel history
def init_db():
    conn = sqlite3.connect('route_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            origin TEXT,
            destination TEXT,
            distance TEXT,
            duration TEXT,
            toll_cost TEXT,
            vehicle TEXT
        )
    ''')
    conn.commit()
    conn.close()


init_db()


@app.route('/')
def home():
    # Serves your Leaflet.js interactive map frontend dashboard interface cleanly
    return render_template('index.html')


@app.route('/api/log_trip', methods=['POST'])
def log_trip():
    try:
        data = request.json
        conn = sqlite3.connect('route_history.db')
        cursor = conn.cursor()

        # Insert precision telemetry packet directly into SQL tables index rows
        cursor.execute('''
            INSERT INTO trips (timestamp, origin, destination, distance, duration, toll_cost, vehicle)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get('origin'),
            data.get('destination'),
            data.get('distance'),
            data.get('duration'),
            data.get('toll_cost'),
            data.get('vehicle')
        ))

        conn.commit()
        conn.close()
        return jsonify({"status": "Success", "message": "Log metrics written successfully to database index."}), 201
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 400


@app.route('/api/get_history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('route_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM trips ORDER BY id DESC LIMIT 10')
    rows = cursor.fetchall()
    conn.close()

    # Restructure SQL matrix back into a clean transit JSON payload object array
    history_logs = []
    for row in rows:
        history_logs.append({
            "id": row[0], "time": row[1], "origin": row[2], "destination": row[3],
            "distance": row[4], "duration": row[5], "tolls": row[6], "vehicle": row[7]
        })
    return jsonify(history_logs)


if __name__ == '__main__':
    # Spins up the internal PyCharm deployment loop running locally on port 5000
    app.run(debug=True, port=5000)