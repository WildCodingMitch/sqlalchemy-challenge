#################################################
# Import the dependencies.
#################################################
from matplotlib import style
style.use("fivethirtyeight")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """All Available Routes: """
    return (
        f"Welcome to the Module 10 Challenge API<br/>"
        f"--------------------------------------<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/end_date <br/>"
    )
#################################################

#################################################
@app.route("/api/v1.0/precipitation")

def precipitation():
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days= 365)

    precipitation_scores = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago, measurement.prcp != None).\
                           order_by(measurement.date).all()
    
    return jsonify(dict(precipitation_scores))
#################################################

#################################################
@app.route("/api/v1.0/stations")

def stations():
    session.query(measurement.station).distinct().count()
    active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).\
                      order_by(func.count(measurement.station).desc()).all()
    
    return jsonify(dict(active_stations))

#################################################

#################################################
@app.route("/api/v1.0/tobs")

def tobs():
    tobs = session.query(measurement.tobs).filter(measurement.station == "USC00519281" ).filter(measurement.date >= "2017,8,23").all()
    tobs_list = list(np.ravel(tobs))
    return jsonify (tobs_list)
#################################################

#################################################
#@app.route("/api/v1.0/<start>")
    
### def start_date(start):
    calculate_temp = start_calculation(start)
    temp_list = list(np.ravel(calculate_temp))

    temp_min = temp_list[0]
    temp_avg = temp_list[1]
    temp_max = temp_list[2]
    start_temperature_dict = {"Minimum temperature": temp_min, "Maximum temperature": temp_max, "Avg temperature": temp_avg}

    return jsonify(start_temperature_dict)
###
def start_calculation(start_date, end_date):
    return session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                         filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
#################################################

#################################################
@app.route("/api/v1.0/start_date/end_date")

def start_end_date(start, end):
    
    calculate_temp = end_calculation(start, end)
    temp_list= list(np.ravel(calculate_temp))

    temp_min = temp_list[0]
    temp_avg = temp_list[1]
    temp_max = temp_list[2]
    end_temperature_dict = { "Minimum temperature": temp_min, "Maximum temperature": temp_max, "Avg temperature": temp_avg}

    return jsonify(end_temperature_dict)

def end_calculation(start_date, end_date):
    return session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                         filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
#################################################

#################################################

if __name__ == "__main__":
   app.run(debug=True)

