from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import shapefile as shp
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from metpy.cbook import get_test_data
import pandas as pd
import time
import mapdata


from werkzeug.utils import redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index2.html")

@app.route("/map", methods = ['GET','POST'])

def update():
    if request.method=='POST':
        eventdate=request.form['eventdate']
        eventtime=request.form['eventtime']
        print(eventdate)
        print(type(eventdate))
        t = eventdate+'T'+eventtime+':00.000000000'
        response = eventdate+' '+eventtime
        print(t)
        db = xr.open_dataset("2m_temp.nc")
        dv = db.metpy.parse_cf('t2m')
        y = dv.latitude
        x = dv.longitude
        

        data = dv.sel(time=t)
        response = eventdate+' '+eventtime

        shp_path = 'Admin2.shp'
        #reading the shape file by using reader function of the shape lib
        sf = shp.Reader(shp_path)

        def read_shapefile(sf):
            #fetching the headings from the shape file
            fields = [x[0] for x in sf.fields][1:]
        #fetching the records from the shape file
            records = [list(i) for i in sf.records()]
            shps = [s.points for s in sf.shapes()]
        #converting shapefile data into pandas dataframe
            df = pd.DataFrame(columns=fields, data=records)
        #assigning the coordinates
            df = df.assign(coords=shps)
            return df
        df = read_shapefile(sf)

        def plot_map(sf):
            plt.figure(figsize = [12,12])
            ax = plt.axes(projection = ccrs.Mercator())
        # This will add borders

            gl = ax.gridlines(draw_labels=True,alpha=0)
            gl.top_labels = False
            gl.rightlabels = False
            data.plot(ax=ax, cmap='jet',alpha=0.9)
            plt.title('Temperature at 2m on time:'+response, fontsize=12)
            
            for shape in sf.shapeRecords():
                x = [i[0] for i in shape.shape.points[:]]
                y = [i[1] for i in shape.shape.points[:]]
                plt.plot(x, y, 'k')
                
                
        #calling the function and passing required parameters to plot the full map
        plot_map(sf)
        plt.savefig('./static/mapf.png')
      
        return render_template("update2.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)