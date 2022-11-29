
from dbm import dumb
from flask import Flask,render_template, redirect, url_for, flash, request, jsonify
from pymysql import IntegrityError

from Models.Estado_rerserva import Estado_reservaSchema, Estado_reserva
from Models.Rol import RolSchema, Rol
from Models.Usuario import UsuarioSchema, Usuario
from Models.Tipo_habitacion import Tipo_habitacionSchema, Tipo_habitacion
from Models.Servicios import ServiciosSchema, Servicios
from Models.Estado_habitacion import Estado_habitacionSchema, Estado_habitacion
from Models.Habitacion import HabitacionSchema, Habitacion
from Models.Servicios_habitacion import Servicios_habitacionSchema, Servicios_habitacion
from Models.Reserva import ReservaSchema, Reserva
from Config.Bd import app, db
from flask_cors import CORS

import json
from urllib import response
from Config.Toke import *
from flask import Flask, request
from sqlalchemy import JSON, exc

# app=Flask(__name__,template_folder='templates')
CORS(app)

# Exceptions
@app.errorhandler(400)
def error(e):
    return errorResponse(400, "Peticion denegada")

@app.errorhandler(404)
def page_not_found(e):
    return errorResponse(404, "URL Desconocida")

@app.errorhandler(405)
def InvalidMethod(e):
    return errorResponse(405, "Metodo invalido")

@app.errorhandler(500)
def internalError(e):
    return errorResponse(500, "Error interno")

@app.errorhandler(exc.IntegrityError)
def IntegrityError(e):
    return errorResponse(409, "Error de integridad - datos invalidos")

@app.errorhandler(exc.DBAPIError)
def DBError(e):
    return errorResponse(500, "Error de la db")

@app.errorhandler(exc.SQLAlchemyError)
def DBError(e):
    return errorResponse(500, "Error de SQLAlchemy")

# @app.errorhandler(jwt.err)
# def DBError(e):
#     return errorResponse(500, "Error de SQLAlchemy")

# Raiz
@app.route('/', methods=['GET'])
def index():
    data = {
        "id" : 1010,
        "nombre": "Diego"
    }
    return render_template('index.html', datos = data)

@app.route('/habitaciones', methods=['GET'])
def indexHab():
    data = {
        "id" : 1010,
        "nombre": "Diego"
    }
    return render_template('habitaciones.html', datos = data)

@app.route('/nosotros', methods=['GET'])
def indexNos():
    data = {
        "id" : 1010,
        "nombre": "Diego"
    }
    return render_template('nosotros.html', datos = data)

@app.route('/galeria', methods=['GET'])
def indexGal():
    data = {
        "id" : 1010,
        "nombre": "Diego"
    }
    return render_template('galeria.html', datos = data)

@app.route('/servicios', methods=['GET'])
def indexServ():
    data = {
        "id" : 1010,
        "nombre": "Diego"
    }
    return render_template('servicios.html', datos = data)

# Token

@app.route('/token', methods=['GET'])
def obtenertoken():
    #var_request = json.loads(event["body"])   
    datatoken = generar_token("William", 123)   
    return datatoken

# @app.route('/verificartoken', methods=['GET'])
def verificartoken():
    token = request.headers['Authorization']
    token = token.replace("Bearer","")
    token = token.replace(" ","")
    # Call the function to validate token
    vf = verificar_token(token)
    return vf

# Finish Token

# Empieza login

@app.route('/login/<id>/<passw>', methods=['GET'])
def login(id, passw):

    usuario = Usuario.query.filter(Usuario.Cedula == id, Usuario.Contraseña == passw)
    resultUsuario = usuarios_schema.dump(usuario)
    return correctResponse(200, datos=resultUsuario)

# # Termina Login

# Comienza Usuario

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

@app.route('/usuario', methods=['GET'])
def indexCliente():
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        all_clientes = Usuario.query.all()
        resultCliente = usuarios_schema.dump(all_clientes)
        
        return correctResponse(200, datos=resultCliente)
    else:
        return jsonify(verify)


@app.route('/usuario/post', methods = ['POST'])
def savearticulo():
    # verify = verificartoken()
    # valido = verify["error"] 
    # if(valido == False):
        nombres = request.json['Nombres']
        apellidos = request.json['Apellidos']
        email = request.json['Email']
        direccion = request.json['Direccion']
        cedula = request.json['Cedula']
        celular = request.json['Celular']
        rol = request.json['Rol']
        contraseña = request.json['Contraseña']

        new_Usuario = Usuario(nombres, apellidos, email, direccion, cedula, celular, rol, contraseña)
        db.session.add(new_Usuario)
        db.session.commit()
        resultUsuario = usuario_schema.dump(new_Usuario)
        return correctResponse(200, datos=resultUsuario)
    # else:
    #     return jsonify(verify)

