# Projet-VegetaLyon
Ce projet est réalisé par des étudiants de l'Ecole Centrale de Nantes, en option Ville Numérique. L'objectif est de créé une application permettant de calculer des "parcours fraicheur" pour des piétons dans la ville de Lyon.
Nous désirons également déterminer les zones qui devraient être végétalisées 

## Cahier des charge

Nous avons défini plusieurs objectifs pour mener à bien ce projet:

OBJECTIF 1: Réalisation d’une carte des ombres, dépendant de l’heure de la journée ainsi que de la date, sur les rues de la zone d’étude.
- Délimiter la zone d’étude
- Recenser les données à disposition & données qui pourraient nous être utiles
- Localiser les sources d’ombre dans la zone d’étude (Arbres, Bâtiments) et leurs caractéristiques (forme, hauteur)
- Calcul de la projection des ombres au sol (contacter Thomas Leduc à propos d’une extension permettant de faire ce calcul)
- Réalisation d’une carte des ombres des bâtiments  (à une date et heure précise, puis de cartes pour chaque heure)
- Réalisation d’une carte des ombres de la végétation (à une date et heure précise, puis de cartes pour chaque heure)
- Réalisation d’une carte des ombres totale  (à une date et heure précise, puis de cartes pour chaque heure)
- Réalisation d’une carte interactive


OBJECTIF 2: Calcul de parcours fraîcheur.
- Déterminer la température “perdue” lorsqu’on est à l’ombre
- Mettre en place un algorithme déterminant le meilleur chemin, avec prise en compte du temps de trajet, de la température, et potentiellement d’autres paramètres (déterminer une pondération).


OBJECTIF 3: Déterminer les zones à végétaliser de façon prioritaire.
- Nécessite des données sur les trajets les plus empruntés par les usagers
- Croiser les trajets les plus empruntés et les trajets les moins ombragés


OBJECTIFS ANNEXES:
- Réfléchir à un moyen d’acquérir des données pour mesurer les températures et confirmer le modèle de simulation.

## Fichiers 

* `README.md` : Ce fichier est celui que vous êtes en train de lire, il explique comment s'y retrouver dans le GitHub.
* `data` : Ce dossier contient les données utilisées par les différents fichiers
* `import_data.py` : Ce programme python contient des fonctions permettant d'importer des données

