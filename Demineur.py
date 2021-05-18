from random import *
import numpy as np
from PIL import Image
from os import chdir
chdir('C:/Users/vivie/Documents/Vivien/Demineur/')

"""
Niveau:   Lignes, Colonnes, Nombre de mines, Taux de réussite.
Expert:   16,     30,       99,              ~ 1%
Moyen:    16,     16,       40,              ~30%.
Débutant: 9,      9,        10,              ~60%.
"""

"""
Exemples d'appels aux fonctions :
reussite(9,9,10,1000)
aff_avancement(16,30,99,100)
charge_image(30,[[192,255,255],[128,128,255],[128,255,96],[255,255,64],[255,96,32],[255,0,32],[224,0,224],[128,0,64],[32,64,64],[192,192,192],[32,32,32]])
"""

def demineur(nb_lignes,nb_colonnes,nb_mines):
    """ Déroulement du jeu du démineur. """
    assert nb_lignes*nb_colonnes>nb_mines, 'Trop de mines'
    # Fonctions auxiliaires
    def cases_voisines(i,j):
        L=[]
        for a in [-1,0,1]:
            for b in [-1,0,1]:
                if (a,b)!=(0,0) and 0<=i+a<nb_lignes and 0<=j+b<nb_colonnes:
                    L.append((i+a,j+b))
        return L

    def placement_mines():
        k=0
        while k<nb_mines:
            i,j=randint(0,nb_lignes-1),randint(0,nb_colonnes-1)
            if not Mines[i][j]:
                Mines[i][j]=True
                k+=1

    def mines_voisines(i,j):
        L=[]
        for a,b in cases_voisines(i,j):
            if Mines[a][b]:
                L.append((a,b))
        return L

    def comptage_mines():
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                if Mines[i][j]:
                    Solution[i][j]=-1
                else:
                    Solution[i][j]=len(mines_voisines(i,j))

    def case_aleatoire(n):
        m=randint(0,n-1)
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                if not Cases_cliquees[i][j]:
                    if m==0:
                        a,b=i,j
                    m-=1
        return a,b

    def decouvrir(i,j):
        Cases_connues[i][j]=Solution[i][j]
        Cases_cliquees[i][j]=True

    def placer_drapeau(i,j):
        Cases_connues[i][j]="d"
        Cases_cliquees[i][j]=True
    # Initialisation
    Mines=[[False]*nb_colonnes for _ in range(nb_lignes)]
    Solution=[[0]*nb_colonnes for _ in range(nb_lignes)]
    Cases_cliquees=[[False]*nb_colonnes for _ in range(nb_lignes)]
    Cases_connues=[["v"]*nb_colonnes for _ in range(nb_lignes)]
    nb_drapeaux=0
    nb_cases=nb_lignes*nb_colonnes
    nb_cases_restantes=nb_cases
    placement_mines()
    comptage_mines()
    # Début de la résolution
    while True:
        x=True
        while x:
            x=False
            for i in range(nb_lignes): # Parcours de la grille
                for j in range(nb_colonnes):
                    n=Cases_connues[i][j]
                    v=0
                    d=0
                    for a,b in cases_voisines(i,j):
                        if Cases_connues[a][b]=="v":
                            v+=1
                        if Cases_connues[a][b]=="d":
                            d+=1
                    if n==v+d: # Placement drapeaux
                        for a,b in cases_voisines(i,j):
                            if Cases_connues[a][b]=="v":
                                placer_drapeau(a,b)
                                nb_cases_restantes-=1
                                nb_drapeaux+=1
                                x=True
                    if n==d: # Cases vides
                        for a,b in cases_voisines(i,j):
                            if Cases_connues[a][b]=="v":
                                decouvrir(a,b)
                                nb_cases_restantes-=1
                                x=True
        if nb_cases_restantes==nb_mines-nb_drapeaux: # Toutes les cases restantes contiennent des mines, c'est gagné !
            break
        i,j=case_aleatoire(nb_cases_restantes) # Si plus aucune indication utile, on tape au hasard
        if Mines[i][j]: # On a touché une mine, dommage :(
            break
        decouvrir(i,j)
        nb_cases_restantes-=1
        if nb_cases_restantes==nb_mines-nb_drapeaux: # Toutes les cases restantes contiennent des mines, c'est gagné !
            break
    if nb_cases_restantes==nb_mines-nb_drapeaux:
        resultat="Gagne"
    else:
        resultat="Perdu"
    return(Cases_connues,Solution,resultat,nb_cases_restantes)

def reussite(nb_lignes,nb_colonnes,nb_mines,nb_essais):
    """
    Permet d'obtenir le taux de réussite de l'algorithme de résolution pour les propriétés de grille passées en paramètre, et sur nb_essais essais.
    """
    g=0
    for i in range(nb_essais):
        connu,sol,res,a_decouvrir=demineur(nb_lignes,nb_colonnes,nb_mines)
        if res=="Gagne":
            g+=1
            # print('g')
    return 100*g/nb_essais

def aff_avancement(nb_lignes,nb_colonnes,nb_mines,nb_cases_restantes):
    """
    Affiche l'avancement de la première partie jouée victorieuse ou dont le nombre de cases non découvertes avant la défaite est inférieure à nb_cases_restantes.
    """
    def affiche_tableau(T):
        """ Pour afficher une image de la grille jouée.
        Légende: gris - non découvert
                 bleu ciel - case vide
                 bleu - 1 mine autour
                 vert - 2 mines autour
                 jaune - 3 mines autour
                 orange - 4 mines autour
                 rouge - 5 mines autour
                 rose - 6 mines autour
                 voilet - 7 mines autour
                 noir - 8 mines autour
                 gris foncé - drapeau placé """
        tab=np.uint8((np.zeros((17*nb_lignes+1,17*nb_colonnes+1,3))))
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                for a in range(16):
                    for b in range(16):
                        for c in range(3):
                            L=['0','1','2','3','4','5','6','7','d','v','-1']
                            M=[[192,255,255],[128,128,255],[128,255,96],[255,255,64],[255,96,32],[255,0,32],[224,0,224],[128,0,64],[32,64,64],[192,192,192],[32,32,32]]
                            for l in range(len(L)):
                                if str(T[i][j])==L[l]:
                                    tab[i*17+a+1][j*17+b+1][c]=M[l][c]
        return Image.fromarray(tab)
    stop=False
    while not stop:
        connu,sol,res,a_decouvrir=demineur(nb_lignes,nb_colonnes,nb_mines)
        if a_decouvrir<nb_cases_restantes:
            stop=True
    affiche_tableau(connu).show() # affiche la grille des cases découvertes
    affiche_tableau(sol).show() # affiche la grille solution
    # affiche_tableau(connu).save('grille_connue.png')
    # affiche_tableau(sol).save('solution.png')
    print(res) # partie gagnée ou perdue


def charge_image(n,couleur):
    """ Pour afficher une image avec les couleurs utilisées:
    n: hauteur de l'image
    couleur: liste des couleurs utilisées ([[192,255,255],[128,128,255],[128,255,96],[255,255,64],[255,96,32],[255,0,32],[224,0,224],[128,0,64],[32,64,64],[192,192,192],[32,32,32]]) en général."""
    c=len(couleur)
    tab=np.uint8((np.zeros((n,n*c,3))))
    for i in range(n):
        for j in range(n):
            for l in range(c):
                for k in range(3):
                    tab[i][l*n+j][k]=couleur[l][k]
    Image.fromarray(tab).show()