from Config.Bd import db, ma

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    Nombres = db.Column(db.String(70))
    Apellidos = db.Column(db.String(70))
    Email = db.Column(db.String(70))
    Direccion = db.Column(db.String(70))
    Cedula = db.Column(db.Integer())
    Celular = db.Column(db.BigInteger())
    Rol = db.Column(db.Integer(), db.ForeignKey('Rol.id_rol'))
    Contraseña = db.Column(db.String(70))

    def __init__(self, Nombres, Apellidos, Email, Direccion, Cedula, Celular, Rol, Contraseña):
        self.Nombres = Nombres
        self.Apellidos = Apellidos
        self.Email = Email
        self.Direccion = Direccion
        self.Cedula = Cedula
        self.Celular = Celular
        self.Rol = Rol
        self.Contraseña = Contraseña

db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Nombres', 'Apellidos', 'Email', 'Direccion', 'Cedula', 'Celular', 'Rol', 'Contraseña')
