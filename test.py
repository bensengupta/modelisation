# -*- coding: utf-8 -*-

import modelisation as mod

# Quelques conseils:
#  - Bien formuler l'équation avec 'y = ... '
#  - Essayer d'utiliser la librairie numpy au lieu de math, ca marche mieux...

# Importer des librairies pour utilisation dans l'équation
mod.import_libraries("random as r")

mod.draw(
    modele="y = a * x + b",  # (Requise) Equation du modele, ex: 'y = a*x**2 + b*x + c'
    x=[0, 1, 2, 3, 4, 5],  # (Requise) Données x
    y=[1, 3, 5, 7, 9.5, 10.5],  # (Requise) Données y
    titre="Exemple de Modelisation",  # Titre du graphique
    legende_x="axe des abscisses",  # Titre de l'axe des abscisses
    legende_y="axe des ordonees",  # Titre de l'axe des ordonees
    grandeur_x="I",  # Grandeur de x
    grandeur_y="U",  # Grandeur de y
    cs=2,  # Chiffres significatifs du modele
    ligne_x=3,  # Dessine une ligne a x=3
    quadrillage=True,  # Affiche ou pas le quadrillage
    axes=True,  # Affiche ou pas les axes d'origine
)

mod.draw(
    modele="y = a*x**2 + b*x + c",
    x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    y=[12, 14, 18, 38, 57, 100, 130, 191, 212, 285, 423, 653, 949, 1209, 1412, 2241,],
)
mod.render(
    # Superpose les modeles, pas toujours parfait
    superposes=False,
    # Nombre de colonnes si on utilise pas superposes
    ncols=1,
)
