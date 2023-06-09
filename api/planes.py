from flightsql import FlightSQLClient
import pandas as pd
import os

def flights_query(range='30 minutes'):
	query = f"""SELECT *
	FROM 'planes'
	WHERE time >= now() - interval '{range}'"""

	# Define the query client
	query_client = FlightSQLClient(
		host= os.environ["QUERY_HOST"],
		token= os.environ["QUERY_TOKEN"],
		metadata={"bucket-name": "planes"})

	# Execute the query
	info = query_client.execute(query)
	reader = query_client.do_get(info.endpoints[0].ticket)

	# Convert to dataframe
	data = reader.read_all()
	df = data.to_pandas().sort_values(by="time", ascending=False)
	df['local_time'] = df['time'].dt.tz_localize('GMT').dt.tz_convert('US/Mountain')
	df['local_time'] = df['local_time'].dt.tz_localize(None)
	df_sorted = df.sort_values(by=['From','local_time'], ascending=[False, False])
	unique = df_sorted.drop_duplicates(subset='Flight', ignore_index=True)
	return unique.drop_duplicates(subset='Callsign', ignore_index=True)

def flights_html():
	flights = flights_query()
	flight_list = []
	for index, row in flights.iterrows():
		flight, airline, origin, dest, callsign = row['Flight'], row['Airline'], row['From'], row['To'], row['Callsign']
			
		if airline:
			flight_str = f'{airline} flight {flight}'
		else:
			flight_str = f'Flight {flight}'

		if origin:
			flightroute = f'from {origin}'
		
		if dest:
			flightroute += f' to {dest}'
		
		if callsign:
			url = f'https://flightaware.com/live/flight/{callsign}'
			flightroute = flightroute if flightroute else ''
			flight_list.append({'flight': flight_str, 'url': url, 'route':flightroute})
		else:
			flight_list.append({'flight': flight_str + ' (no additional information available)'})

	return flight_list
