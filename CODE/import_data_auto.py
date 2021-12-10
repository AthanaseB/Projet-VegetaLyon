## IMPORTATION ##

import json
from shapely import geometry
import pandas as pd
import geopandas
import time

## LECTURE GEOJSON ##

def lecteur(path):
    ''' Ouvre un fichier json en dictionnaire'''
    with open(path, 'r',encoding="utf-8") as file:
        gsv = json.load(file)
    return(gsv)

def deplieur_1(gsv):
    '''Déplie la première étape'''
    is_features = False
    for cle, valeur in gsv.items():
        if cle == 'features':
            is_features = True
    if is_features:
        return(gsv['features'])
    else:
        return(gsv)

def deplieur_2(gsv):
    '''Déplie la deuxième étape'''
    
    tab = []
    #On regarde si dans le schéma il y a properties et geometry pour chaque ligne : 
    for row in gsv:  
        is_prop = False
        is_geom = False
        for cle, valeur in row.items():
            if cle == 'properties':
                is_prop = True
            if cle == 'geometry':
                is_geom = True
                if row['geometry'] == None:
                    is_geom = False
        
        #Si le schéma correspond, on ajoute les propriétés et la géométrie sous une forme utilisable
        if is_prop and is_geom:
            dic = {}
            for cle, valeur in row['properties'].items():
                dic[cle] = valeur #ajout des propriétés
                
                #ajout de la géométrie sous la forme appropriée en fonction du type et des coordonnées :
                type_geom = row['geometry']['type']
                if type_geom == 'Point':
                    geom = geometry.Point(row['geometry']['coordinates'])
                elif type_geom == 'Polygon':
                    geom = geometry.Polygon(row['geometry']['coordinates'][0])
                elif type_geom == 'MultiPolygon':
                    geom = geometry.Polygon(row['geometry']['coordinates'][0][0])
                dic['geometry'] = geom
                
            tab.append(dic)
    return(tab)

def arbre_to_gdf(gsv):
    '''Créé un Geodataframe contenant les données qui nous interessent sur les arbres'''
    tab = []
    for i in range(0, len(gsv)):
        geom = gsv[i]['geometry']
        
        if 'rayoncouronne_m' in gsv[i].keys():
            rayon = gsv[i]['rayoncouronne_m']
        else:
            rayon = 0
            
        if 'hauteurtotale_m' in gsv[i].keys(): 
            hauteurtotale = gsv[i]['hauteurtotale_m']
        else:
            hauteurtotale = 0
            
        tab.append({'index': i,'hauteur': hauteurtotale,'rayon': rayon, 'geometry': geom})
    df = pd.DataFrame(tab)
    gdf = geopandas.GeoDataFrame(df, crs=4171)
    gdf = gdf.to_crs(2154)
    return(gdf)

def building_to_gdf(gsv):
    '''Créé un Geodataframe contenant les données qui nous interessent sur les batiments'''
    tab = []
    for i in range(0, len(gsv)):
        geom = gsv[i]['geometry']
        htotale = gsv[i]['htotale']
        tab.append({'index': i,'hauteur': htotale, 'geometry': geom})
    df = pd.DataFrame(tab)
    gdf = geopandas.GeoDataFrame(df, crs=4171)
    gdf = gdf.to_crs(2154)
    return(gdf)

## FONCTION COMPLETE ##

def path_to_gdf(path_arbre, path_building):
    '''fonction finale regroupant créant les geodataframes des arbres et batiments à partir des chemins d'accès'''
    gsv_arbre = lecteur(path_arbre)
    gsv_arbre = deplieur_1(gsv_arbre)
    gsv_arbre = deplieur_2(gsv_arbre)
    
    gsv_building = lecteur(path_building)
    gsv_building = deplieur_1(gsv_building)
    gsv_building = deplieur_2(gsv_building)
    
    gdf_arbre = arbre_to_gdf(gsv_arbre)
    gdf_building = building_to_gdf(gsv_building)
    return(gdf_arbre, gdf_building)

path_arbre="data/arbre_villeurbanne.json"
path_buildings="data/building_first_100.json"

#tests
#arb, bati=path_to_gdf(path_arbre, path_buildings)
#arb.head()
