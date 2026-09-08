class Persona:
    def __init__(self, PER_ID, PER_UUID, PER_NOMBRE, PER_SEG_NOMBRE, PER_PRI_APELLIDO, PER_SEG_APELLIDO, PER_CORREO, PER_DIRECCION, PER_IDENTIFICACION, PER_TELEFONO):
        self.PER_ID = PER_ID
        self.PER_UUID = PER_UUID
        self.PER_NOMBRE = PER_NOMBRE
        self.PER_SEG_NOMBRE = PER_SEG_NOMBRE
        self.PER_PRI_APELLIDO = PER_PRI_APELLIDO
        self.PER_SEG_APELLIDO = PER_SEG_APELLIDO
        self.PER_CORREO = PER_CORREO
        self.PER_DIRECCION = PER_DIRECCION
        self.PER_IDENTIFICACION = PER_IDENTIFICACION
        self.PER_TELEFONO = PER_TELEFONO

    def to_dic(self):
        return {
            "id": self.PER_ID,
            "uuid": self.PER_UUID,
            "nombre": self.PER_NOMBRE,
            "seg_nombre": self.PER_SEG_NOMBRE,
            "pri_apellido": self.PER_PRI_APELLIDO,
            "seg_apellido": self.PER_SEG_APELLIDO,
            "correo": self.PER_CORREO,
            "direccion": self.PER_DIRECCION,
            "identificacion": self.PER_IDENTIFICACION,
            "telefono": self.PER_TELEFONO
        }