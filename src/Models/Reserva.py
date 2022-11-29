from Config.Bd import db, ma

class Reserva(db.Model):
    __tablename__ = 'Reserva'
    id_reserva = db.Column(db.Integer, primary_key=True)
    Check_in = db.Column(db.Date())
    Check_out = db.Column(db.Date())
    id_habitacion = db.Column(db.Integer(), db.ForeignKey('Habitacion.id_habitacion'))
    id_usuario = db.Column(db.Integer(), db.ForeignKey('Usuario.id_usuario'))
    Num_adultos = db.Column(db.Integer())
    Num_ninos = db.Column(db.Integer())
    Estado_reserva = db.Column(db.Integer(), db.ForeignKey('Estado_reserva.id_estado'))
    Total = db.Column(db.Float())

    def __init__(self, Check_in, Check_out, id_habitacion, id_usuario, Num_adultos, Num_ninos, Estado_reserva, Total):
        self.Check_in = Check_in
        self.Check_out = Check_out
        self.id_habitacion = id_habitacion
        self.id_usuario = id_usuario
        self.Num_adultos = Num_adultos
        self.Num_ninos = Num_ninos
        self.Estado_reserva = Estado_reserva
        self.Total = Total

db.create_all()

class ReservaSchema(ma.Schema):
    class Meta:
        fields = ('id_reserva', 'Check_in', 'Check_out','id_habitacion', 'id_usuario', 'Estado', 'Num_adultos', 'Num_ninos', 'Estado_reserva', 'Total')
