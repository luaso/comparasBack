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
    def serializarDetalleSubasta(cls, datos):
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

    @classmethod
    def serializarDetalleSubasta2(cls, pujas, subastas):
        arr = []
        for puja in pujas:
            print("-----------------------------------------------")

            precioPuja = puja[0]
            idUsuario = puja[1]

            for subasta in subastas:

                if (precioPuja == subasta[0].precioPuja and idUsuario == subasta[0].idUsuario):
                    idPuja = subasta[0].idPuja
                    idSubasta = subasta[0].idSubasta
                    fechaPuja = subasta[0].fechaPuja.strftime("%Y-%m-%d %H:%M:%S")

                    SubastaIdSubasta = subasta[1].idSubasta
                    SubastaIdUsuario = subasta[1].idUsuario
                    SubastaIdEstado = subasta[1].idEstado
                    SubastaTiempoInicial = subasta[1].tiempoInicial.strftime("%Y-%m-%d %H:%M:%S")
                    SubastaNombreSubasta = subasta[1].nombreSubasta
                    SubastaPrecioIdeal = subasta[1].precioIdeal
                    SubastaFechaSubasta = subasta[1].fechaSubasta.strftime("%Y-%m-%d %H:%M:%S")

                    UsuarioIdUsuario = subasta[2].idUsuario
                    UsuarioNombreUsuario = subasta[2].nombreUsuario
                    UsuarioNombreComercial = subasta[2].nombreComercial

            result = {
                "Pujas.idPuja": idPuja,
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
        prueba = jsonify({"resultado": arr})
        print(arr)

        return prueba