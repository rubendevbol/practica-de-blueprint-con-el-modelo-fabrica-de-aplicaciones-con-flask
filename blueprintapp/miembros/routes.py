# Librerias a usar en el modulo
from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required

# Referencia a la base de datos
from blueprintapp.app import db
# Modelos con los que interactura el modulo
from blueprintapp.miembros.models import Miembro

bp_miembro = Blueprint('bp_miembro',__name__,template_folder='templates')

@bp_miembro.route("/")
@login_required
def index():
    miembros = Miembro.query.all()
    return render_template('miembro/index.html',miembros=miembros)

@bp_miembro.route("/create",methods=['GET','POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('miembro/create.html')
    nombre = request.form.get('nombre', '').strip()
    email = request.form.get('email', '').strip()

    if not nombre or not email:
        flash('Debes completar nombre y correo para crear el miembro.', 'warning')
        return render_template('miembro/create.html', nombre=nombre, email=email), 400

    miembro = Miembro(nombre=nombre, email=email)
    db.session.add(miembro)
    db.session.commit()
    flash('Miembro creado correctamente.', 'success')
    return redirect(url_for('bp_miembro.index'))


@bp_miembro.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    miembro = Miembro.query.get_or_404(id)

    if request.method == "GET":
        return render_template('miembro/edit.html', miembro=miembro)

    nombre = request.form.get("nombre", '').strip()
    email = request.form.get("email", '').strip()

    if not nombre or not email:
        flash('Debes completar nombre y correo para actualizar el miembro.', 'warning')
        return render_template('miembro/edit.html', miembro=miembro), 400

    miembro.nombre = nombre
    miembro.email = email
    db.session.commit()
    flash('Miembro actualizado correctamente.', 'success')
    return redirect(url_for('bp_miembro.index'))


@bp_miembro.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def delete(id):
    miembro = Miembro.query.get_or_404(id)
    db.session.delete(miembro)
    db.session.commit()
    flash('Miembro eliminado correctamente.', 'success')
    return redirect(url_for('bp_miembro.index'))




