# Librerias a usar en el modulo
from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required

# Referencia a la base de datos
from blueprintapp.app import db
# Modelos con los que interactura el modulo
from blueprintapp.miembros.models import Miembro
from blueprintapp.tareas.models import Tarea

bp_tarea = Blueprint('bp_tarea',__name__,template_folder='templates')

@bp_tarea.route("/")
@login_required
def index():
    tareas = Tarea.query.all()
    return render_template('tareas/index.html',tareas=tareas)

@bp_tarea.route("/create",methods=['GET','POST'])
@login_required
def create():
    miembros = Miembro.query.all()

    if request.method == 'GET':
        return render_template('tareas/create.html', miembros=miembros)
    descripcion = request.form.get('descripcion', '').strip()
    completado = 'completado' in request.form.keys()
    miembro_id = request.form.get('miembro_id', type=int)

    if not descripcion or not miembro_id:
        flash('Debes completar la descripción para crear la tarea.', 'warning')
        return render_template('tareas/create.html', descripcion=descripcion, completado=completado, miembro_id=miembro_id, miembros=miembros), 400

    miembro = Miembro.query.get(miembro_id)

    if not miembro:
        flash('Debes seleccionar un miembro válido.', 'warning')
        return render_template('tareas/create.html', descripcion=descripcion, completado=completado, miembro_id=miembro_id, miembros=miembros), 400

    tarea = Tarea(descripcion=descripcion, completado=completado, miembro_id=miembro_id)
    db.session.add(tarea)
    db.session.commit()
    flash('Tarea creada correctamente.', 'success')
    return redirect(url_for('bp_tarea.index'))


@bp_tarea.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    tarea = Tarea.query.get_or_404(id)
    miembros = Miembro.query.all()

    if request.method == 'GET':
        return render_template('tareas/edit.html', tarea=tarea, miembros=miembros)

    descripcion = request.form.get('descripcion', '').strip()
    completado = 'completado' in request.form.keys()
    miembro_id = request.form.get('miembro_id', type=int)

    if not descripcion or not miembro_id:
        flash('Debes completar la descripción para actualizar la tarea.', 'warning')
        return render_template('tareas/edit.html', tarea=tarea, descripcion=descripcion, completado=completado, miembro_id=miembro_id, miembros=miembros), 400

    miembro = Miembro.query.get(miembro_id)

    if not miembro:
        flash('Debes seleccionar un miembro válido.', 'warning')
        return render_template('tareas/edit.html', tarea=tarea, descripcion=descripcion, completado=completado, miembro_id=miembro_id, miembros=miembros), 400

    tarea.descripcion = descripcion
    tarea.completado = completado
    tarea.miembro_id = miembro_id
    db.session.commit()
    flash('Tarea actualizada correctamente.', 'success')
    return redirect(url_for('bp_tarea.index'))


@bp_tarea.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def delete(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    flash('Tarea eliminada correctamente.', 'success')
    return redirect(url_for('bp_tarea.index'))




