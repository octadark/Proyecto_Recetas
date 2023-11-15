from flask import render_template, session, redirect,request, flash
from app_flask.modelos.modelo_usuarios import Usuario
from app_flask import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/', methods=['GET'])
def despliega_login_registro():
    return render_template('login_registro.html')

@app.route('/procesa/registro', methods=['POST'])
def procesa_registro():
    if Usuario.validar_registro(request.form) == False:
        return redirect('/')
    password_encriptado = bcrypt.generate_password_hash(request.form['password'])
    nuevo_usuario = {
        **request.form,
        'password' : password_encriptado
    }
    id_usuario = Usuario.crear_uno(nuevo_usuario)
    session['id_usuario'] = id_usuario
    session['nombre'] = nuevo_usuario['nombre']
    session['apellido'] = nuevo_usuario['apellido']

    return redirect('/recetas')

@app.route('/procesa/login', methods=['POST'])
def procesa_login():
    usuario_login = Usuario.obtener_uno(request.form)
    if usuario_login == None:
        flash('Este correo no existe', 'error_login')
        return redirect('/')
    if not bcrypt.check_password_hash(usuario_login.password, request.form['password']):
        flash('Credenciales incorrectas', 'error_login')
        return redirect('/')
    session['id_usuario'] = usuario_login.id
    session['nombre'] = usuario_login.nombre
    session['apellido'] = usuario_login.apellido
    return redirect('/recetas')

@app.route('/procesa/logout', methods=['POST'])
def procesa_logout():
    session.clear()
    return redirect('/')