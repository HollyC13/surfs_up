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
Base = automap_base
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
    /api/v1.0/preciptiation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Create precipitation route
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