# Water Quality Data Engineering Pipeline

## Project Overview

This project implements a simple ETL (Extract, Transform, Load) data pipeline using the Environment Agency Hydrology API.

The pipeline retrieves the latest 10 readings for two water quality parameters from the station:

HIPPER_PARK ROAD BRIDGE_E_202312

The selected parameters are:
- Ammonium
- Temperature

The data is then transformed and stored in a structured SQLite database using a simple star schema design.

##  Architecture

The pipeline follows a standard ETL structure:

1. Extract  
   Retrieve the latest readings from the Hydrology API using measure IDs.

2. Transform  
   Clean and structure the data to retain only required fields:
   - Station Name
   - Parameter
   - Value
   - DateTime

3. Load  
   Store the processed data into a SQLite database.


## Data Source

Environment Agency Hydrology API

Base URL:
https://environment.data.gov.uk/hydrology/

Endpoint used:
https://environment.data.gov.uk/hydrology/data/readings.json

The API structure follows:

Station → Measures → Readings

Since readings are associated with measure IDs, the pipeline retrieves data using the specific measure identifiers.

## Database Design

The project uses SQLite as a lightweight relational database.

Two tables are created:

### 1️⃣ stations (Dimension Table)

| Column Name   | Type    |
|---------------|---------|
| station_id    | INTEGER |
| station_name  | TEXT    |

### 2️⃣ measurements (Fact Table)

| Column Name     | Type    |
|-----------------|---------|
| measurement_id  | INTEGER |
| station_id      | INTEGER |
| parameter       | TEXT    |
| value           | REAL    |
| datetime        | TEXT    |

A foreign key relationship links measurements to stations.

This design follows a simple star schema approach.

## Technologies Used

- Python 3
- Requests (API calls)
- SQLite (Database)
- Pandas (optional – for viewing data)

