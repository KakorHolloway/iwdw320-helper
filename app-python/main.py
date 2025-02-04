# def carre(a):
#     return a*a
# def factorielle(a):
#     i = 1
#     result = 1
#     while i < a+1:
#         result = result * i
#         i+=1
#     return result
# def exposant(a):
#     i = 1
#     result = a
#     while i < a:
#         result = result * a
#         i+=1
#     return result

# choix = ""
# while choix.upper() != "N":
#     choixmenu = input("carre 1)\nfactorielle 2)\nexposant 3)\n")
#     while True:
#         try:
#             nombre = int(input("indiquez le nombre:\n"))
#             break
#         except ValueError:
#             print("Erreur ce n'est pas un nombre !")
#     if choixmenu == "1":
#         print(carre(nombre))
#     elif choixmenu == "2":
#         print(factorielle(nombre))
#     elif choixmenu == "3":
#         print(exposant(nombre))
#     else:
#         print("choix inconnu")
#     choix = ""
#     while choix.upper() != "N" and choix.upper() != "Y":
#         choix = input("Continuer ? Y/N\n")

from flask import Flask, jsonify, request
from Librairie import Librairie

fnac = Librairie("fnac", "36 rue de la boustifaille")
fnac.ajouter_livre(["Harry Potter", "JK Rowling"])
fnac.ajouter_livre(["La guerre des mondes", "HG Wells"])
app = Flask(__name__)

@app.route("/test")
def hello_world():
    return "Ma page html est ici"

@app.route("/librairie")
def afficher_librairie():
    dictLibrairie = {}
    dictLibrairie['nom'] = fnac.get_nom()
    dictLibrairie['adresse'] = fnac.get_adresse()
    dictLibrairie['livres'] = {}
    for livre in fnac.get_livre():
        dictLibrairie['livres'][livre[0]] = livre[1]
    return dictLibrairie, 200

@app.route("/librairie/nom")
def afficher_nom():
    return jsonify(fnac.get_nom()), 200

@app.route("/librairie/adresse")
def afficher_adresse():
    return jsonify(fnac.get_adresse()), 200

@app.route("/librairie/livres")
def afficher_livres():
    dictLivres = {}
    for livre in fnac.get_livre():
        dictLivres[livre[0]] = livre[1]
    return dictLivres, 200

@app.route("/librairie/livres", methods=['POST'])
def ajouter_livre():
    livreRequest = request.get_json()
    if livreRequest.get('titre') == None:
        return "Error with the json, titre not found", 400
    if livreRequest.get('auteur') == None:
        return "Error with the json, auteur not found", 400
    print([])
    fnac.ajouter_livre([livreRequest['titre'],livreRequest['auteur']])
    return "Book add with success", 204

@app.route("/librairie/livres", methods=['DELETE'])
def supprimer_livre():
    livreRequest = request.get_json()
    if livreRequest.get('titre') == None:
        return "Error with the json, titre not found", 400
    if livreRequest.get('auteur') == None:
        return "Error with the json, auteur not found", 400
    fnac.supprimer_livre([livreRequest['titre'],livreRequest['auteur']])
    return "Book deleted with success", 204
