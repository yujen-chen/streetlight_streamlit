import numpy as np
import pandas as pd
import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import folium_static # import folium_static package to display folium map in streamlit


# load the shapefile data using @st.cache
@st.cache_data
def load_shn_data():
    shn_gdf = gpd.read_file("SHN_Lines_processed.geojson")
    counties = np.sort(shn_gdf['County'].unique())
    routes = np.sort(shn_gdf['Route'].unique())
    directions = shn_gdf['Direction'].unique()
    return shn_gdf, counties, routes, directions

@st.cache_data
def load_ca_data():
    ca_gdf = gpd.read_file("ca_counties_processed.geojson") 
    ca_center = ca_gdf.unary_union.centroid
    return ca_gdf, ca_center

# load the data
shn_gdf, shn_counties, shn_routes, shn_directions = load_shn_data()
ca_gdf, ca_center = load_ca_data()



# side bar
with st.sidebar:
    all_counties = [] + list(shn_counties)
    selected_county = st.selectbox(
        'County: ',
        (all_counties))
        
    selected_county_gdf = shn_gdf[shn_gdf['County']==selected_county]
    selected_county_routes = np.sort(selected_county_gdf['Route'].unique())
    selected_route = st.selectbox(
        'Route: ',
        (selected_county_routes))
    selected_route_gdf = selected_county_gdf[selected_county_gdf['Route']==selected_route]



st.write(selected_county)
st.write(selected_route)

st.write('SHN_Lines')
st.dataframe(selected_county_gdf.drop(columns=['geometry'])) # need to drop geometry column to be displayed in streamlit

# st.write('CA_counties')
# st.dataframe(ca_gdf.drop(columns=['geometry'])) 

# create folium app
def create_map(data):
    m = folium.Map(location=[ca_center.y, ca_center.x], zoom_start=5.5)
    folium.GeoJson(data).add_to(m)
    return m

# plot the map
m = create_map(selected_route_gdf)
folium_static(m)
