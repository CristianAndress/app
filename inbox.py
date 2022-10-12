from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, send_file
)

from app.auth import login_required
from app.db import get_db

bp = Blueprint('inbox', __name__, url_prefix='/inbox')

@bp.route("/getDB")
@login_required
def getDB():
    return send_file(current_app.config['DATABASE'], as_attachment=True)


@bp.route('/show')
@login_required
def show():
    db = get_db()
    messages = db.execute(
        "select * from message"#####
    ).fetchall() #trae todos los registros seleccionados en el select anterior

    return render_template("inbox/show.html", messages=messages)#####


@bp.route('/send', methods=('GET', 'POST'))
@login_required
def send():
    if request.method == 'POST':        
        from_id = g.user['id']
        to_username = request.form["to"]####
        subject = request.form["subject"]
        body = request.form["body"]

        db = get_db()
       
        if not to_username:
            flash('To field is required')
            return render_template('inbox/send.html')
        
        if not subject:
            flash('Subject field is required')
            return render_template('inbox/send.html')
        
        if not body:
            flash('Body field is required')
            return render_template('inbox/send.html')    
        
        error = None    
        userto = None 
        
        #aqui se va a validar que el usuario si exista como usuario
        userto = db.execute(
            "select * from message where username = ?", (to_username,) ##### select * from message where username = ?. se coloca interrogacion para indicarle que va a recibir un parametro, en esta caso to_username
        ).fetchone()
        
        if userto is None:
            error = 'Recipient does not exist'
     
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "Insert into message (from_id, to_id, subject, body) values (?,?,?,?)", #####
                (g.user['id'], userto['id'], subject, body)
            )
            db.commit() #para confirmar los cambios a nivel de base de datos. si no se pone esto no se hacen los cambios. los cambios quedan de forma permanente

            return redirect(url_for('inbox.show'))

    return render_template('inbox/send.html')