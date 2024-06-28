import rasterio
import matplotlib as mpl
import shapely
import pandas as pd
import geopandas as gpd
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import rioxarray as rxr

from shapely.geometry import Point

ma_map = gpd.read_file("geospatials/resources/TOWNSSURVEY_POLYM.shp")
town_data = pd.read_csv("geospatials/resources/towndata.csv")
counties_map = gpd.read_file("geospatials/resources/COUNTIESSURVEY_POLYM.shp")

min_data = min(town_data['median_household_income'])
max_data = max(town_data['median_household_income'])

color_min = 0
color_max_scaling = 1

def color_fader(c1, c2, mix=0):
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

town_data['color_scaling'] = color_min + (max_data - town_data['median_household_income'] + min_data) / (max_data) * color_max_scaling
town_data['colors'] = town_data['color_scaling'].apply(lambda x: "#{:02x}{:02x}{:02x}".format(int(40*x/color_max_scaling), int(90*x/color_max_scaling), int(255*x/color_max_scaling)))
# county_to_color = {
#     "MIDDLESEX": (0, 0, 1, 1),
#     "BARNSTABLE": (1, 1, 0, 1),
#     "BERKSHIRE": (1, 0, 0, 1),
#     "BRISTOL": (1, 0, 1, 1),
#     "DUKES": (0, 1, 0, 1),
#     "ESSEX": (0.5, 0, 1, 1),
#     "FRANKLIN": (1, 0.5, 0, 1),
#     "HAMPDEN": (0, 0.5, 0.5, 1),
#     "HAMPSHIRE": (0, 0, 0, 1),
#     "NANTUCKET": (0, 0, 0, 1),
#     "NORFOLK": (0, 0.5, 1, 1),
#     "PLYMOUTH": (0.5, 1, 1, 1),
#     "SUFFOLK": (1, 0.5, 1, 1),
#     "WORCESTER": (1, 1, 0/5, 1)
# }
# town_data['colors'] = town_data['COUNTY'].map(county_to_color)

# def multiply(t, s):
#     m = tuple(item * s if i < 3 else item for i, item in enumerate(t))
#     return m

# town_data['colors'] = town_data.apply(lambda row: multiply(row['colors'], row['color_scaling']), axis=1)

ma_map = pd.merge(ma_map, town_data, left_on='TOWN', right_on='TOWN')


ax = ma_map.plot(color=ma_map['colors'], edgecolors=(1, 1, 1, 0.3))
ax.set_facecolor("#141030")
counties_map.plot(ax=ax, edgecolors='white', color="none")
plt.show()