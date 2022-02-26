from flask import Flask, flash, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mrkizmaz/Desktop/Flask-TodoApp/todo.db'
db = SQLAlchemy(app)

app.secret_key = "mirkizmaz"

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)


# anasayfa
@app.route("/")
def index():
    todos = todo.query.all()
    return render_template("index.html", todos = todos)

# todo ekleme
@app.route("/add", methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = todo(title = title, complete = False)

    db.session.add(newTodo)
    db.session.commit()
    flash(message = "Todonuz basarıyla eklendi.", category = "success")
    return redirect(url_for("index"))

# todo tamamlama
@app.route("/complete/<string:id>")
def completeTodo(id):

    toDo = todo.query.filter_by(id = id).first()
    toDo.complete = not toDo.complete
    db.session.commit()
    if toDo.complete:
        flash(message = "Tebrikler! Todonuzu tamamladınız.", category = "success")
    else:
        flash(message = "Todonuzu tamamlamadınız!", category = "danger")
    return redirect(url_for("index"))

# todo silme
@app.route("/delete/<string:id>")
def deleteTodo(id):
    toDo = todo.query.filter_by(id = id).first()
    db.session.delete(toDo)
    db.session.commit()
    flash(message = "Todonuzu sildiniz!", category = "warning")
    return redirect(url_for("index"))



if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)