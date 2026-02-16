import random

# Jeu : Trouver le nombre
# Converti depuis Scratch (jeu_trouver_nombre.sb3)

# Initialisation des variables
A = 0   # nombre proposé par le joueur
C = 0   # compteur de tentatives

# Tirage d'un nombre aléatoire entre 1 et 1000
B = random.randint(1, 1000)

# Boucle jusqu'à ce que le joueur trouve le bon nombre
while A != B:
    A = int(input("Donner un nombre compris entre 1 et 1000 : "))
    C = C + 1

    if A == B:
        print("Gagné !")
    elif A < B:
        print("Trop petit !")
    else:
        print("Trop grand !")

# Affichage du nombre de tentatives
print("Nombre de réponses pour gagner :")
print(C)
