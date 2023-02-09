# SQLAlchemy Challenge
## Background 
To help with trip planning, decide to do a climate analysis about the area. The following sections outline the steps that were taken to accomplish this task.

## PART 1 : Analyse and Explore the Climate Data

* Precipitation Analysis

A query is designed to retrieve the last 12 months of precipitation data, and only the date and prcp values is selected.

The query results also loded into a Pandas DataFrame to help get discriptive analysis of data 
Finally the result ploted by using the DataFrame plot method.

* Station Analysis

Queried data to get total number of stations in data.

Session query is desisgned to find most active station and temprature observations related to this active sation for recent 12 months in given data.

## PART 2 : Climate APP

After the initial analysis was completed, a Flask API designed based on the queries already developed.

The following routes are created by using Flask.

* /api/v1.0/precipitation
    Convert the query results to a dictionary using date as the key and prcp as the value.
* /api/v1.0/stations
    Return a JSON list of stations from the dataset.
* /api/v1.0/tobs
    Return a JSON list of temperature observations (TOBS) for the previous year of the most active station.
* /api/v1.0/<start> and /api/v1.0/<start>/<end>
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.