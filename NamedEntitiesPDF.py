#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:19:46 2020

@author: Hank Greenburg
"""
#Importing the necessary package
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline #Only uncomment if used in jupyter notebook

import pandas as pd
import geopandas as gpd

from urllib import request
from geotext import GeoText

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from shapely.geometry import Point, Polygon
import descartes
from tika import parser


#%% This does txt or pdf files but it doesn't work well as pdf
#The below line will do the same but with text files
#doc = open("/home/hank/Work/plotting-named-entities-in-python/text.txt",encoding="utf8").read()
#Comment out everything below this and uncomment out the link above to do the same but with text files
parsed = parser.from_file("/home/hank/Work/Text.pdf")

try:
    doctext = parsed["content"].strip().replace("\r","").replace("\n","")

except:
    print("Document has no text")
    doctext = ''

#%%Better version of pdf parsing and plotting
parsed = parser.from_file("/home/hank/Work/Text.pdf")#Change the path you your own, pdf is included into the repo
try:
    doctext = parsed["content"]
    docmeta = parsed["metadata"]

except Exception as E:
    print(E, "Document has no text")
    doctext = ''

#%%
#print(f'{type(raw)}, \n{len(raw)}, \n{raw[:501]}')
#places = GeoText(doc) #Uncomment out if you want to do a text file
places = GeoText(doctext)# Comment out if you are working with text files or you'll get an error
cities = list(places.cities)
#cities

geolocator = Nominatim(timeout=2)

lat_lon = []
for city in cities: 
    try:
        location = geolocator.geocode(city)
        if location:
            #print(location.latitude, location.longitude)
            lat_lon.append(location)
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s"%
             (city, e))
#lat_lon

df = pd.DataFrame(lat_lon, columns=['City Name', 'Coordinates'])
df.head(7) 

#%%

geometry = [Point(x[1], x[0]) for x in df['Coordinates']]
geometry[:7]

## coordinate system I'm using
crs = {'init': 'epsg:4326'}

## convert df to geo df
geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
geo_df.head()

# world map .shp file I downloaded at https://hub.arcgis.com/datasets/a21fdb46d23e4ef896f31475217cbb08_1
#You will have to rename the shp file
countries_map =gpd.read_file('/home/hank/Work/plotting-named-entities-in-python/GeoSpatial Data/Countries_WGS84.shp')

f, ax = plt.subplots(figsize=(16, 16))
countries_map.plot(ax=ax, alpha=0.4, color='grey')
geo_df['geometry'].plot(ax=ax, markersize = 30, 
                        color = 'b', marker = '^', alpha=.2)
