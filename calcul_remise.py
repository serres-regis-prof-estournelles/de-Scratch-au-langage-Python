# Calcul de remise
# Converti depuis Scratch (calcul_remise.sb3)

# Demander le montant de la commande
M = float(input("Montant de la commande ? "))

# Calculer la remise selon le montant
if M < 30000:
    taux = 1
    R = M * (1 / 100)
    print("Taux de remise : 1 %")
else:
    taux = 2
    R = M * (2 / 100)
    print("Taux de remise : 2 %")

# Afficher le montant de la remise
print("Montant de la remise")
print(R, "euros")
