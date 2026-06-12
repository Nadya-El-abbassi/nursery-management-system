# Nursery Management System_GreenTech_Sisters

##  Description du Notre  projet

Smart Nursery est une application web de gestion de stock et de ventes destinée à une pépinière.
Elle permet de gérer les plantes, les catégories, les ventes, ainsi qu’un conseiller IA pour assister la gestion commerciale.

##  Équipe du projet


* Nadia El Aabassi :Workflow & Release Manager
* Douaa MOUYASSIR  : Feature Lead
* Yassmine Soufary : AI Lead 
* Siham Loukch : Quality Lead 
* Nada El fissi : Refactoring Lead 
* Ikram MOUHSINE  : Business & Documentation Lead


##  Technologies utilisées

*  Frontend : HTML + CSS
*  Backend : Python Flask
*  Base de données : SQLite
*  API IA : clé API Grok
*  Architecture : MVC (Routes / Services / Repositories)


##  Fonctionnalités principales

 Tableau de bord

* Vue globale du stock  : nombre de plantes, stock total
* Ventes du jour
* Chiffre d’affaires du jour et total (MAD)
* Alertes de stock faible
* Raccourcis : ajouter plante, enregistrer vente, accéder à l’IA



## Gestion du stock (/plants)

* Liste des plantes du catalogue
* Ajout d’une plante (nom, espèce, prix, quantité, seuil d’alerte, description)
* Modification / suppression de plante
* Mise en évidence des stocks faibles (ex : lavande, rosier, olivier)



## Catégories (/categories)

* Liste des catégories (Plantes, Engrais, Pots, Outils…)
* Ajout, modification et suppression
* Gestion simple avec nom + description

--

## Ventes (/sales)

* Historique complet des ventes
* Ajout d’une vente (plante + client + quantité)
* Calcul automatique du total
* Mise à jour automatique du stock
* Vérification du stock avant validation
* Statistiques : CA et ventes du jour + total



## Conseiller IA (/ai)

* Analyse du stock (ruptures, réapprovisionnement)
* Recommandation de plantes selon les besoins du client
* Génération automatique de fiches produits commerciales



## Architecture du projet

* Routes (gestion des endpoints)
* Services (logique métier)
* Repositories (accès base de données)


##  Autres informations

* Interface en français
* Devise : MAD (Dirham marocain)
* Base de données locale SQLite
* Système de notifications (flash messages)


 ## Impact métier & cas d’usage réel

Cette application est conçue pour répondre à un besoin concret des pépinières :

* Réduction des pertes liées aux erreurs de stock
* Meilleur suivi des plantes à forte rotation
* Aide à la décision pour le réapprovisionnement
* Amélioration de la rentabilité grâce au suivi du chiffre d’affaires en temps réel
* Digitalisation complète d’un processus traditionnel souvent manuel

## Objectif du projet

Optimiser la gestion d’une pépinière en automatisant le suivi du stock, des ventes et en intégrant un assistant intelligent pour améliorer la prise de décision.

## Améliorations futures

* Application mobile 
* Authentification utilisateur 
* Dashboard analytics avancé 
* Export PDF des ventes 