# Librerias a usar en el modulo
from flask import request, render_template, redirect, url_for, Blueprint, flash

# Referencia a la base de datos
from blueprintapp.app import db
# Modelos con los que interactura el modulo
from blueprintapp.tareas.models import Tarea

bp_tarea = Blueprint('bp_tarea',__name__,template_folder='templates')

@bp_tarea.route("/")
def index():
    tareas = Tarea.query.all()
    return render_template('tareas/index.html',tareas=tareas)

@bp_tarea.route("/create",methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('tareas/create.html')
    descripcion = request.form.get('descripcion', '').strip()
    completado = 'completado' in request.form.keys()

    if not descripcion:
        flash('Debes completar la descripción para crear la tarea.', 'warning')
        return render_template('tareas/create.html', descripcion=descripcion, completado=completado), 400

    tarea = Tarea(descripcion=descripcion, completado=completado)
    db.session.add(tarea)
    db.session.commit()
    flash('Tarea creada correctamente.', 'success')
    return redirect(url_for('bp_tarea.index'))


@bp_tarea.route("/editar/<int:id>", methods=["GET", "POST"])
def edit(id):
    tarea = Tarea.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('tareas/edit.html', tarea=tarea)

    descripcion = request.form.get('descripcion', '').strip()
    completado = 'completado' in request.form.keys()

    if not descripcion:
        flash('Debes completar la descripción para actualizar la tarea.', 'warning')
        return render_template('tareas/edit.html', tarea=tarea), 400

    tarea.descripcion = descripcion
    tarea.completado = completado
    db.session.commit()
    flash('Tarea actualizada correctamente.', 'success')
    return redirect(url_for('bp_tarea.index'))


@bp_tarea.route("/eliminar/<int:id>", methods=["POST"])
def delete(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    flash('Tarea eliminada correctamente.', 'success')
    return redirect(url_for('bp_tarea.index'))