@app.route('/usuario/mod/<id>', methods=['PUT'])
def update_articulo(id):
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        usuario = Usuario.query.get(id)
        
        nombres = request.json['Nombres']
        apellidos = request.json['Apellidos']
        email = request.json['Email']
        direccion = request.json['Direccion']
        cedula = request.json['Cedula']
        celular = request.json['Celular']
        rol = request.json['Rol']
        contraseña = request.json['Contraseña']

        usuario.Nombres = nombres
        usuario.Apellidos = apellidos
        usuario.Email = email
        usuario.Direccion = direccion
        usuario.Cedula = cedula
        usuario.Celular = celular
        usuario.Rol = rol
        usuario.Contraseña = contraseña

        db.session.commit()
        resultUsuario = usuario_schema.dump(usuario)
        return correctResponse(200, datos=resultUsuario)
    else:
        return jsonify(verify)

@app.route('/usuario/cedula/<cedula>', methods=['GET'])
def buscar_Cliente(cedula):
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        usuario = Usuario.query.filter(Usuario.Cedula == cedula)
        resultUsuario = usuarios_schema.dump(usuario)
        return correctResponse(200, datos=resultUsuario)
    else:
        return jsonify(verify)


# Termina Usuario

# Comienza reserva

reserva_schema = ReservaSchema()
reservas_schema = ReservaSchema(many=True)

@app.route('/reservas', methods=['GET'])
def indexReservas():
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        all_reservas = Reserva.query.all()
        resultReservas = reservas_schema.dump(all_reservas)
        return correctResponse(200, datos=resultReservas)
    else:
        return jsonify(verify)

@app.route('/reservas/post', methods = ['POST'])
def saveReserva():
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        checkin = request.json['Check_in']
        checkout = request.json['Check_out']
        idHabitacion = request.json['id_habitacion']
        idUsuario = request.json['id_usuario']
        numAdultos = request.json['Num_adultos']
        numNinos = request.json['Num_ninos']
        estadoReserva = request.json['Estado_reserva']
        total = request.json['Total']

        new_Reserva = Reserva(checkin, checkout, idHabitacion, idUsuario, numAdultos, numNinos, estadoReserva, total)
        db.session.add(new_Reserva)
        db.session.commit()
        resultReservas = reserva_schema.dump(new_Reserva)
        return correctResponse(200, datos=resultReservas)
    else:
        return jsonify(verify)

@app.route('/reservas/<id>', methods = ['PUT'])
def updateReserva(id):
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        reserva = Reserva.query.get(id)

        checkin = request.json['Check_in']
        checkout = request.json['Check_out']
        idHabitacion = request.json['id_habitacion']
        idUsuario = request.json['id_usuario']
        numAdultos = request.json['Num_adultos']
        numNinos = request.json['Num_ninos']
        estadoReserva = request.json['Estado_reserva']
        total = request.json['Total']

        reserva.Check_in = checkin
        reserva.Check_out = checkout
        reserva.id_habitacion = idHabitacion
        reserva.id_usuario = idUsuario
        reserva.Num_adultos = numAdultos
        reserva.Num_ninos = numNinos
        reserva.Estado_reserva = estadoReserva
        reserva.Total = total

        db.session.commit()
        resultReservas = reserva_schema.dump(reserva)
        return correctResponse(200, datos=resultReservas)
    else:
        return jsonify(verify)

# Buscar las reservas que tenga un usuario con su CC
@app.route('/reservas/<usuario>', methods=['GET'])
def usuarioReservas(usuario):
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        res =[]
        results = db.session.query(Reserva, Usuario).join(Usuario).filter(Usuario.Cedula == usuario).all()  
        for reserva, usuario in results:
            aux = {               
                    "Nombres": usuario.Nombres + " " + usuario.Apellidos,
                    "Cedula": usuario.Cedula,
                    "Celular": usuario.Celular,
                    "id_reserva": reserva.id_reserva,
                    "num_adultos": reserva.Num_adultos,
                    "num_niños": reserva.Num_ninos,
                    "Check_in": reserva.Check_in,
                    "Check_out": reserva.Check_out,
                    "Total": reserva.Total
            }
            res.append(aux)  
        return correctResponse(200, datos=res)
    else:
        return jsonify(verify)

# Termina reserva

# Comienza Habitaciones

habitacion_schema = HabitacionSchema()
habitaciones_schema = HabitacionSchema(many=True)

# todas habitaciones
@app.route('/habitacionesGet', methods=['GET'])
def indexHabitaciones():
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        all_habitaciones = Habitacion.query.all()
        resultHabitaciones = habitaciones_schema.dump(all_habitaciones)
        return correctResponse(200, datos=resultHabitaciones)
    else:
        return jsonify(verify)

