#FONCTIONS DE GENERATION DES OMBRES :
    
from datetime import datetime, timedelta
from t4gpd.commons.DatetimeLib import DatetimeLib
from t4gpd.sun.STHardShadow import STHardShadow

import matplotlib.pyplot as plt

from import_data import *

def calcul_ombre(date, gdf):
    '''calcul l'ombre à la date et l'heure indiquée des structures 
    contenues dans data (arbres ou batiments)'''
    gdf_ombre=STHardShadow(gdf, date, 
                       occludersElevationFieldname='HAUTEUR',
                       altitudeOfShadowPlane=0, 
                       aggregate=True, tz=None, model='pysolar').run()
    return(gdf_ombre)


#TEST :
    
from t4gpd.demos.GeoDataFrameDemos import GeoDataFrameDemos
#from shapely import geometry

test_buildings = GeoDataFrameDemos.districtRoyaleInNantesBuildings()
date = datetime(2021, 10, 13, 13)

def mapping(buildings, shadow=None):
    '''fonction pour les tests d'affichage des batiments et potentiellement d'une couche d'ombre'''
    _, basemap = plt.subplots(figsize=(1.5 * 8.26, 1.5 * 8.26))
    if shadow is not None:
        shadow.plot(ax=basemap, color='orange', edgecolor='red', alpha=0.4)
    buildings.plot(ax=basemap, color='lightgrey', edgecolor='dimgrey')
    plt.axis('off')
    plt.show()
    
test_shadow = calcul_ombre(date, test_buildings)

mapping(test_buildings, test_shadow)



