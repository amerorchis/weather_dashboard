from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter, DataRange1d
from bokeh.layouts import layout, row
from bokeh.themes import Theme
import pandas as pd
from api.query import query
from bokeh.io import curdoc
from api.convert import *
from bokeh.models import Label, Circle, HoverTool, ColumnDataSource
from datetime import datetime


# refactor this so that only one function is used and the timeframe is just passed as a variable

def graph_daily(timeframe='daily'):
	if timeframe == 'daily':
		title = 'Over Last 24 Hours'
		x_start = df['local_time'].min() - pd.Timedelta(minutes=15)
		x_stop = df['local_time'].max() + pd.Timedelta(minutes=15)

	# create a figure object
	df = query()

	# Add relevant columns
	df['Temp_F'] = df['Temp'].apply(convert_temp)
	df['AQI'] = df['Particulates2_5'].apply(get_aqi)

	# Create Temperature Graph
	p = figure(title=f'Temperature {title}', x_axis_label='Time', y_axis_label=f'Temperature (°F)', sizing_mode='stretch_width', max_width=820, height=350)
	p.x_range = DataRange1d(start=x_start, end=x_stop)
	max_temp = int(float(df['Temp_F'].max()))//1
	margin = max_temp*0.2 if max_temp*0.2 > 3 else 3
	p.y_range = DataRange1d(start=int(float(df['Temp_F'].min()))//1-margin, end=max_temp+margin)
	p.xaxis.formatter = DatetimeTickFormatter(seconds = '%-I:%M:%S', minsec = '%-I:%M:%S', minutes = '%-I:%M:%S', hours='%b %-d, %-I:%M%p')

	# add a line to the figure
	p.line(x=df['local_time'], y=df[f'Temp_F'], line_width=3)
	p.toolbar.logo = None
	p.toolbar_location = None

	latest_time = df['local_time'].max()
	current = df.loc[df['local_time'] == latest_time]
	latest_temperature = float(current['Temp_F'].iloc[0])

	circle_source = ColumnDataSource(data=dict(x=[latest_time], y=[latest_temperature]))
	dot = Circle(x=latest_time, y=latest_temperature, line_color="#050517", size=15, line_width=0, fill_color="#a0d68d")
	dot_renderer = p.add_glyph(circle_source, dot)

	label = Label(x=latest_time, x_offset=-53, y=latest_temperature, y_offset=26, background_fill_color='#e1e8ed', text=f'Now: {(round(latest_temperature))}°F', 
	       text_color="black", text_font_size="12px", text_baseline="middle", text_align="left", border_line_width = 3, border_line_color='#e1e8ed')
	p.add_layout(label)
	
	hover_tool = HoverTool(tooltips=[("Time", "@x{%b %-d, %-I:%M%p}"), ("Temp", "@y{0.00}°F")], formatters={"@x": "datetime"})
	p.add_tools(hover_tool)
	hover_tool = HoverTool(tooltips=[("Temperature Now", "@y{0.00}°F")], renderers=[dot_renderer])
	p.add_tools(hover_tool)

	# Create AQI graph
	q = figure(title=f'AQI {title}', x_axis_label='Time', y_axis_label=f'AQI', sizing_mode='stretch_width', max_width=820, height=350)
	q.x_range = DataRange1d(start=x_start, end=x_stop)
	max_aqi = int(float(df['AQI'].max()))//1
	margin = max_aqi*0.2 if max_aqi*0.2 > 5 else 5
	q.y_range = DataRange1d(start=0, end=max_aqi+margin)
	q.xaxis.formatter = DatetimeTickFormatter(seconds = '%-I:%M:%S', minsec = '%-I:%M:%S', minutes = '%-I:%M:%S', hours='%b %-d, %-I:%M%p')

	# add a line to the figure
	q.line(x=df['local_time'], y=df[f'AQI'], line_width=2)
	q.toolbar.logo = None
	q.toolbar_location = None

	latest_aqi = float(current['AQI'].iloc[0])

	circle_source = ColumnDataSource(data=dict(x=[latest_time], y=[latest_aqi]))
	dot = Circle(x=latest_time, y=latest_aqi, line_color="#050517", size=15, line_width=0, fill_color="#a0d68d")
	dot_renderer = q.add_glyph(circle_source, dot)

	label = Label(x=latest_time, x_offset=-50, y=latest_aqi, y_offset=20, background_fill_color='#e1e8ed', text=f'Now: {(round(latest_aqi))}', 
	       text_color="black", text_font_size="12px", text_baseline="middle", text_align="left", border_line_width = 3, border_line_color='#e1e8ed')
	q.add_layout(label)
	
	hover_tool = HoverTool(tooltips=[("Time", "@x{%b %-d, %-I:%M%p}"), ("AQI", "@y")], formatters={"@x": "datetime"})
	q.add_tools(hover_tool)
	hover_tool = HoverTool(tooltips=[("Now", "@y")], renderers=[dot_renderer])
	q.add_tools(hover_tool)

	return p, q

def graph_weekly():
	# create a figure object
	df = query('7 days')

	# Add relevant columns
	df['Temp_F'] = df['Temp'].apply(convert_temp)
	df['AQI'] = df['Particulates2_5'].apply(get_aqi)

	# Create Temperature Graph
	p = figure(title=f'Temperature Over Last 7 Days', x_axis_label='Time', y_axis_label=f'Temperature (°F)', sizing_mode='stretch_width', max_width=820, height=350)
	p.x_range = DataRange1d(start=datetime.now() - pd.Timedelta(days=7, hours=8), end=datetime.now() + pd.Timedelta(hours=8))
	p.y_range = DataRange1d(start=int(float(df['Temp_F'].min()))//1-1, end=int(float(df['Temp_F'].max()))//1+1)
	p.xaxis.formatter = DatetimeTickFormatter(days='%b %-d, %-I:%M%p', hours='%b %-d, %-I:%M%p')

	# add a line to the figure
	p.line(x=df['local_time'], y=df[f'Temp_F'], line_width=3)
	p.toolbar.logo = None
	p.toolbar_location = None

	latest_time = df['local_time'].max()
	current = df.loc[df['local_time'] == latest_time]
	latest_temperature = float(current['Temp_F'].iloc[0])

	circle_source = ColumnDataSource(data=dict(x=[latest_time], y=[latest_temperature]))
	dot = Circle(x=latest_time, y=latest_temperature, line_color="#050517", size=15, line_width=0, fill_color="#a0d68d")
	dot_renderer = p.add_glyph(circle_source, dot)

	label = Label(x=latest_time, x_offset=-53, y=latest_temperature, y_offset=26, background_fill_color='#e1e8ed', text=f'Now: {(round(latest_temperature))}°F', 
	       text_color="black", text_font_size="12px", text_baseline="middle", text_align="left", border_line_width = 3, border_line_color='#e1e8ed')
	p.add_layout(label)
	
	hover_tool = HoverTool(tooltips=[("Time", "@x{%b %-d, %-I:%M%p}"), ("Temp", "@y{0.00}°F")], formatters={"@x": "datetime"})
	p.add_tools(hover_tool)
	hover_tool = HoverTool(tooltips=[("Temperature Now", "@y{0.00}°F")], renderers=[dot_renderer])
	p.add_tools(hover_tool)

	# Create AQI graph
	q = figure(title=f'AQI Over Last 7 Days', x_axis_label='Time', y_axis_label=f'AQI', sizing_mode='stretch_width', max_width=820, height=350)
	q.x_range = DataRange1d(start=datetime.now() - pd.Timedelta(days=7, hours=8), end=datetime.now() + pd.Timedelta(hours=8))
	max_aqi = int(float(df['AQI'].max()))//1
	margin = max_aqi*0.2 if max_aqi*0.2 > 5 else 5
	q.y_range = DataRange1d(start=0, end=max_aqi+margin)
	q.xaxis.formatter = DatetimeTickFormatter(days='%b %-d, %-I:%M%p', hours='%b %-d, %-I:%M%p')

	# add a line to the figure
	q.line(x=df['local_time'], y=df[f'AQI'], line_width=2)
	q.toolbar.logo = None
	q.toolbar_location = None

	latest_aqi = float(current['AQI'].iloc[0])

	circle_source = ColumnDataSource(data=dict(x=[latest_time], y=[latest_aqi]))
	dot = Circle(x=latest_time, y=latest_aqi, line_color="#050517", size=15, line_width=0, fill_color="#a0d68d")
	dot_renderer = q.add_glyph(circle_source, dot)

	label = Label(x=latest_time, x_offset=-50, y=latest_aqi, y_offset=20, background_fill_color='#e1e8ed', text=f'Now: {(round(latest_aqi))}', 
	       text_color="black", text_font_size="12px", text_baseline="middle", text_align="left", border_line_width = 3, border_line_color='#e1e8ed')
	q.add_layout(label)
	
	hover_tool = HoverTool(tooltips=[("Time", "@x{%b %-d, %-I:%M%p}"), ("AQI", "@y")], formatters={"@x": "datetime"})
	q.add_tools(hover_tool)
	hover_tool = HoverTool(tooltips=[("Now", "@y")], renderers=[dot_renderer])
	q.add_tools(hover_tool)

	return p, q