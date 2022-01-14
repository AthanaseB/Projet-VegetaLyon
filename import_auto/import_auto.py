import json
from shapely import geometry
import pandas as pd
import geopandas

def lecteur(path):
    ''' Ouvre un fichier json en dictionnaire'''
    with open(path, 'r',encoding="utf-8") as file:
        gsv = json.load(file)
    file.close
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
    #On regarde si dans le schéma il y a properties et geometry
    is_prop = False
    is_geom = False
    for cle, valeur in gsv[0].items():
        if cle == 'properties':
            is_prop = True
        if cle == 'geometry':
            is_geom = True
    
    if is_prop and is_geom:
        tab = []
        i=0
        for row in gsv:
            i=i+1
            #print(i)
            is_prop = False
            is_geom = False
            for cle, valeur in row.items():
                if cle == 'properties':
                    is_prop = True
                if cle == 'geometry':
                    is_geom = True
                    if row['geometry'] == None:
                        is_geom = False
            if is_prop and is_geom:
                dic = {}
                for cle, valeur in row['properties'].items():
                    dic[cle] = valeur
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
    '''Transorme un dictionnaire en GeoDataFrame'''
    tab = []
    for i in range(0, len(gsv)):
        geom = gsv[i]['geometry']
        rayon = gsv[i]['rayoncouronne_m']
        hauteurtotale = gsv[i]['hauteurtotale_m']
        tab.append({'index': i,'hauteur': hauteurtotale,'rayon': rayon, 'geometry': geom})
    df = pd.DataFrame(tab)
    gdf = geopandas.GeoDataFrame(df, crs=4171)
    gdf = gdf.to_crs(2154)
    return(gdf)

def building_to_gdf(gsv):
    '''Transorme un dictionnaire en GeoDataFrame'''
    tab = []
    for i in range(0, len(gsv)):
        geom = gsv[i]['geometry']
        htotale = gsv[i]['htotale']
        tab.append({'index': i,'hauteur': htotale, 'geometry': geom})
    df = pd.DataFrame(tab)
    gdf = geopandas.GeoDataFrame(df, crs=4171)
    gdf = gdf.to_crs(2154)
    return(gdf)

def road_to_gdf(gsv):
    '''Transforme un dictionnaire en GeoDataFrame'''
    tab=[]
    #A completer lorsque les donnees seront connues
    df = pd.DataFrame(tab)
    gdf = geopandas.GeoDataFrame(df, crs=4171)
    gdf = gdf.to_crs(2154)
    return(gdf)
    
def path_to_gdf(path_arbre, path_building patg_road=None):
    gsv_arbre = lecteur(path_arbre)
    gsv_arbre = deplieur_1(gsv_arbre)
    gsv_arbre = deplieur_2(gsv_arbre)
    
    gsv_building = lecteur(path_building)
    gsv_building = deplieur_1(gsv_building)
    gsv_building = deplieur_2(gsv_building)
    
    gdf_arbre = arbre_to_gdf(gsv_arbre)
    gdf_building = building_to_gdf(gsv_building)
    return(gdf_arbre, gdf_building)