@app.route('/habitaciones/post', methods = ['POST'])
def saveHabitacion():
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        numero = request.json['Numero']
        estado = request.json['Estado']
        tipo = request.json['Tipo']

        new_habitacion = Habitacion(numero, estado, tipo)
        db.session.add(new_habitacion)
        db.session.commit()
        resultHabitaciones = habitacion_schema.dump(new_habitacion)
        return correctResponse(200, datos=resultHabitaciones)
    else:
        return jsonify(verify)

@app.route('/habitaciones/mod/<id>', methods = ['PUT'])
def updateHabitacion(id):
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        habitacion = Habitacion.query.get(id)

        # numero = request.json['Numero']
        estado = request.json['Estado']
        # tipo = request.json['Tipo']

        # habitacion.Numero = numero
        habitacion.Estado = estado
        # habitacion.Tipo = tipo

        db.session.commit()
        resultHabitacion = habitacion_schema.dump(habitacion)
        return correctResponse(200, datos=resultHabitacion)
    else:
        return jsonify(verify)

# Habitaciones disponibles
@app.route('/habitaciones/disp', methods=['GET'])
def indexHabitacionesDisp():
    # verify = verificartoken()
    # valido = verify["error"] 
    # if(valido == False):
        # all_habitaciones = Habitacion.query.filter(Habitacion.Estado == 1).all()
        # resultHabitaciones = habitaciones_schema.dump(all_habitaciones)

        res =[]
        results = db.session.query(Habitacion, Tipo_habitacion).join(Tipo_habitacion).filter(Habitacion.Tipo == Tipo_habitacion.id_tipo).all()  
        for habitacion, tipo in results:
            aux = {          
                    "id_habitacion":habitacion.id_habitacion,     
                    "Numero": habitacion.Numero ,
                    "Precio": tipo.Precio,
                    "Camas": tipo.Camas,
                    "Descripcion": tipo.Descripcion,
                    "Tipo": tipo.Nombre,
            }
            res.append(aux)  

        return correctResponse(200, datos=res   )
    # else:
    #     return jsonify(verify)

@app.route('/habitaciones/disp/<people>', methods=['GET'])
def indexHabitacionesDispPeople(people):
    # verify = verificartoken()
    # valido = verify["error"] 
    # if(valido == False):
        # all_habitaciones = Habitacion.query.filter(Habitacion.Estado == 1).all()
        # resultHabitaciones = habitaciones_schema.dump(all_habitaciones)

        res =[]
        results = db.session.query(Habitacion, Tipo_habitacion).join(Tipo_habitacion).filter(Habitacion.Tipo == Tipo_habitacion.id_tipo, Tipo_habitacion.Camas >= people, Habitacion.Estado == 1).all()  
        for habitacion, tipo in results:
            aux = {               
                    "id_habitacion":habitacion.id_habitacion,
                    "Numero": habitacion.Numero ,
                    "Precio": tipo.Precio,
                    "Camas": tipo.Camas,
                    "Descripcion": tipo.Descripcion,
                    "Tipo": tipo.Nombre,
            }
            res.append(aux)  

        return correctResponse(200, datos=res   )
    # else:
    #     return jsonify(verify)

# Servicios de una habitacion
@app.route('/habitaciones/servicios/<numero>', methods=['GET'])
def habitacionServicios(numero):
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        res ={
            "Piscina":False,
            "Spa":False,
            "Restaurante":False,
            "Gym":False
        }
        results = db.session.query(Servicios_habitacion, Habitacion, Servicios).join(Habitacion).join(Servicios).filter(Habitacion.Numero == numero).all()  
        for servicios_habitacion, habitacion, servicios in results:
            idServicio = servicios_habitacion.id_servicio_habitacion
            res[servicios.Nombre] = True
        return correctResponse(200, datos=res)
    else:
        return jsonify(verify)

# Termina Habitaciones

# Empienza Servicios

servicio_schema = ServiciosSchema()
servicios_schema = ServiciosSchema(many=True)

@app.route('/servicios', methods=['GET'])
def indexServicios():
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        all_servicios = Servicios.query.all()
        resultServicios = servicios_schema.dump(all_servicios)
        return correctResponse(200, datos=resultServicios)
    else:
        return jsonify(verify)

@app.route('/servicios/post', methods = ['POST'])
def saveServicio():
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        nombre = request.json['Nombre']

        new_Servicio = Servicios(nombre)
        db.session.add(new_Servicio)
        db.session.commit()
        resultServicios = servicio_schema.dump(new_Servicio)
        return correctResponse(200, datos=resultServicios)
    else:
        return jsonify(verify)

@app.route('/servicios/<id>', methods = ['PUT'])
def updateServicio(id):
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        servicio = Servicios.query.get(id)

        nombre = request.json['Nombre']

        servicio.Nombre = nombre

        db.session.commit()
        resultServicios = servicio_schema.dump(servicio)
        return correctResponse(200, datos=resultServicios)
    else:
        return jsonify(verify)

