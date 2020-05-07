# -*- coding: utf-8 -*-
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from sys import version_info
from scipy.optimize import curve_fit
from .gen_func import Function

precision = 100
graphs, error = [], False
libraries = ["np"]


def import_libraries(*libs):
    """
    Importe une ou plusieurs librairies pour utilisation dans le modèle.

    Note: np est déja importé

    ## Exemples

    - `import_libraries("random", "numpy as np")`
    """
    global error
    for lib in libs:
        # Ajoute l'alias à la liste librairies pour pouvoir le détecter dans le modèle
        libraries.append(lib.split("as")[0] if "as" in lib else lib)
        try:
            exec("import {}".format(lib), globals())
        except:
            print("ERREUR: Librairie '{}' introuvable".format(lib))
            error = True


def draw(
    modele,
    x,
    y,
    cs=3,
    axes=True,
    quadrillage=False,
    titre="",
    legende_x="",
    legende_y="",
    grandeur_x="x",
    grandeur_y="y",
    ligne_x=None,
):
    """
    Trace une courbe selon le modèle et les données x et y.

    Note: Pour voir la courbe, il faut faire `render()`.

    ## Exemples

    - `draw('y = a * x + b', [1, 2, 3, 4, 5], [3, 5, 7, 9, 11])`
    - `draw('y = a * x ** 2 + b * x + c', [1, 2, 3, 4, 5], [3, 2, 7, 8, 12])`

    ## Paramètres

    #### Requises:
    - modele (string): Équation du modèle en language python (avec des contantes a une lettre)
    - x (list): Données experimentales
    - y (list): Données experimentales

    #### Optionnels:
    - cs (int): Chiffres significatifs du modèle
    - quadrillage (boolean): Si le quadrillage est affiché (défaut: False)
    - axes (boolean): Si les axes x et y sont affichés (défaut: True)
    - titre (string): Titre du modèle
    - legende_x (string): Étiquette de l'axe des abscisses
    - legende_y (string): Étiquette de l'axe des ordonees
    - grandeur_x (string): Grandeur de l'axe des abscisses (ex: 't' ou 'h')
    - grandeur_y (string): Grandeur de l'axe des abscisses (ex: 'g(x)' ou 'U(g)')
    - ligne_x (int): Trace une ligne pour déterminer l'image d'un antécedant
    """
    global error

    #################################### TESTS ####################################
    # Vérifie pour des erreurs encontrés precedamment, si il y en a, quitte la fonction
    if error:
        return "error"

    try:
        x, y = np.array(x), np.array(y)
    except:
        print(
            """ERREUR: Les paramètres 'x' et 'y' doivent être des listes non-vides contenant vos données expérimentales
Exemple: x=[1, 2, 3] et y=[1, 4, 9]
votre x={}
votre y={}""".format(
                x, y
            )
        )
        error = True

    # Vérifie que modèle est un string
    if not isinstance(modele, str):
        print(
            """ERREUR: Votre paramètre 'modele' ({}) doit être un string non-nul avec une équation en language python avec des constantes à une lettre
Exemple: modele='y = a * x ** 2 + b * x + c' ou modele='y = a * x + b'""".format(
                modele
            )
        )
        error = True
    # Verifie que x et y ne sont pas vides
    elif (x.size == 0 or y.size == 0) or (x.size != y.size):
        print(
            """ERREUR: Les paramètres 'x' et 'y' doivent contenir au moins un item et doivent contenir le même nombre de données
Exemple: x=[1, 2, 3] ey y=[1, 4, 9]
votre x contient {} items
votre y contient {} items""".format(
                x.size, y.size
            )
        )
        error = True

    elif modele.find("=") == -1:
        print(
            "ERREUR: Votre equation '{}' ne contient pas de signe '=', votre modele doit etre sous la forme 'y=m*x+p'".format(
                modele
            )
        )
        error = True
    elif modele.split("=")[0].replace(" ", "") != "y":
        print(
            "ERREUR: Votre equation '{}' doit contenir 'y' à gauche du signe égal, pas '{}'".format(
                modele
            )
        )
        error = True

    # Si on est en python 2.7, utilise des string unicode
    if version_info[0] < 3:
        modele = unicode(modele, "utf-8")
        titre = unicode(titre, "utf-8")
        legende_x = unicode(legende_x, "utf-8")
        legende_y = unicode(legende_y, "utf-8")
        grandeur_x = unicode(grandeur_x, "utf-8")
        grandeur_y = unicode(grandeur_y, "utf-8")

    # Ajoute le graphique a la liste de graphiques
    graphs.append(
        (
            modele,
            x,
            y,
            titre,
            legende_x,
            legende_y,
            grandeur_x,
            grandeur_y,
            ligne_x,
            cs,
            quadrillage,
            axes,
        )
    )


def round_cs(num, cs=2):
    return round(num, cs - int(np.floor(np.log10(abs(num)))) - 1)


