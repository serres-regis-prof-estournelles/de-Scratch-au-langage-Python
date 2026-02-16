import random

# Tirage aléatoire : combien de tirages pour que A égale B ?
# Converti depuis Scratch (.sb3)

# Initialisation
A = 0
B = 1  # valeurs différentes pour entrer dans la boucle
C = 0  # compteur de tirages

# Boucle : on tire A et B au hasard à chaque tour jusqu'à ce que A == B
while A != B:
    A = random.randint(1, 10000)
    B = random.randint(1, 10000)
    C = C + 1

# Affichage du résultat
print(f"A = {A}, B = {B}")
print(f"Nombre de tirages nécessaires pour que A = B : {C}")
