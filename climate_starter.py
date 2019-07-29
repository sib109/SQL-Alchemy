
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

# Home
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<start><br/>"
        f"/api/v1.0/start_date<start>/end_date<end><br/>"
    )


# Prcp
@app.route("/api/v1.0/precipitation")
def precipitation():

    prcp_data = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date).all()
    prcp = {i[0]:i[1] for i in prcp_data}
    session.close()
    return jsonify(prcp)


# Station
@app.route("/api/v1.0/stations")
def stations():

    station_data = session.query(Station.station, Station.name).all()
   # stations = [i[0] for i in station_data]
    session.close()
    return jsonify(station_data)


# Tobs
@app.route("/api/v1.0/tobs")
def tobs():

    maxdate = session.query(func.max(Measurement.date)).all()
    max_date = dt.datetime.strptime(maxdate[0][0], '%Y-%m-%d')

    max_minus_year = max_date - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.date >= max_minus_year).order_by(Measurement.date.desc()).all()

    tobs_data = {i[0]:i[1] for i in results}

    return jsonify(tobs_data)


if __name__ == '__main__':
    app.run(debug=True)
