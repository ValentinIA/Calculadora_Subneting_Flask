from flask import Flask, render_template, request, url_for, redirect, session
from passlib.hash import pbkdf2_sha256
import os
from pymongo import MongoClient
from Subneting import subneting
from dotenv import load_dotenv

def build():
    app=Flask(__name__)
    app.secret_key = "Secreto de estado"
    cliente=MongoClient(os.getenv("MONGODB_URI"))
    app.db = cliente.Proyecto
    coleccion = app.db.Subneting 

    @app.route("/", methods=["GET", "POST"])
    def index():
        '''
        Comprobar sesion
        if session.get("usuario"):
            return redirect(url_for("calculadora"))
        else:
            return render_template("Index.html")
        
        '''
        return redirect(url_for("calculadora"))

    @app.route("/login", methods=["GET","POST"])
    def login():

        if request.method == "POST":
                
            usuario = request.form.get("usuario")
            usuario_existe = coleccion.find_one({"usuario": usuario}, {"_id": 0})


            if usuario_existe:
                contraseña = request.form.get("contraseña")
                
                if pbkdf2_sha256.verify(contraseña, usuario_existe["contraseña"]):

                    session["usuario"]=usuario
                    print(session["usuario"])
                    return redirect(url_for("calculadora"))
                else:
                    return render_template("login.html", error="Contraseña incorrecta")
                
            else:
                    return render_template("login.html", error="Usuario no existe")
            
        return render_template("login.html")

    @app.route("/registro", methods=["GET","POST"])
    def registro():
        
        if request.method == "POST":
                
                usuario = request.form.get("usuario")
                existe = coleccion.find_one({"usuario": usuario}, {"_id": 0})


                if existe:
                    return render_template("registro.html", error=True)

                else:
                    contraseña = pbkdf2_sha256.hash(request.form.get("contraseña"))
                    parametros = {"usuario": usuario, "contraseña": contraseña}
                    app.db.Subneting.insert_one(parametros)

                    return redirect(url_for("login"))

        return render_template("registro.html")

    @app.route("/calculadora", methods=["GET","POST"])
    def calculadora():
        '''
        Comprobar sesion
        if not session.get("usuario"):
            return redirect(url_for("index"))
        '''

        resultado = None

        if request.method == "POST":
                
                ip = request.form.get("ip")
                mascara = int(request.form.get("mascara"))
                
                if ip and mascara: 
                    resultado = subneting(ip, mascara)
                    
        return render_template("calculadora.html", resultado=resultado)

    @app.route("/logout", methods=["GET","POST"])
    def logout():
        session.pop("usuario", None)
        return redirect(url_for("index"))

    return app

if __name__ == "__main__":
    app=build()
    app.run()