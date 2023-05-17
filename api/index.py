from flask import Flask, render_template
from api.get_current import *
from api.graph import *
from bokeh.themes import Theme
from bokeh.embed import components
from bokeh.resources import CDN
import concurrent.futures


app = Flask(__name__, static_url_path='/static')
theme = Theme(filename="api/static/theme.yml")


@app.route('/')
@app.route('/daily')
def index():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit the functions to the executor
        current_future = executor.submit(get_current)
        dailies_future = executor.submit(get_dailies)
        graph_future = executor.submit(graph_daily)

        # Retrieve the results from each future
        current_temp, humidity, hum_desc, pressure, press_desc, aqi, aqi_desc, _time = current_future.result()
        low_temp, high_temp = dailies_future.result()
        p1, p2 = graph_future.result()

    script1, div1 = components(p1, theme=theme)
    script2, div2 = components(p2, theme=theme)
    
    return render_template('dashboard.html', current_temp=current_temp, humidity=humidity, hum_desc=hum_desc, pressure=pressure, press_desc=press_desc, 
                           aqi=aqi, aqi_desc=aqi_desc, pull_time=_time, low_temp=low_temp, high_temp=high_temp, script1=script1, div1=div1,
                           script2=script2, div2=div2, bokeh_resources=CDN.render())

@app.route('/static/css/style.css')
def css():
    return app.send_static_file('css/style.css')