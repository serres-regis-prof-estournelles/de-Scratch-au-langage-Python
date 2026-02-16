# ============================================================
#  Conversion Scratch → Python
#  Projet : demander_2___2.sb3
#  Sprite  : Lutin1 (le chat)
# ============================================================
#
#  Blocs Scratch d'origine :
#
#  🚩 Quand le drapeau vert est cliqué
#     └─ demander [ 2+2=? ] et attendre
#     └─ si <réponse = 4> alors
#           dire [Exact] pendant (5) secondes
#        sinon
#           dire [Faux]  pendant (5) secondes
#
# ============================================================

import time


def dire(message: str, duree: float) -> None:
    """Équivalent du bloc 'dire [...] pendant (n) secondes'."""
    print(f"💬 Le lutin répond : {message}")
    time.sleep(duree)


def main() -> None:
    # --- Quand le drapeau vert est cliqué ---

    # Bloc : demander [ 2+2=? ] et attendre
    reponse = input(" 2+2=? ")

    # Bloc : si <réponse = 4> alors / sinon
    if reponse == "4":
        dire("Exact", 5)
    else:
        dire("Faux", 5)


if __name__ == "__main__":
    main()
