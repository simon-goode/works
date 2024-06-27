import rasterio
import matplotlib
import shapely
import pandas as pd
import geopandas as gpd
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import rioxarray as rxr

from shapely.geometry import Point

airports = pd.read_csv("geospatials/resources/airports", delimiter=",", names=['id', 'name', 'city', 'country',
                                                                      'iata', 'icao', 'lat', 'long', 'altitude',
                                                                      'timezone', 'dst', 'tz', 'type', 'source'])

# airport_geometry = [Point(xy) for xy in zip(airports['long'], airports['lat'])]
# airport_geodata = gpd.GeoDataFrame(airports, crs="EPSG:4326", geometry=airport_geometry)
# fig, ax = plt.subplots(facecolor='black',
#                        subplot_kw={'projection': ccrs.Robinson()},
#                        figsize=(20,20))
# ax = plt.axes(projection=ccrs.Robinson())
# ax.patch.set_facecolor('black')

# airport_geodata.plot(ax=ax, transform=ccrs.PlateCarree, markersize=4, alpha=1, color='crimson', edgecolors='none')
# plt.setp(ax.spines.values(), color='black')
# plt.setp([ax.get_xticklines(), ax.get_yticklines()], color='black')
# ax.set_ylim(-7000000, 9000000)
# plt.show()

routes = pd.read_csv("geospatials/resources/routes",
                     delimiter=',',
                     names=['airline', 'id', 'source_airport',
                            'source_airport_id', 'destination_airport',
                            'destination_airport_id', 'codeshare',
                            'stops', 'equitment'])
source_airports = airports[['name', 'iata', 'icao', 'lat', 'long']]
destination_airports = source_airports.copy()
source_airports.columns = [str(col) + '_source' for col in source_airports.columns]
destination_airports.columns = [str(col) + '_destination' for col in destination_airports.columns]

routes = routes[['source_airport', 'destination_airport']]
routes = pd.merge(routes,
                  source_airports,
                  left_on='source_airport',
                  right_on='iata_source')
routes = pd.merge(routes,
                  destination_airports,
                  left_on='destination_airport',
                  right_on='iata_destination')

from shapely.geometry import LineString

routes_geometry = [LineString([[routes.iloc[i]['long_source'],
                                routes.iloc[i]['lat_source']],
                                [routes.iloc[i]['long_destination'],
                                 routes.iloc[i]['lat_destination']]]) for i in range(routes.shape[0])]
routes_geodata = gpd.GeoDataFrame(routes, geometry=routes_geometry, crs='EPSG:4326')

airport_source_count = routes.source_airport.value_counts()
airport_destination_count = routes.destination_airport.value_counts()

airport_source_count = pd.DataFrame({'airport':airport_source_count.index,
                                     'source_airport_count': airport_source_count.values})
airport_destination_count = pd.DataFrame({'airport':airport_destination_count.index,
                                     'destination_airport_count': airport_destination_count.values})

airport_counts = pd.merge(airport_source_count,
                          airport_destination_count,
                          left_on="airport",
                          right_on="airport")
airport_counts['count'] = airport_counts['source_airport_count'] + airport_counts['destination_airport_count']
airport_counts = pd.merge(airport_counts,
                          airports,
                          left_on="airport",
                          right_on="iata")

geometry = [Point(xy) for xy in zip(airport_counts.long, airport_counts.lat)]

airport_counts = gpd.GeoDataFrame(airport_counts, geometry=geometry, crs="EPSG:4326")
airport_counts['markersize'] = airport_counts['count'] / 10

fig, ax = plt.subplots(subplot_kw={'projection': ccrs.Robinson()}, figsize=(20,20))
ax.patch.set_facecolor('black')

routes_geodata.plot(ax=ax, color='white', linewidth=0.1, alpha=0.1, transform=ccrs.Geodetic())
airport_counts.plot(ax=ax, markersize=airport_counts['markersize'], transform=ccrs.PlateCarree(), alpha=0.8, column=airport_counts['long'], cmap='jet', edgecolors='none')
plt.setp(ax.spines.values(), color='#090909')
plt.setp([ax.get_xticklines(), ax.get_yticklines()], color='#090909')
ax.set_ylim(-7000000, 8800000)
plt.show()