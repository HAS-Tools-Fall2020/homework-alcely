# %%
# Section 1: Import the modules we will use.
# Note: you may need to install some packages.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import help_function as hf
import seaborn as sns
import geopandas as gpd
import fiona
import contextily as ctx

# %%
# Section 2: Modify the following variables
current_week = 13

# USGS URL for the flow data:
site = '09506000'
start = '1989-01-01'
end = '2020-11-21'

# %%
# Section 3: Download the flow data directly from the USGS website.


url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no=" + \
      site + "&referred_module=sw&period=&begin_date=" + start + \
      "&end_date=" + end
data = pd.read_table(url, skiprows=30,
                     names=['agency_cd', 'site_no',
                            'datetime', 'flow', 'code'],
                     parse_dates=['datetime'])

# Expand the dates to year, month, day, and days of the week.
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# Aggregate flow values to weekly: from sunday to saturday
flow_weekly = data.resample("W-SAT", on='datetime').mean()

# %%
# Section 4: The forecast
# Step 4.1: Calculate the historical daily mean flow.

hist_flow = hf.hist_daily_mean(data, 2020)

# Step 4.2: create a dataframe to store all the variables
# related to the forecast.
# Step 4.3: aggregate the historical daily mean flow to weekly
# starting from 2020-08-23 to the following 15 weeks.
mymodel = pd.DataFrame(
    {'hist_data': hf.weekly_mean(hist_flow, 8, 29, 16),
     'data_2020': np.zeros(16)},
    index=np.arange(1, 17))

# Step 4.4: Store in the df the 2020 weekly flow
# from 2020-08-23 to the most recent value
mymodel['data_2020'] = (mymodel['data_2020'].iloc[0:current_week] +
                        flow_weekly['2020-08-29':]['flow'].values
                        ).round(2)

# Step 4.5: calculate correction factor
mymodel['factors'] = (mymodel.data_2020.values /
                      mymodel.hist_data.values
                      ).round(3)

# Step 4.6: Brain model for 16 weeks
mymodel['forecasts16'] = (mymodel['hist_data'].values *
                          mymodel['factors'][11:current_week].mean()
                          ).round(2)

# Step 4.7: Regressive model for 16 weeks
x = mymodel.iloc[7:current_week][['hist_data']].values.reshape(-1, 1)
y = mymodel.iloc[7:current_week]['data_2020'].values

lt_pred = []
for i in range(16):
    initial_xval = mymodel['hist_data'].iloc[i]
    if i < 4:
        pred = (hf.R_Model(x, y, initial_xval) * 0.6).round(2)
    else:
        pred = hf.R_Model(x, y, initial_xval).round(2)
    lt_pred.append(pred[0])

mymodel['Rmodel'] = lt_pred

# Step 4.8: print results
print('My forecast entries #', current_week)
print('week1 =', mymodel['forecasts16'][current_week+1])
print('week2 =', mymodel['forecasts16'][current_week+2])
print('16 weeks forecast:')
mymodel[['Rmodel']]

# %%
# Section 5: Graphs
# Section 5.1: a line plot
plt.style.use('seaborn')

fig, ax = plt.subplots()
ax.plot(mymodel['hist_data'].T, color='black', label='Historical Mean')
ax.plot(mymodel['data_2020'].T, color='blue', label='2020 weekly flows')
ax.plot(mymodel['forecasts16'].T, color='r', label='Brain model',
        linestyle="--")
ax.plot(mymodel['Rmodel'].T, color='green', label='Regression model',
        linestyle="--")
ax.set(title="Observed & Predicted Flow", xlabel="Weeks",
       ylabel="Weekly Avg Flow [cfs]")
ax.legend()

fig.savefig('plot_lines.png')

# Section 5.2: a scatter plot
plt.style.use('seaborn')

fig, ax = plt.subplots()
ax.set_aspect(1)
sns.regplot(x=mymodel.loc[1:current_week]['hist_data'].values,
            y=mymodel.loc[1:current_week]['data_2020'].values,
            line_kws={"color": "r", "alpha": 0.7, "lw": 2})
ax.set(title="Observed Flow 2020 -vs- Historical Mean Flow",
       ylabel="Observed Flow 2020 [cfs]",
       xlabel="Historical Mean Flow [cfs]")

fig.savefig("plot_scatter.png")

# %%
# Section 6: Create a Map
# Section 6.2: Looking the LAT and LON of specific USGS gauge
# Gauges II USGS stream gauge dataset:
# Download here:
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder
file = r'..\..\data\gagesII_9322_point_shapefile\gagesII_9322_sept30_2011.shp'
gages = gpd.read_file(file)

# Section 6.3: Creating dataframe USGS stream gauge
df_usgs = pd.DataFrame({'STAID': ['09506000'],
                        'STANAME': ['VERDE RIVER NEAR CAMP VERDE, AZ'],
                        'LAT': [34.448361],
                        'LON': [-111.789871]})

# Section 6.4: Adding more datasets
# Watershed boundaries for the lower colorado:
# https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View

file = r'..\..\data\WBD_15_HU2_GDB\WBD_15_HU2_GDB.gdb'
fiona.listlayers(file)
HUC6 = gpd.read_file(file, layer="WBDHU6")

# Section 6.5: Arizona USGS gauges
gages_AZ = gages[gages['STATE'] == 'AZ']

# Section 6.6: creating the GeoDataFrame
# USGS
gdf_usgs = gpd.GeoDataFrame(
    df_usgs, geometry=gpd.points_from_xy(df_usgs.LON, df_usgs.LAT),
    columns=['geometry'], crs=HUC6.crs)

# Change projection of HUC6
HUC6_az = HUC6.to_crs(gages_AZ.crs)
usgs_az = gdf_usgs.to_crs(gages_AZ.crs)

# Section 6.7: Map
fig, ax = plt.subplots(figsize=(8, 8))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=50, cmap='Dark2',
              ax=ax, label='Drain area (km^2)')
usgs_az.plot(ax=ax, color='b', marker='*', markersize=200,
             label='Forecast Gauge')
HUC6_az.boundary.plot(ax=ax, color=None,
                      edgecolor='dimgrey', linewidth=1)
plt.ylabel('Latitude(m)', fontsize=10, labelpad=0)
plt.xlabel('Longitude(m)', fontsize=10, labelpad=0)
plt.title('Gauges in the watershed\nof Lower Colorado River')
text = ('VERDE RIVER NEAR CAMP VERDE' +
        '\nLat: 34.45\nLon: -111.79')
plt.annotate(text, xy=(-1432892.272, 1384411.251),
             xycoords='data', xytext=(-1532892, 1684411), textcoords='data',
             arrowprops=dict(arrowstyle="->"))
ctx.add_basemap(ax, crs=gages_AZ.crs)
ax.legend()

plt.savefig('lau_map.png')

# %%
