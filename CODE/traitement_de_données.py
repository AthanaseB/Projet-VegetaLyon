## IMPORTATIONS ##
    
from datetime import datetime
from t4gpd.commons.DatetimeLib import DatetimeLib
from t4gpd.sun.STHardShadow import STHardShadow
from t4gpd.sun.STTreeHardShadow import STTreeHardShadow
from t4gpd.demos.GeoDataFrameDemos import GeoDataFrameDemos
#from shapely import geometry
import matplotlib.pyplot as plt
from import_data import *


## FONCTIONS DE GENERATION DES OMBRES ##

def calcul_ombre(date, bati = None, arb= None):
    '''calcul l'ombre à la date et l'heure indiquée des structures 
    contenues dans les GeoDataFrame passées en paramêtre (arbres ou batiments)'''
    if bati is not None:
        ombre_bati=STHardShadow(bati, date, 
                       occludersElevationFieldname='hauteur',
                       altitudeOfShadowPlane=0, 
                       aggregate=True, tz=None, model='pysolar').run()
    if arb is not None:
        ombre_arb=STTreeHardShadow(arb, date,
                                  treeHeightFieldname ='hauteur',
                                  treeCrownRadiusFieldname ='rayon',
                                  altitudeOfShadowPlane = 0,
                                  tz = None, model = 'pysolar').run()
    if bati is not None:
        if arb is not None:
            return(ombre_bati,ombre_arb)
        else:
            return(ombre_bati)
    
    elif arb is not None:
        return(ombre_arb)
    else:
        print("pas de données indiquées")

    


## AFFICHAGE DES DONNEES ##

def mapping(buildings, shadows=None, roads=None):
    '''fonction pour les tests d'affichage des batiments et potentiellement d'une couche d'ombre'''
    _, basemap = plt.subplots(figsize=(1.5 * 8.26, 1.5 * 8.26))
    if shadows is not None:
        shadows.plot(ax=basemap, color='orange', edgecolor='red', alpha=0.4)
    if roads is not None:
        roads.plot(aw=basemap, color = 'black', )
    buildings.plot(ax=basemap, color='lightgrey', edgecolor='dimgrey')
    plt.axis('off')
    plt.show()
    
## TEST ##
"""
test_buildings = GeoDataFrameDemos.districtRoyaleInNantesBuildings()
date = datetime(2021, 10, 13, 13)    
test_shadow = calcul_ombre(date, test_buildings)
mapping(test_buildings, test_shadow)
"""
## TRAITEMENT ITINERAIRE ##

#gdf_lines est un GDF contenant les LineStrings des chemins proposés
#gdf_ombres est un GDF contenant les polygons des ombres

def ombre_autour(gdf_lines):#a créer
    '''
    Cette fonction calcul un gdf contenant les ombres des batiments et arbres proches d'un ensemble 
    d'itinéraires contenu dans gdf_lines. Cette fonction doit reduire le temps de calcul de l'ombre
    '''
    return(gdf_ombres)

def projection_ombre(gdf_lines, gdf_ombres):
    '''
    Cette fonction prend en entrée un gdf contenant des chemins pré-sélectionnés,
    ainsi que la carte des ombres.
    Elle renvoie pour chaque chemin proposé la longueur de ce chemin qui est à l'ombre
    '''
    longueur_chemin_a_l_ombre =[]
    for i in gdf_lines.index:
        longueur_ombre = 0
        for j in gdf_ombres.index:
            line = gdf_ombres["geometry"][j].intersection(gdf_lines["geometry"][i])
            longueur = line.length
            longueur_ombre = longueur_ombre + longueur
        longueur_chemin_a_l_ombre.append(longueur_ombre)
    return(longueur_chemin_a_l_ombre)

def choix_2_chemins(gdf_lines, longueur_chemin_a_l_ombre):
    '''
    Cette fonction prend en entrée 2 chemins proposés, et la distance à l'ombre
    pour chacun d'eux. On vient ensuite choisir le chemin le plus adapté, en renvoyant
    un gdf contenant uniquement le chemin choisit
    '''
    choix = 0
    
    len_1 = gdf_lines["geometry"][0].length
    len_2 = gdf_lines["geometry"][1].length
    
    len_ombre_1 = longueur_chemin_a_l_ombre[0]
    len_ombre_2 = longueur_chemin_a_l_ombre[1]
    
    #Critère 1: Si un chemin est 20% plus long que l'autre, il est exclu
    if (len_1 > len_2 * 1.2):
        choix = 2
    elif (len_2 > len_1 * 1.2):
        choix = 1
    
    #Critère 2: On choisit celui qui est, proportionnellement, le plus ombragé
    if (len_ombre_1/len_1 > len_ombre_2/len_2):
        choix = 1
    else:
        choix = 2
    return(choix-1)

def choix_n_chemins(gdf_lines,longueur_chemin_a_l_ombre):
    nb_chemins = len(longueur_chemin_a_l_ombre)
    chemins = [i for i in range(0,nb_chemins)]
    while (len(chemins)>1):
        row_1 = gdf_lines.iloc[chemins(0)]
        row_2 = gdf_lines.iloc[chemins(1)]
        gdf_temp = geopandas.GeoDataFrame([row_1,row_2])
                
        len_1 = longueur_chemin_a_l_ombre[chemins(0)]
        len_2 = longueur_chemin_a_l_ombre[chemins(1)]
        len_temp = [len_1 + len_2]
        
        choix_chemin = choix_2_chemins(gdf_temp, len_temp)
        chemins.pop(choix_chemin)
    return(gdf_lines.iloc(chemins[0]))


