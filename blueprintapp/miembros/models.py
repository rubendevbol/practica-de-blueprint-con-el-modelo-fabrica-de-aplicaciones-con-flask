from blueprintapp.app import db

class Miembro(db.Model):
    __tablename__ = "miembros"
    
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    usuario_id = db.Column(db.Integer,db.ForeignKey("usuarios.id"),unique=True,nullable=True)

    usuario = db.relationship("User",back_populates="miembro")
    
    tareas = db.relationship("Tarea",back_populates="miembro",cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MIEMBRO: {self.nombre} - {self.email}>"