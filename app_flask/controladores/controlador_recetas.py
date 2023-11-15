from flask import render_template, request, redirect, session
from app_flask.modelos.modelo_recetas import Receta
from app_flask import app

@app.route('/recetas', methods=['get'])
def desplegar_recetas():
    if "id_usuario" not in session:
        return redirect('/')
    lista_recetas = Receta.obtener_todos()
    return render_template('recetas.html', lista_recetas = lista_recetas)

@app.route('/formulario/receta', methods=['GET'])
def desplegar_formulario_receta():
    if "id_usuario" not in session:
        return redirect('/')
    return render_template('formulario_receta.html')

@app.route('/crear/receta', methods=['POST'])
def crear_receta():
    if Receta.validar_receta(request.form) == False:
        return redirect('/formulario/receta')
    nueva_receta = {
        **request.form,
        "id_usuario": session['id_usuario']
    }
    Receta.crear_uno(nueva_receta)
    return redirect('/recetas')

@app.route('/eliminar/receta/<int:id>', methods=['POST'])
def eliminar_receta(id):
    receta = {
        "id": id
    }
    Receta.elimina_uno(receta)
    return redirect('/recetas')

@app.route('/formulario/editar/receta/<int:id>', methods=['GET'])
def despliega_formulario_editar_receta(id):
    if "id_usuario" not in session:
        return redirect('/')
    datos = {
        "id" : id
    }
    receta = Receta.obtener_uno(datos)
    print(receta.formato_fecha())
    return render_template('formulario_editar_receta.html', receta = receta)

@app.route('/editar/receta/<int:id>', methods=['POST'])
def editar_receta(id):
    if Receta.validar_receta(request.form) == False:
        return redirect(f'/formulario/editar/receta/{id}')
    editar_receta = {
        **request.form,
        "id" : id,
        "id_usuario" : session['id_usuario']
    }
    Receta.actualizar_uno(editar_receta)
    return redirect('/recetas')

@app.route('/detalle/receta/<int:id>', methods=['GET'])
def desplegar_detalle_receta(id):
    if "id_usuario" not in session:
        return redirect('/')
    datos = {
        "id" : id
    }
    receta = Receta.obtener_uno_con_usuario(datos)
    return render_template('detalle_receta.html', receta = receta)
