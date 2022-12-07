import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>='2016-08-23').group_by(Measurement.date).order_by(Measurement.date).all()

    session.close()

    prec_list = []
    for date, prcp in results:
        prec_dict = {}
        prec_dict['date'] = date
        prec_dict['prcp'] = prcp
        prec_list.append(prec_dict)

    return jsonify(prec_list)

@app.route("/api/v1.0/stations")
def stations ():
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    station_list = []
    for station in results:
        station_list.append(station)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>='2016-08-23').filter(Station.station == Measurement.station).filter(Station.name == 'WAIHEE 837.5, HI US').all()

    session.close()

    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs 
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def StartDate(start):
    session = Session(engine)

    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()

    session.close()

    start_list = []
    for date,tmin,tmax,tavg in results:
        start_dict = {}
        start_dict['Date'] = date
        start_dict['TMIN'] = tmin
        start_dict['TMAX'] = tmax
        start_dict['TAVG'] = tavg
        start_list.append(start_dict)

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def StartDateEndDate(start,end):
    session = Session(engine)

    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date<=end).group_by(Measurement.date).all()

    session.close()

    startend_list = []
    for date,tmin,tmax,tavg in results:
        startend_dict = {}
        startend_dict['Date'] = date
        startend_dict['TMIN'] = tmin
        startend_dict['TMAX'] = tmax
        startend_dict['TAVG'] = tavg
        startend_list.append(startend_dict)

    return jsonify(startend_list)

if __name__ == '__main__':
    app.run(debug=True)