# Dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Set up database engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create a variable for each class
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to database
session = Session(engine)

# Define flask app
app = Flask(__name__)

# Define welcome route
@app.route("/")

# Create function for routing information
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Define precipitation route
@app.route("/api/v1.0/precipitation")

# Create precipitation function
def precipitation():
    # Calculate date one year ago from date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query for date/precipitation for previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    # Use jsonify() to romat results into JSON structured file (dictionary)
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Define station route
@app.route("/api/v1.0/stations")

# Create station function
def stations():
    # Collect all stations
    results = session.query(Station.station).all()
    # Unravel results into one-dimensional array, then a list, then jsonify
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Define temperature route
@app.route("/api/v1.0/tobs")

# Create temp function
def temp_monthly():
    # Calculate date one year ago from date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query primary station for all temps from previous year
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    # Unravel results into one-dimensional array, then a list
    temps = list(np.ravel(results))
    # jsonify results
    return jsonify(temps=temps)

# Define status route
@app.route("/api.v1.0/temp/<start>")
@app.route("/api.v1.0/temp/<start>/<end>")

# Create stats function including start and end parameters
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)