# Termina servicios
# ROLES 
rol_schema = RolSchema()
roles_schema = RolSchema(many=True)
@app.route('/rol', methods=['GET'])
def getRol():
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        all_rol = Rol.query.all()
        result_rol = roles_schema.dump(all_rol)
        return correctResponse(200, datos=result_rol)
    else:
        return jsonify(verify)


@app.route('/rol/<id>', methods = ['PUT'])
def update_rol(id):
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        rol = Rol.query.get(id)

        nombre = request.json['Nombre']

        rol.Nombre = nombre

        db.session.commit()
        result_rol = rol_schema.dump(rol)
        return correctResponse(200, datos=result_rol)
    else:
        return jsonify(verify)

@app.route('/rol/post', methods = ['POST'])
def insertRol():
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        nombre = request.json['Nombre']

        nuevo_rol = Rol(nombre)
        db.session.add(nuevo_rol)
        db.session.commit()
        resulRol = servicio_schema.dump(nuevo_rol)
        return correctResponse(200, datos=resulRol)
    else:
        return jsonify(verify)

@app.route('/rol/num_rol/<id_rol>', methods=['GET'])
def buscar_Rol(id_rol):
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        roles = Rol.query.filter(Rol.id_rol == id_rol)
        result_roles = roles_schema.dump(roles)
        return correctResponse(200, datos=result_roles)
    else:
        return jsonify(verify)


#Tipo de habitacion#
TipoHabitacion_schema = Tipo_habitacionSchema()
TipoHabitaciones_schema = Tipo_habitacionSchema(many=True)

@app.route('/tipHabitacion', methods=['GET'])
def insertTipHabitacion():
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        all_TipHabitacion = Tipo_habitacion.query.all()
        resultTipoCliente = TipoHabitaciones_schema.dump(all_TipHabitacion)
        
        return correctResponse(200, datos=resultTipoCliente)
    else:
        return jsonify(verify)



@app.route('/tipHabitacion/post', methods = ['POST'])
def insertTipHabitaciones():
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        nombre = request.json['Nombre']
        precio = request.json['Precio']
        camas = request.json['Camas']
        descripcion = request.json['Descripcion']

        nuevo_tipoHabitacion = Tipo_habitacion(nombre, precio, camas, descripcion)
        db.session.add(nuevo_tipoHabitacion)
        db.session.commit()
        resulTipo_Habitacion = TipoHabitacion_schema.dump(nuevo_tipoHabitacion)
        return correctResponse(200, datos=resulTipo_Habitacion)
    else:
        return jsonify(verify)



@app.route('/tipHabitacion/<id>', methods = ['PUT'])
def update_tipoHabitacion(id):
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        Tipohabitacion = Tipo_habitacion.query.get(id)

        nombre = request.json['Nombre']
        precio = request.json['Precio']
        camas = request.json['Camas']
        descripcion = request.json['Descripcion']

        Tipohabitacion.Nombre = nombre
        Tipohabitacion.Precio = precio
        Tipohabitacion.Camas = camas
        Tipohabitacion.Descripcion = descripcion

        db.session.commit()
        resulTipo_Habitaciones = TipoHabitacion_schema.dump(Tipohabitacion)
        return correctResponse(200, datos=resulTipo_Habitaciones)
    else:
        return jsonify(verify)



@app.route('/tipHabitacion/mod/<id>', methods=['GET'])
def buscar_TipoHabitacion(id):
    verify = verificartoken()
    valido = verify["error"] 
    if(valido == False):
        TipoHabitacion = Tipo_habitacion.query.filter(Tipo_habitacion.id_tipo == id)
        resulTipo_Habitaciones= TipoHabitaciones_schema.dump(TipoHabitacion)
        return correctResponse(200, datos=resulTipo_Habitaciones)
    else:
        return jsonify(verify)
5



def correctResponse(error=False,mensaje="Operación exitosa", datos=None):
    if len(datos) < 1:
        mensaje = "Informacion no encontrada"
        error = 404
    res = {
        "statusCode": error,
        "message": mensaje,
        "data": datos,
    }
    return res

def errorResponse(error,mensaje="Operación invalida", datos=None):
    res = {
        "statusCode": error,
        "message": mensaje,
        "data": datos,
    }
    return res

#Iniciamos app para que se ejecute en un puerto#
if __name__ == "__main__":
    app.run(debug=True)

# @app.route('/<id>', methods=['DELETE'])
# def delete_articulo(id):
#     articulo = Articulo.query.get(id)
#     db.session.delete(articulo)
#     db.session.commit()
#     return articulo_schema.jsonify(articulo)

# # Termina articulos


