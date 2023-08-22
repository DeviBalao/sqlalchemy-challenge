# sqlalchemy-challenge

This challenge has 2 parts:
### Part 1: Analyze and Explore the Climate Data

climate_starter.ipynb - Python and SQLAlchemy are used to do a basic climate analysis and data exploration of the climate database (hawaii.sqlite). Specifically, using SQLAlchemy ORM queries, Pandas, and Matplotlib. 
		
#### Precipitation Analysis:
	
 	Shows the summary statistics for the precipitation data.
	Displays a bar chart showing the precipitation data for the previous 12 months.
	
#### Station Analysis:

	Shows the list of stations and observation count per station.
	Calculates the lowest, highest, and average temperatures on the most-active station.
	Displays a histogram of the observed temperatures on the most-active station for the previous 12 months.

### Part 2: Design a Climate App

app.py - This file has the Climate App. It is designed using Flask. There are 5 available routes and these routes are listed in the homepage.

#### /api/v1.0/precipitation

	Shows the last 12 months of precipitation data (Date and precipitation).
 
#### /api/v1.0/stations

	Shows list of stations and their details from the dataset.
	
#### /api/v1.0/tobs

	Shows the dates and temperature observations of the most-active station for the previous year of data.
	
#### /api/v1.0/<startdate>	

	Shows minimum, maximum and average temperature for all the dates greater than or equal to the start date.
	
#### /api/v1.0/<startdate>/<enddate>

	Shows minimum, maximum and average temperature for the dates from the start date to the end date, inclusive.
	
Note:
 
The Resources folder has the data files used in this challenge. 

If Flask is not available in the environment, it can be installed using the command - pip install Flask

