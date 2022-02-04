## IMPORTATIONS ##
    
from datetime import datetime
from t4gpd.commons.DatetimeLib import DatetimeLib
from t4gpd.sun.STHardShadow import STHardShadow
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
                       occludersElevationFieldname='HAUTEUR',
                       altitudeOfShadowPlane=0, 
                       aggregate=True, tz=None, model='pysolar').run()
    if arb is not None:
        ombre_arb=STTreeHardShadow(arb, date,
                                  treeHeightFieldname ='hauteurtotale',
                                  treeCrownRadiusFieldname ='rayon',
                                  altitudeOfShadowPlane = 0,
                                  agregate = True, tz = None, model = 'pysolar').run()
    ombre_tot = ombre_bati
    ombre_tot.append(ombre_arb)
    return(ombre_tot)


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

test_buildings = GeoDataFrameDemos.districtRoyaleInNantesBuildings()
date = datetime(2021, 10, 13, 13)    
test_shadow = calcul_ombre(date, test_buildings)
mapping(test_buildings, test_shadow)



