import flask
import json
import sqlite3
from pip._vendor import requests
#Variabke et donnees necessaires a l'API
fichier = open("benin_zones_bj_lean.json")
username =""
password =""
list_lieu = json.load(fichier)
#Importation de la base de donnees de l'API
def db_connect():
    connection = sqlite3.connect("D:\\Projets\\flask\\pays.sqlite")
    return connection

def db_req_dep():
    list_dep = []
    cur_loc = db_connect().cursor()
    cur_loc.execute("SELECT CDP,DP FROM DEP")
    list_dep = cur_loc.fetchall() 
    loc_res = {list_dep[i][0]:list_dep[i][1] for i in range(0,len(list_dep))}
    return json.dumps(loc_res)



def db_req_com (dep):
    com_list = []
    cur_dep = db_connect().cursor()
    cur_dep.execute(f"SELECT id_com,CM FROM CM WHERE id_dep = (SELECT CDP FROM DEP WHERE DP = '{dep}')")
    com_list = cur_dep.fetchall()
    #Conversion de la liste en dictionnaire
    com_res = {com_list[i][0]:com_list[i][1] for i in range(0,len(com_list))}
    return com_res
    
def db_req_arr(com):
    arr_list = []
    cur_arr = db_connect().cursor()
    cur_arr.execute(f"SELECT id_ar,AR FROM AR WHERE id_cm = (SELECT CCM FROM CM WHERE CM = '{com}'  LIMIT 1)")
    arr_list = cur_arr.fetchall()
    #Conversion de la liste en dictionnaire
    arr_res = {arr_list[i][0]:arr_list[i][1] for i in range(0,len(arr_list))}
    return arr_res

def db_req_vq(arr):
    vq_list = []
    cur_vq = db_connect().cursor()
    cur_vq.execute(f"SELECT id_com,VQ FROM VQ WHERE id_arr = (SELECT CAR FROM AR WHERE AR = '{arr}'  )")
    vq_list = cur_vq.fetchall()
    #Conversion de la liste nen dictionnaire
    vq_res = {vq_list[i][0]:vq_list[i][1] for i in range(0,len(vq_list))}
    return vq_res

def db_req(username,password):
    req = []
    cur = db_connect().cursor()
    cur.execute(f"SELECT * FROM user WHERE nom = '{username}' AND mot_de_passe = '{password}'")
    req = cur.fetchall()
    if req == []:
        return False
    return True
app = flask.Flask(__name__)
i = 0
"""while i < len(list_lieu):
    list_dep.append(list_lieu[i]["DP"])
    list_com.append(list_lieu[i]["CM"])
    list_arr.append(list_lieu[i]["AR"])
    list_qr.append(list_lieu[i]["VQ"])
    list_dep = list(set(list_dep))
    list_com = list(set(list_com))
    list_arr = list(set(list_arr))
    list_qr = list(set(list_qr))
    i += 1

def depart (dep):
    j = 0
    list_com = []
    while j < len(list_lieu) :
        if list_lieu[j]["DP"] == dep:
            list_com.append(list_lieu[j]["CM"])
        j += 1

    return list (set(list_com ))

def com (com):
    k = 0
    list_arr = []
    while k < len(list_lieu) :
        if list_lieu[k]["CM"] == com:
            list_arr.append(list_lieu[k]["AR"])
        k += 1
    return list (set(list_arr ))

def arr (arr):
    l = 0
    list_qr = []
    while l < len(list_lieu) :
        if list_lieu[l]["AR"] == arr:
            list_qr.append(list_lieu[l]["VQ"])
        l += 1
    return list (set(list_qr ))
"""
   
@app.route("/")
def login():
    return flask.render_template("index.html")
donn = []
@app.route("/login", methods = ["POST"])
def login_s():
    donn = flask.request.form
    user = donn.get("name")
    pasw = donn.get("pass")
    """if db_user.count(username) != 0:
        return json.dumps(list_dep)
    """
    db_connect()
    if db_req(user,pasw) == True :
        return "Success"
    return "Donnees non valide. Vous n'etes pas enregistré"

@app.route("/dep")
def search_com ():
    db_connect()    
    sortie_dep = db_req_dep()
    return sortie_dep

@app.route("/com")
def p_dep ():
    flask.request.args["dep"]
    db_connect()
    sortie = db_req_com(flask.request.args["dep"])
    return json.dumps(sortie)
    #return depart( flask.request.args["dep"])

@app.route("/arr")
def search_arr ():
    db_connect()
    sortie_arr = db_req_arr(flask.request.args["com"])
    return sortie_arr
    #return com( flask.request.args["com"])

@app.route("/qr")
def search_qr ():
    db_connect()
    sortie_vq = db_req_vq(flask.request.args["arr"])
    return sortie_vq
    #return arr( flask.request.args["arr"])

app.run(host='0.0.0.0', port=81)