## IMPORTATION ##

import json
from shapely import geometry
import pandas as pd
import geopandas

## LECTURE GEOJSON ##

def arbre_to_gdf(path):
    '''Renvoie un GeoDataFrame à partir du chemin où est déposé le geoJson d alignement des arbres'''
    with open(path, 'r',encoding="utf-8") as file:
        gsv = json.load(file)
        gsv = gsv['features']
    file.close
    tab = []
    for i in range(0, len(gsv)):
        x, y = gsv[i]['geometry']['coordinates']
        point = geometry.Point(x,y)
        rayon = gsv[i]['properties']['rayoncouronne_m']
        hauteurtotale = gsv[i]['properties']['hauteurtotale_m']
        tab.append({'index': i,'hauteur': hauteurtotale,'rayon': rayon, 'geometry': point})
    df = pd.DataFrame(tab)
    gdf = geopandas.GeoDataFrame(df, crs=4171)
    gdf = gdf.to_crs(2154)
    return(gdf)

def building_to_gdf(path):
    '''Renvoie un GeoDataFrame à partir du chemin où est déposé le geoJson des batiments'''
    with open(path, 'r',encoding="utf-8") as file:
        gsv = json.load(file)
        gsv = gsv['features']
    file.close
    tab = []
    for i in range(0, len(gsv)):
        coord = gsv[i]['geometry']['coordinates'][0]
        geom = geometry.Polygon(coord)
        htotale = gsv[i]['properties']['htotale']
        tab.append({'index': i,'hauteur': htotale, 'geometry': geom})
    df = pd.DataFrame(tab)
    gdf = geopandas.GeoDataFrame(df, crs=4171)
    gdf = gdf.to_crs(2154)
    return(gdf)

## TESTS ##

path_arbre = "C:/Users/meder/Documents/Etudes/EC Nantes/EI3/P1/Automatisation de l'importation/data_short/arbre_villeurbanne.json"
gdf_arbre = arbre_to_gdf(path_arbre)
print(gdf_arbre.head())

path_building = "C:/Users/meder/Documents/Etudes/EC Nantes/EI3/P1/Automatisation de l'importation/data_short/building_first_100.json"
gdf_building = building_to_gdf(path_building)
print(gdf_building.head())