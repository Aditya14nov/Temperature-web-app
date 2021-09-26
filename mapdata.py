import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import shapefile as shp
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from metpy.cbook import get_test_data
import pandas as pd
import datetime
import time


db = xr.open_dataset("2m_temp.nc")
dv = db.metpy.parse_cf('t2m')
y = dv.latitude
x = dv.longitude
eventdate = '2020-7-14'
eventtime = '00:00'
t = eventdate+'T'+eventtime+':00.000000000'

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


