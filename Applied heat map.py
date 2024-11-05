#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:03:00 2020

@author: Hank Greenburg
"""


#%%
import pandas as pd
from folium import Map
import os
from folium.plugins import HeatMap

from geotext import GeoText

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from tika import parser
path = '/home/hank/Work/Text.pdf' #This will be the location of your pdf or txt
PDFfolder = '/home/hank/Work/' #Location of collections of PDFs
#%%
pdflist = []
total = 0
lists = os.walk(PDFfolder)
for path, dir, filenames in lists:
    for filename in filenames:
        if filename.endswith(".pdf"):
                doc = os.path.join(path,filename)
                print(doc)
                total += 1 
                parsed = parser.from_file(doc)#Change the path you your own, pdf is included into the repo
                try:
                    doctext = parsed["content"]
                    docmeta = parsed["metadata"]
                    pdflist.append(doctext)

                except Exception as E:
                    print(E, "Document has no text")
                    doctext = ''
        else:
            continue
pdflist = str(pdflist)
#%%
#Comment this out if you want to run a pdf
#doc = open("/home/hank/Work/plotting-named-entities-in-python/text.txt",encoding="utf8").read()
#Change the path on the above code and it'll run a txt file
#print(f'{type(raw)}, \n{len(raw)}, \n{raw[:501]}')
places = GeoText(pdflist)# This is for getting a list of pdf's that have been parsed.

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
             (city, e)) #This is giving an error if a location is found in the document but not 
                        #able to find it's location in real life. 
#%%
#This breaks up lat_lon into seperate columns or else latitude and longitude would be in the
#same column in the csv
lat = [i[0] for i in lat_lon]
lon = [i[1] for i in lat_lon]
lon1 = [i[0] for i in lon]
lon2 = [i[1] for i in lon]
#New list with the proper columns
data = {'Location':lat,'latitude': lon1, 'longitude': lon2}
#Takes our list and makes it into a dataframe
df_lat_lon = pd.DataFrame(data)
#Used to name our columns
col_names = ["Location","latitude","longitude"]
#Saves our csv to a particular location
path2 = '/home/hank/Work/Loca1.csv' #This is the location for the saved city/country names
pd.DataFrame(df_lat_lon).to_csv(path2, header=col_names,index=False)
#%%
#Loads the data frame from the path given above
df = pd.read_csv(path2)
#%%
hm_wide = HeatMap(
    list(zip(df.latitude.values, df.longitude.values)),
    min_opacity=1,
    radius=17, 
    blur=20, #If you adjust this you change the intensity of the heat map
    max_zoom=1,
)
#%%
for_map = Map(location=[30.169621, -96.683617], zoom_start=4, )
for_map.add_child(hm_wide)
#I am unsure why this isn't showing the plot in the Spyder.
#May need a tweak as this is working in Jupyter Notebook.





