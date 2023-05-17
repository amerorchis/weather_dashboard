from flightsql import FlightSQLClient
import pandas as pd
import os

def query(range='24 hours'):
	query = f"""SELECT *
	FROM 'weather'
	WHERE time >= now() - interval '{range}'"""

	# Define the query client
	query_client = FlightSQLClient(
		host= os.environ["QUERY_HOST"],
		token= os.environ["QUERY_TOKEN"],
		metadata={"bucket-name": "weather"})

	# Execute the query
	info = query_client.execute(query)
	reader = query_client.do_get(info.endpoints[0].ticket)

	# Convert to dataframe
	data = reader.read_all()
	df = data.to_pandas().sort_values(by="time", ascending=False)
	df['local_time'] = df['time'].dt.tz_localize('GMT').dt.tz_convert('US/Mountain')
	df['local_time'] = df['local_time'].dt.tz_localize(None)
	return df

