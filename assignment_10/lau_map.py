# %% 
# %%
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import geopandas as gpd
import fiona
from shapely.geometry import Point
import contextily as ctx


# %%
# Section 1: Reading data to plot
# Section 1.2: Looking the LAT and LON of specific USGS gauge
# Gauges II USGS stream gauge dataset:
# Download here:
# https://water.usgs.gov/GIS/metadata/usgswrd/XML/gagesII_Sept2011.xml#stdorder
file = r'C:\Users\alcel\Documents\GitHub\2020FA_CodingSkills\homework-alcely\data\gagesII_9322_sept30_2011\gagesII_9322_sept30_2011.shp'
gages = gpd.read_file(file)

# Look the information of some gauges
gages[gages['STAID'] == '09506000'][['STANAME', 'LAT_GAGE', 'LNG_GAGE']]
gages[gages['STAID'] == '09504000'][['STANAME', 'LAT_GAGE', 'LNG_GAGE']]
gages[gages['STAID'] == '09505400'][['STANAME', 'LAT_GAGE', 'LNG_GAGE']]

# Section 1.2: Creating dataframe USGS stream gauge
df_usgs = pd.DataFrame({'STAID': ['09506000', '09504000',
                                  '09505400'],
                        'STANAME': ['VERDE RIVER NEAR CAMP VERDE, AZ',
                                    'VERDE RIVER NEAR CLARKDALE, AZ.',
                                    'BEAVER CREEK NR LAKE MONTEZUMA, AZ'
                                    ],
                        'LAT': [34.448361, 34.852242, 	34.615],
                        'LON': [-111.789871, -112.065994, -111.837222]})

# Section 1.3: Creating dataframe NOAA weather gauge
df_NOAA = pd.DataFrame({'STAID': ['USC00025635'],
                        'STANAME': ['MONTEZUMA CASTLE NM, AZ'],
                        'LAT': [34.616667],
                        'LON': [-111.833333]})

# Section 1.4: Adding more datasets
# Watershed boundaries for the lower colorado:
# https://viewer.nationalmap.gov/basic/?basemap=b1&category=nhd&title=NHD%20View

file = r'C:\Users\alcel\Documents\GitHub\2020FA_CodingSkills\homework-alcely\data\WBD_15_HU2_GDB\WBD_15_HU2_GDB.gdb'
fiona.listlayers(file)
HUC6 = gpd.read_file(file, layer="WBDHU6")
print(HUC6.crs)

# Section 1.5: Arizona USGS gauges
gages_AZ = gages[gages['STATE'] == 'AZ']

# %%
# Section 2: creating the GeoDataFrame
# USGS
gdf_usgs = gpd.GeoDataFrame(
    df_usgs, geometry=gpd.points_from_xy(df_usgs.LON, df_usgs.LAT),
    columns=['geometry'], crs=HUC6.crs)

print(gdf_usgs.head())
print(gdf_usgs.crs)

# NOAA
gdf_NOAA = gpd.GeoDataFrame(
    df_NOAA, geometry=gpd.points_from_xy(df_NOAA.LON, df_NOAA.LAT),
    columns=['geometry'], crs=HUC6.crs)

print(gdf_NOAA.head())
print(gdf_NOAA.crs)

# Change projection of HUC6
HUC6_az = HUC6.to_crs(gages_AZ.crs)
usgs_az = gdf_usgs.to_crs(gages_AZ.crs)
noaa_az = gdf_NOAA.to_crs(gages_AZ.crs)


# %%
# Section 3: Map
fig, ax = plt.subplots(figsize=(8, 8))
gages_AZ.plot(column='DRAIN_SQKM', categorical=False,
              legend=True, markersize=10, cmap='Dark2',
              ax=ax, label= 'Drain area (km^2)')
usgs_az.plot(ax=ax, color='r', marker='*', markersize=25, label='USGS GAUGES')
noaa_az.plot(ax=ax, color='b', marker='s', markersize=25, label='NOAA GAUGES')
HUC6_az.boundary.plot(ax=ax, color=None,
                      edgecolor='dimgrey', linewidth=1)
plt.ylabel('Latitude(m)', fontsize=10, labelpad=0)
plt.xlabel('Longitude(m)', fontsize=10, labelpad=0)
plt.title('Gauges in the watershed\nof Lower Colorado River')
text = ('Forecast Gauge:\nVERDE RIVER NEAR CAMP VERDE' +
        '\nLat: 34.45\nLon: -111.79')
plt.annotate(text, xy=(-1432892.272, 1384411.251),
             xycoords='data', xytext=(-1532892, 1684411), textcoords='data',
             arrowprops=dict(arrowstyle="->"))
ctx.add_basemap(ax, crs=gages_AZ.crs)
ax.legend()

plt.savefig('lau_map.png')
