# Import the dependencies.

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,desc

from flask import Flask, jsonify

import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine )

# Save references to each table
#print(Base.classes.keys())
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
#session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# To avoid jsonify() sorting the keys
app.config['JSON_SORT_KEYS'] = False


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """ List of available API Routes: """
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<startdate><br/>"
        f"/api/v1.0/<startdate>/<enddate><br/>"        
    )

# Function to calculate last year date
def previous_year_date():
    
    # Calculate the date one year from the last date in data set.
    last_year_date = str(dt.date(2017,8,23) - dt.timedelta(days=365))

    return last_year_date


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    last_year_date = previous_year_date()

    # Retrieve the data and precipitation scores for the last year.
    last_month_data = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= last_year_date).all()
    
    # Close the session
    session.close()

    # Create a dictionary from the query results
    last_month_data_list=[]
    for each_date,prcp in last_month_data:
        data_dict = {}
        data_dict[each_date] = prcp

        # Create a list dictionaries        
        last_month_data_list.append(data_dict)

    # Return jsonified result
    return jsonify(last_month_data_list)


@app.route("/api/v1.0/stations")
def stations():

    # Create the session link
    session = Session(engine)

    # Get the details of all the stations
    station_data = session.query(Station.station, Station.name,Station.latitude, Station.longitude,Station.elevation).all()
       
    # Close the session
    session.close()

    # Create a dictionary from the query results
    station_data_list=[]
    for station,name,latitude,longitude,elevation in station_data:
        data_dict = {}
        data_dict["station"] = station
        data_dict["name"] = name
        data_dict["latitude"] = latitude
        data_dict["longitude"] = longitude
        data_dict["elevation"] = elevation

        # Create a list dictionaries
        station_data_list.append(data_dict)
    
    # Return jsonified result
    return jsonify(station_data_list)


@app.route("/api/v1.0/tobs")
def temp_Observ():

    # Create the session link
    session = Session(engine)

    # Get the most-active station (i.e. which stations have the most rows)
    most_active_station = session.query(Station.station).\
                    filter(Measurement.station==Station.station).\
                    group_by(Station.station).\
                    order_by(func.count(Measurement.station).desc()).first()
    
    most_active_station_id = str(most_active_station)[2:-3]
    
    # Calculate the date one year from the last date in data set.
    last_year_date = previous_year_date()

    # Get the dates and temperature observations of the most-active station for the previous year of data
    tobs_data = session.query(Measurement.station, Measurement.date,Measurement.tobs).\
                filter(Measurement.station == most_active_station_id).\
                filter(Measurement.date >= last_year_date ).all()

       
    # Close the session
    session.close()

    # Create a dictionary from the query results
    tobs_data_list=[]
    for station,date,tobs in tobs_data:
        data_dict = {}
        data_dict["station"] = station
        data_dict["date"] = date
        data_dict["tobs"] = tobs

        # Create a list dictionaries
        tobs_data_list.append(data_dict)
    
    # Return jsonified result
    return jsonify(tobs_data_list)
    
	

if __name__ == "__main__":
    app.run(debug=True)
