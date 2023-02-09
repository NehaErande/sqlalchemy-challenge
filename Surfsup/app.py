import numpy as np
import pandas as pd
import datetime as dt
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    "List of available api routes."
    return (
         f"Available Routes for Hawaii Weather Data:<br/><br>"
        f"-- Daily Precipitation Totals for Last Year: <a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation<a><br/>"
        f"-- Active Weather Stations: <a href=\"/api/v1.0/stations\">/api/v1.0/stations<a><br/>"
        f"-- Daily Temperature Observations for Station USC00519281 for Last Year: <a href=\"/api/v1.0/tobs\">/api/v1.0/tobs<a><br/>"
        f"-- Min, Average & Max Temperatures for Date Range: /api/v1.0/trip/yyyy-mm-dd/yyyy-mm-dd<br>"
        f"NOTE: If no end-date is provided, the trip api calculates stats through 08/23/17<br>" 
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year).all()

    session.close()
    # Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return JSON list of all stations"""
    sel = [Measurement.station]   
    station = session.query(*sel).group_by(Measurement.station).all()
    session.close()
    list_of_stations = list(np.ravel(station)) 
    return jsonify(list_of_stations)
  

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    sel = [Measurement.date, Measurement.tobs]
# Get last 12 months of temprature data for the most active station
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    active_station_temp = session.query(*sel).\
                    filter(func.strftime(Measurement.date) >= one_year, Measurement.station == 'USC00519281').\
                    group_by(Measurement.date).\
                    order_by(Measurement.date).all()
    session.close()

    # Creating dictionary with date and temprature observations
    observation_dates = []
    temperature_observations = []

    for date, observation in active_station_temp:
        observation_dates.append(date)
        temperature_observations.append(observation)
    """Return date and temprature observations for most active station"""
    most_active_tobs_dict = dict(zip(observation_dates, temperature_observations))

    return jsonify(most_active_tobs_dict)


if __name__ == "__main__":
    app.run(debug=True)    



