import requests
import sqlite3

# STEP 1: FETCH READINGS

def fetch_readings(measure_id, limit=10):
    url = "https://environment.data.gov.uk/hydrology/data/readings.json"

    params = {
        "measure": measure_id,
        "_limit": limit
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching data:", response.status_code)
        return []

    data = response.json()
    return data.get("items", [])

# STEP 2: TRANSFORM DATA

def transform_data(raw_data, parameter_name):
    cleaned = []

    for item in raw_data:
        record = {
            "station": "HIPPER_PARK ROAD BRIDGE_E_202312",
            "parameter": parameter_name,
            "value": item.get("value"),
            "datetime": item.get("dateTime")
        }
        cleaned.append(record)

    return cleaned

# STEP 3: CREATE DATABASE

def create_database():
    conn = sqlite3.connect("hydrology.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stations (
            station_id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_name TEXT UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id INTEGER,
            parameter TEXT,
            value REAL,
            datetime TEXT,
            FOREIGN KEY (station_id) REFERENCES stations(station_id)
        )
    """)

    conn.commit()
    return conn

# STEP 4: LOAD DATA

def load_data(conn, records):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO stations (station_name)
        VALUES (?)
    """, ("HIPPER_PARK ROAD BRIDGE_E_202312",))

    cursor.execute("""
        SELECT station_id FROM stations
        WHERE station_name = ?
    """, ("HIPPER_PARK ROAD BRIDGE_E_202312",))

    station_id = cursor.fetchone()[0]

    for record in records:
        cursor.execute("""
            INSERT INTO measurements (station_id, parameter, value, datetime)
            VALUES (?, ?, ?, ?)
        """, (
            station_id,
            record["parameter"],
            record["value"],
            record["datetime"]
        ))

    conn.commit()

# MAIN FUNCTION

def main():

    ammonium_measure = "E64999A-amm-i-subdaily-mgL"
    temperature_measure = "E64999A-temp-i-subdaily-C"

    ammonium_raw = fetch_readings(ammonium_measure)
    temperature_raw = fetch_readings(temperature_measure)

    ammonium_clean = transform_data(ammonium_raw, "AMMONIUM")
    temperature_clean = transform_data(temperature_raw, "TEMPERATURE")

    all_records = ammonium_clean + temperature_clean

    conn = create_database()
    load_data(conn, all_records)
    conn.close()

    print("Pipeline completed successfully!")
    print("Total records inserted:", len(all_records))


if __name__ == "__main__":
    main()