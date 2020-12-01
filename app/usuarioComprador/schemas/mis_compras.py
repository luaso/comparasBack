from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('Subastas.idSubasta',
                  'Usuarios.nombreUsuario',
                  'Usuarios.apellidoPatUsuario',
                  'Subastas.fechaSubasta',
                  'Pujas.precioPuja',
                  'Pujas.fechaPuja',
                  'Pujas.idSubasta')

class TaskSchema2(ma.Schema):
    class Meta:
        fields = ('Productos.nombreProducto',
                  'Productos.idProducto',
                  'Productos.marca',
                  'Productos.unidadMedida',
                  'Productos.cantidadPaquete')

class TaskSchema3(ma.Schema):
    class Meta:
        fields = ('Usuarios.idUsuario',
                  'Usuarios.nombreUsuario',
                  'Usuarios.apellidoPatUsuario',
                  'Pujas.precioPuja')