from blueprintapp.app import db
from flask_login import UserMixin

Column = db.Column

class User(db.Model,UserMixin ):
    __tablename__ = "usuarios"
    
    id = Column(db.Integer, primary_key = True)
    username = Column(db.String(20), nullable=False, unique=True)
    password = Column(db.String(255), nullable=False)
    rol = Column(db.String(20), default="user")
    miembro = db.relationship("Miembro", back_populates="usuario", uselist=False)