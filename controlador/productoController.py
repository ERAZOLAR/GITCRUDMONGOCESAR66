from app import app, productos, categorias, usuarios
from flask import Flask, render_template, request, jsonify, redirect,flash, url_for, session, Request
import pymongo
import os
from bson.objectid import ObjectId
#from bson import ObjectId
from pymongo.errors import DuplicateKeyError, PyMongoError
from pymongo import MongoClient
import base64
from PIL import Image
from io import BytesIO
from bson.json_util import dumps
import threading
 
import yagmail

app.secret_key = "mxynkmdclqtnmmmk"

# CREAMOS RUTA DE INICIO funcionando
@app.route("/")
def  inicio ():
    listaProductos = productos.find()
    listaCategorias = categorias.find()
    listaP = []
    print(listaP)

    for p in listaProductos:
        categoria = categorias.find_one({'_id':ObjectId(p['categoria'])})
        #agregar atributo nuevo al producto
        if p ['categoria'] == categoria['_id']:
            p['categoria'] = categoria['nombre']
        
            #p['nombreCategoria'] =  categoria['nombre']
            listaP.append(p)
    
    return render_template("listarProductos2.html",
                           Productos = listaP,
                           #MostrarProductos = listaProductos
                           categorias=listaCategorias)



app.secret_key = "mxynkmdclqtnmmmk"

#INGRESAR POR LOGIN SESION .... PROBLEMAS SE INFORMA URL NO ENCONTRADA
@app.route("/ingreso", methods=['GET', 'POST'])
def ingreso():
     mensaje= None
     estado = False
     enviarCorreo=None
     try:
        #TRAIGO DATOS DE FROMULARIO INGRESAR.HTML
          usuario= request.form['correoBd']
          password = request.form['contrasena']
          datosConsulta = {"usuario": usuario, "password": password}
          user = usuarios.find_one(datosConsulta)
          
          if (user):
               #VALIDO DATSO PARA SESSION USUARIO AUTENTICADO
               session['usuario']= user ["usuario"]
               estado = True
               if app.config['ENV'] == 'PRODUCTION':
                email = yagmail.SMTP("erazolar@gmail.com", open(".password").read(), encoding='UTF-8')
                asunto ="Ingreso de Usuario"
                mensaje =f"Usuario  <b>{user['nombres']} \ </b> Ingreso al sistema"
                enviarCorreo = threading.Thread( target = enviarCorreo, args = (email,["erazolar@gmail.com", user['correo']], asunto, mensaje))
                enviarCorreo.start()

                #BUSCA listarProductos.html de validar credenciales
               return redirect("listarProductos2.html")
          else:
               
               mensaje = "Datos Incorrectos"

             


     except pymongo.errors as error:
            mensaje = error
# de NO validar credenciales regresa a ingreso.html
     return render_template("ingreso.html", estado = estado, mensaje = mensaje)





# AGREGAR PRODUCTO funcionando

@app.route("/vistaAgregarProducto")

def vistaAgregarProducto():
    listaCategorias = categorias.find()
    
    #print (type)(listaCategorias)
    #producto = None
    return render_template("frmAgregarProducto2.html",
                           categorias=listaCategorias,)


@app.route("/vistaActualizarProducto")

def vistaActualizarProducto():
    listaCategorias = categorias.find()
    
    #print (type)(listaCategorias)
    #producto = None
    return render_template("frmActualizarProducto2.html",
                           categorias=listaCategorias,)






@app.route("/agregarProducto", methods=['POST'])
def agregarProducto():
    mensaje = None
    estado = False
    listaCategorias=categorias.find()

    try:
        #lectura de datos que viene del formulario
        #que realiza la peticion
        codigo = int(request.form["codigo"])
        nombre = request.form["nombre"]
        precio = int(request.form["precio"])
        idCategoria = ObjectId(request.form["categoria"])
        foto = request.files["fileFoto"]
        #crear un producto de tipo diccionario para
        #agregar a la base de datos
        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "categoria": ObjectId(idCategoria)
        }

        #hacer la insercion a la base de datos
        resultado = productos.insert_one(producto)
        Productos = productos.find()
        #validar el resultado de la insercion del productoi
        if(resultado.acknowledged):
            idProducto = ObjectId(resultado.inserted_id)
            nombreFoto = f"{idProducto}.jpg"
            #de acuerdo al id del producto se carga la foto al servidor
            foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))
            mensaje = "Producto Agregado Satisfactoriamente"
            estado = True
        else:
            mensaje =  "Dificultades al Agregar el producto"

        
        return render_template("listarProductos2.html", estado = estado, mensaje = mensaje, Productos=Productos, categorias=listaCategorias)


    except pymongo.errors as error:
        mensaje = error




# EDITAR REMITE FORMULARIO PERO NO DESPLIEGA foto ... NO GUARDA CAMBIO
        
@app.route('/editar/<string:id>')
def editar_producto_template(id):
    #print(f'EL ID ES {id}')
    query_producto = {'_id': ObjectId(id)}
    producto = productos.find_one(query_producto)
    listaCategorias=categorias.find()   
    # BUSCAR PRODUCTO POR ID
    # INYECTAR PRODUCTO AL TEMPLATE EDITAR
    # PARA POBLAR CAMPOS DEL PRODUCTO

    # print (type)(listaCategorias)
    # producto = None
    
    return render_template("editar.html", producto=producto,
                           categorias=listaCategorias)


@app.route('/editar/<string:id>', methods=['POST'])
def editar_producto(id):
    listaCategorias = categorias.find()
    idCategoria = request.form["categoria"]
    mensaje = None
    estado = False
    Productos = productos.find()

    myquery = {"_id": id}
    newvalues = {
        "$set": {"codigo": request.form['codigo'], "nombre": request.form['nombre'], "precio": request.form['precio'], "categoria": ObjectId(idCategoria)}}

    productos.update_one(myquery, newvalues)
    # print (type)(listaCategorias)
    # producto = None
    return render_template("listarProductos2.html",
                           categorias=listaCategorias, estado = estado, mensaje = mensaje, Productos=Productos)

  



#ELIMINAR FUNCIONA SIN VALIDACION 

@app.route("/eliminar/<idProducto>", methods=['GET'])
def eliminar(idProducto):
      mensaje = None
      estado = False
      Productos = productos.find()
      listaCategorias=categorias.find()

      try:
          
          #SOLICITAR CONFIRMACION
          
          
          # Eliminar el producto por ID
        resultado = productos.delete_one({"_id": ObjectId(idProducto)})

          # Validar el resultado de la eliminación
        if (resultado.deleted_count):
                    mensaje = "Producto Eliminado Satisfactoriamente"
                    estado = True
        else:
                    mensaje = "Dificultades al Eliminar el producto"
          
          
        return render_template("listarProductos2.html", estado = estado, mensaje = mensaje, Productos=Productos, categorias=listaCategorias)

      except pymongo.errors as error:
          mensaje = error

















































   # resultado = productos.insert_one(producto)
    #if(resultado.acknowledged):
    #    idProducto = resultado.inserted_id
     #   nombreFoto = f"{idProducto}.jpg"
      #  foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))
       # mensaje = "Producto Agregado"
        #estado = True
    #else:
     #   mensaje="Problemas al Agregar"





    #mensaje = None
    #estado = False
    
        



# AGREGAR PRODUCTOS METODO JSON