def render(superposes=False, ncols=None):
    """
    Affiche la (ou les) courbe(s) definis avec draw().
    
    Note: Avec `superposes=True`, les titres et étiquettes de votre dernier `draw()` auront priorité sur les autres.

    ## Exemples
    
    - `render()`
    - `render(plot_par_rangee=3)`
    - `render(superposes=True)`

    ## Parametres
    
    - ncols (int): Nombre de colonnes
    - superposes (boolean): Si les deux graphiques sont superposés (défaut: False)
    """
    # Vérifie pour des erreurs encontres precedamment, si il y en a, quitte la fonction
    if error:
        return "error"

    # Calcul du nombre de colonnes et de rangées pour les subplots
    if not ncols:
        ncols = len(graphs) // 3 + 1

    num = 100 * np.ceil(len(graphs) / ncols) + 10 * ncols + 1

    plt.subplots_adjust(
        left=0.125, bottom=0.05, right=0.9, top=0.95, wspace=0.2, hspace=0.4
    )

    for graph in graphs:
        modele, x, y, titre, legende_x, legende_y, grandeur_x, grandeur_y, ligne_x, cs, quadrillage, axes = graph
        # Sépare les deux graphes si on ne superpose pas
        if not superposes:
            plt.subplot(num)

        # Déssine les points des données expérimentales
        plt.plot(x, y, "+")

        # Si on precise un titre, legende_x ou legende_y, applique les
        if titre and not superposes:
            plt.title(titre)
        if legende_x:
            plt.xlabel(legende_x)
        if legende_y:
            plt.ylabel(legende_y)
        if quadrillage:
            plt.grid()
        if axes:
            plt.axvline(x=0, color="k", linewidth=1)
            plt.axhline(y=0, color="k", linewidth=1)

        try:
            f = Function(modele, libraries)
        except:
            print(
                """ERREUR: Le programme ne comprend pas votre équation ({})
Problèmes possibles:
 - vous avez un caractère non-compris par python (ex: ^ au lieu de **)
 - vous avez mis côte-à-côte un numéro et lettre (ex: 3x au lieu de 3*x)
 - vous utilisez une virgule au lieu d'un point (ex: 3,1 au lieu de 3.1)
 """.format(
                   modele
                )
            )
            return "error"

        # Valeurs x du modèle. On cherche a tracer une ligne aussi lisse que possible,
        # donc il nous faut beaucoup de points entre xmin et xmax
        if ligne_x:
            xmin = min(min(x), ligne_x, 0) * 1.1
            xmax = max(max(x), ligne_x) * 1.1
        else:
            xmin = min(min(x), 0) * 1.1
            xmax = max(x) * 1.1
        modele_x = np.linspace(xmin, xmax, precision)

        # Si f.no_fit == True, on skip curve_fit()
        # curve_fit determine les valeures de constantes dans une fonction python
        negative_x = True if min(x) < 0 else False
        modele_y, negative_y = [], False
        if not f.no_fit:
            f.set_params(curve_fit(f.real_func, x, y)[0])
            print(np.all(np.isfinite(curve_fit(f.real_func, x, y)[1])))
        for i in modele_x:
            res = f.func(i)
            if res < 0:
                negative_y = True
            modele_y.append(res)
        
        residuals = np.array([
            yval - f.func(xval) for xval, yval in zip(x, y)
        ])
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        cc = str(round_cs(r_squared, 4))

        if not negative_x:
            plt.xlim(0)
        if not negative_y:
            plt.ylim(0)

        # Si une abscisse est donnée, tracer la ligne correspondante pour trouver l'ordonée
        if ligne_x:
            plt.vlines(ligne_x, 0, f.func(ligne_x), color="b")
            plt.hlines(f.func(ligne_x), 0, ligne_x, color="b")

        label = modele.replace("y", grandeur_y, 1)

        f.stripped = f.stripped.rjust(len(label))
        for param, letter in zip(f.params, f.letters):
            while letter in f.stripped:
                val = str(round_cs(param, cs))
                index = f.stripped.find(letter)
                f.stripped = (
                    f.stripped[:index] + " " * len(val) + f.stripped[index + 1 :]
                )
                label = label[:index] + val + label[index + 1 :]
        index = f.stripped.find("x")
        if index != -1:
            label = label[:index] + grandeur_x + label[index + 1 :]
        label = u"Modèle: " + label

        # Affiche un appercu dans la console
        print("========================= NOUVEAU GRAPHIQUE =========================")
        print(
            "Modèle tracé à partir de l'équation '{}' avec {} inconnus ({})".format(
                modele, len(f.letters), ", ".join(f.letters)
            )
        )
        print(" - " + label)
        print(" - " + u"R\u00B2 = " + cc)

        label += u"\nR\u00B2 = " + cc
        if superposes:
            label = titre + "\n" + label
        plt.plot(modele_x, modele_y, label=label)
        plt.legend()
        num += 1
    plt.show()
