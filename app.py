# Import the dependencies.

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

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
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
#session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# To retain the order of keys in the dictionary passed to jsonify (to avoid jsonify() sorting the keys)
app.config['JSON_SORT_KEYS'] = False


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """ List of available API Routes: """
    return (
        f"<b>Available Routes: </b><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2010-01-26<br/>"        
        f"/api/v1.0/2010-01-26/2015-03-24<br/>"        
        f"<b>Note: Date format must be: yyyy-mm-dd </b><br/>"
    )

# Function to calculate previous year date
def previous_year_date():
    
    # Create session
    session = Session(engine)

    # Get the last/most recent date from the data
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    # Close session
    session.close()

    # From the recent date, get year, month and date separately 
    latest_date  = str(recent_date)
    r_year = int(latest_date[2:6])
    r_month = int(latest_date[7:9])
    r_date = int(latest_date[10:12])

    # Calculate the date one year from the last/most recent date in data set.
    last_year_date = str(dt.date(r_year,r_month,r_date) - dt.timedelta(days=365))

    return last_year_date


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Calculate the date one year from the last date in data set.
    last_year_date = previous_year_date()

    # Create our session (link) from Python to the DB
    session = Session(engine)

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
        data_dict["Station ID"] = station
        data_dict["Station Name"] = name
        data_dict["Latitude"] = latitude
        data_dict["Longitude"] = longitude
        data_dict["Elevation"] = elevation

        # Create a list dictionaries
        station_data_list.append(data_dict)
    
    # Return jsonified result
    return jsonify(station_data_list)


@app.route("/api/v1.0/tobs")
def temp_Observ():

    # Calculate the date one year from the last date in data set.
    last_year_date = previous_year_date()

    # Create the session link
    session = Session(engine)

    # Get the most-active station (i.e. which stations have the most rows)
    most_active_station = session.query(Station.station).\
                    filter(Measurement.station==Station.station).\
                    group_by(Station.station).\
                    order_by(func.count(Measurement.station).desc()).first()
    
    print(most_active_station)
    # Remove the extra characters and get the ID from the result
    most_active_station_id = str(most_active_station)[2:-3]    

    # Get the dates and temperature observations of the most-active station for the previous year
    tobs_data = session.query(Measurement.station, Measurement.date,Measurement.tobs).\
                filter(Measurement.station == most_active_station_id).\
                filter(Measurement.date >= last_year_date ).all()

       
    # Close the session
    session.close()

    # Create a dictionary from the query results
    tobs_data_list=[]
    for station,date,tobs in tobs_data:
        data_dict = {}
        data_dict["Station ID"] = station
        data_dict["Date"] = date
        data_dict["Observed temperature"] = tobs

        # Create a list dictionaries
        tobs_data_list.append(data_dict)
    
    # Return jsonified result
    return jsonify(tobs_data_list)
    
	
@app.route("/api/v1.0/<startdate>")
def temp_calc_start_date(startdate):    

    # Create session
    session = Session(engine)

    # Calculate MIN, MAX, AVG temperature for all the dates greater than or equal to the start date
    sel = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    temp_data = session.query(*sel).\
                filter(Measurement.date >= startdate).all()
        
    # Close the session
    session.close()    

    # unpack the values and set in a dictionary
    min_temp, max_temp, avg_temp = temp_data[0]
    temp_data_dict = {}
    if (min_temp is None) and (max_temp is None) and (avg_temp is None):
        return jsonify({ "Error": f"No data found for startdate {startdate}"}),404
    else:               
        temp_data_dict['Minimum temperature'] = min_temp
        temp_data_dict['Maximum temperature'] = max_temp
        temp_data_dict['Average temperature'] = round(avg_temp,2)
        return jsonify(temp_data_dict)


@app.route("/api/v1.0/<startdate>/<enddate>")
def temp_calc_start_end_date(startdate, enddate):    

    # Create session
    session = Session(engine)

    # Calculate MIN, MAX, AVG temperature for the dates from the start date to the end date, inclusive
    sel = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    temperature_data = session.query(*sel).\
                filter(Measurement.date >= startdate).\
                filter(Measurement.date <= enddate).all()
    
    # Close the session
    session.close()
        
    # unpack the values and set in a dictionary
    min_temp, max_temp, avg_temp = temperature_data[0]
    temperature_data_dict = {}
    if (min_temp is None) and (max_temp is None) and (avg_temp is None):
        return jsonify({ "Error": f"No data found for startdate {startdate} and enddate {enddate}"}),404
    else:        
        temperature_data_dict['Minimum temperature'] = min_temp
        temperature_data_dict['Maximum temperature'] = max_temp
        temperature_data_dict['Average temperature'] = round(avg_temp,2)
        return jsonify(temperature_data_dict)


if __name__ == "__main__":
    app.run(debug=True)
