from app import app, categorias
from flask import Flask, render_template, request, jsonify, redirect
import pymongo

#CREAMOS RUTA PARA LISTAR CATEGORIAS
@app.route("/listarProductos")
def listarProductos():
    listaCategorias = categorias.find()
    return render_template("listarProductos2.html", categorias=listaCategorias)

#CREAMOS RUTA PARA AGREGAR CATEGORIAS
@app.route("/vistaAgregarCategoria")
def vistaAgregarCategoria():
    return render_template("frmAgregarCategoria.html")

#CREAMOS RUTA PARA AGREGAR CATEGORIAS
@app.route("/agregarCategoria", methods=['POST'])
def agregarCategoria():
    mensaje = None
    estado = False
    try:
        nombre = request.form["nombre"]
        #CREAMOS UN DICTIONARIO PARA GUARDAR LA CATEGORIA
        categoria = {
            "nombre": nombre
        }
        #GUARDAMOS LA CATEGORIA EN LA BASE DE DATOS
        resultado = categorias.insert_one(categoria)
        if resultado.acknowledged:
            mensaje = "Categoria Agregada Satisfactoriamente"
            estado = True
        else:
            mensaje = "Dificultades al Agregar la Categoria"
    except pymongo.errors as error:
        mensaje = error

    return render_template("listarCategorias.html", estado=estado, mensaje=mensaje, categorias=categorias)

#CREAMOS RUTA PARA MODIFICAR CATEGORIAS
@app.route("/vistaModificarCategoria/<idCategoria>", methods=['GET'])
def vistaModificarCategoria(idCategoria):
    categoria = categorias.find_one({"_id": ObjectId(idCategoria)})
    return render_template("frmModificarCategoria.html", categoria=categoria)

#CREAMOS RUTA PARA ACTUALIZAR CATEGORIAS
@app.route("/actualizarCategoria", methods=['POST'])
def actualizarCategoria():
    mensaje = None
    estado = False
    try:
        idCategoria = ObjectId(request.form["idCategoria"])
        nombre = request.form["nombre"]
        #CREAMOS UN DICTIONARIO PARA ACTUALIZAR LA CATEGORIA
        categoriaActualizada = {
            "nombre": nombre
        }
        #ACTUALIZAMOS LA CATEGORIA EN LA BASE DE DATOS
        resultado = categorias.update_one({"_id": idCategoria}, {"$set": categoriaActualizada})
        if resultado.modified_count > 0:
            mensaje = "Categoria Modificada Satisfactoriamente"
            estado = True
        else:
            mensaje = "Dificultades al Modificar la Categoria"
    except pymongo.errors as error:
        mensaje = error

    return render_template("listarCategorias.html", estado=estado, mensaje=mensaje, categorias=categorias)

#CREAMOS RUTA PARA ELIMINAR CATEGORIAS
@app.route("/eliminarCategoria/<idCategoria>", methods=['GET'])
def eliminarCategoria(idCategoria):
    mensaje = None
    estado = False
    try:
        #ELIMINAMOS LA CATEGORIA DE LA BASE DE DATOS
        resultado = categorias.delete_one({"_id": ObjectId(idCategoria)})
        if resultado.deleted_count > 0:
            mensaje = "Categoria Eliminada Satisfactoriamente"
            estado = True
        else:
            mensaje = "Dificultades al Eliminar la Categoria"
    except pymongo.errors as error:
        mensaje = error

    return render_template("listarCategorias.html", estado=estado, mensaje=mensaje, categorias=categorias)
            

