from marshmallow import fields
from flask import jsonify
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('direccion',
                  'direccionOpcional1',
                  'direccionOpcional2',
                  'Subastas.idSubasta',
                  'Subastas.idUsuario',
                  'Subastas.idEstado',
                  'Subastas.tiempoInicial',
                  'Subastas.nombreSubasta',
                  'Subastas.precioIdeal',
                  'Subastas.fechaSubasta',
                  'Subastas_Productos.idSubasta',
                  'Subastas_Productos.idProducto',
                  'Subastas_Productos.Cantidad',
                  'Productos.nombreProducto',
                  'idProducto',
                  'idCategoria',
                  'nombreProducto',
                  'contenidoProducto',
                  'Pujas.idPuja',
                  'Pujas.precioPuja',
                  'Pujas.fechaPuja',
                  'Pujas.idUsuario',
                  'Subastas_Productos.cantidad',
                  'Productos.nombreProducto',
                  'Productos.marca',
                  'Productos.unidadMedida',
                  'Productos.cantidadPaquete',
                  'Usuarios.idUsuario',
                  'Usuarios.nombreUsuario',
                  'Usuarios.nombreComercial')


class Serializar:

    @classmethod
    def serializarDetalleSubasta(cls,datos):
        print(datos)
        arr = []
        for dato in datos:

            print("-----------------------------------------------")

            idPuja = dato[0]
            idSubasta = dato[1]
            idUsuario = dato[2]
            precioPuja = dato[3]
            fechaPuja = dato[4].strftime("%Y-%m-%d %H:%M:%S")

            SubastaIdSubasta = dato[5].idSubasta
            SubastaIdUsuario = dato[5].idUsuario
            SubastaIdEstado = dato[5].idEstado
            SubastaTiempoInicial = dato[5].tiempoInicial.strftime("%Y-%m-%d %H:%M:%S")
            SubastaNombreSubasta = dato[5].nombreSubasta
            SubastaPrecioIdeal = dato[5].precioIdeal
            SubastaFechaSubasta = dato[5].fechaSubasta.strftime("%Y-%m-%d %H:%M:%S")

            UsuarioIdUsuario = dato[6].idUsuario
            UsuarioNombreUsuario = dato[6].nombreUsuario
            UsuarioNombreComercial = dato[6].nombreComercial

            result = {
                "Pujas.idPuja":idPuja,
                "Pujas.idSubasta": idSubasta,
                "Pujas.idUsuario": idUsuario,
                "Pujas.precioPuja": precioPuja,
                "Pujas.fechaPuja": fechaPuja,
                "Subastas.idSubasta": SubastaIdSubasta,
                "Subastas.idUsuario": SubastaIdUsuario,
                "Subastas.idEstado": SubastaIdEstado,
                "Subastas.tiempoInicial": SubastaTiempoInicial,
                "Subastas.nombreSubasta": SubastaNombreSubasta,
                "Subastas.precioIdeal": SubastaPrecioIdeal,
                "Subastas.fechaSubasta": SubastaFechaSubasta,
                "Usuarios.idUsuario": UsuarioIdUsuario,
                "Usuarios.nombreUsuario": UsuarioNombreUsuario,
                "Usuarios.nombreComercial": UsuarioNombreComercial
                }
            arr.append(result)
        prueba = jsonify({"resultado":arr})
        print(prueba)

        return prueba