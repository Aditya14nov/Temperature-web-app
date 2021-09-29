from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import shapefile as shp
import cartopy.feature as cfeature
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from metpy.cbook import get_test_data
import pandas as pd
import time


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
        fig = Figure()
        def plot_map(sf):
            fig = plt.figure(figsize = [12,12])
            ax = fig.add_subplot(111)
            
        # This will add borders

            data.plot(ax=ax, cmap='jet',alpha=0.9)
            plt.title('Temperature at 2m on time:'+response, fontsize=12)
            ax.set_label('Label via method')
            plt.ylabel('Latitude in degrees',fontsize = 12)
            plt.xlabel('Longitude in degrees',fontsize = 12)
            ax.legend(title='Temperature at 2m from Surface', title_fontsize = 12)
            
            for shape in sf.shapeRecords():
                x = [i[0] for i in shape.shape.points[:]]
                y = [i[1] for i in shape.shape.points[:]]
                plt.plot(x, y, 'k')
                
                
        #calling the function and passing required parameters to plot the full map
        t1=t[0:13]
        plot_map(sf)
        str = './static/'+t1+'.png'
        # print(t1)
        # print(f'./static/{t1}.png')
        plt.savefig(str)
        plt.close(fig)
        path = '.'+str
        # data = f'../static/{t1}.png'
        return render_template("update2.html", value=path)

        

if __name__ == "__main__":
    app.run(debug=True, port=5000)