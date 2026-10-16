#!/usr/bin/env python3
"""
Interroge une URL en boucle pendant une durée donnée, puis affiche
le nombre de requêtes effectuées.

Usage :
    python3 compteur_requetes.py <url> <durée_en_secondes> [--timeout N]

Exemple :
    python3 compteur_requetes.py http://localhost:8080/ 10
"""

import argparse
import sys
import time
import urllib.error
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Interroge une URL pendant une durée donnée et compte les requêtes."
    )
    parser.add_argument("url", help="URL à interroger (http:// ou https://)")
    parser.add_argument("duree", type=float, help="Durée du test en secondes")
    parser.add_argument(
        "--timeout", type=float, default=5.0,
        help="Délai maximal par requête en secondes (défaut : 5)",
    )
    args = parser.parse_args()

    if args.duree <= 0:
        parser.error("la durée doit être strictement positive")

    total = succes = erreurs = 0
    debut = time.monotonic()
    fin = debut + args.duree

    print(f"Interrogation de {args.url} pendant {args.duree:g} s...")

    try:
        while time.monotonic() < fin:
            total += 1
            try:
                with urllib.request.urlopen(args.url, timeout=args.timeout) as rep:
                    rep.read()  # consomme la réponse pour libérer la connexion
                    succes += 1
            except urllib.error.HTTPError:
                erreurs += 1  # réponse reçue mais code 4xx/5xx
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
                erreurs += 1  # serveur injoignable, délai dépassé, etc.
    except KeyboardInterrupt:
        print("\nInterrompu par l'utilisateur.")

    ecoule = time.monotonic() - debut

    print(f"Requêtes effectuées : {total}")
    print(f"  - réussies (2xx/3xx) : {succes}")
    print(f"  - en erreur          : {erreurs}")
    print(f"Durée réelle         : {ecoule:.2f} s")
    if ecoule > 0:
        print(f"Débit moyen          : {total / ecoule:.1f} req/s")

    return 0 if erreurs == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
