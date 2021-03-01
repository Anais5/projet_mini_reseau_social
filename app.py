from flask import Flask, url_for, request, redirect, render_template
from outils.data_base import DataBase
from outils.settings import DATABASE, DB_NAME

app = Flask(__name__, template_folder='templates')
db = DataBase(DB_NAME, DATABASE)

#page d'accueil
@app.route('/', methods=["GET", "POST"])
def accueil():
    return render_template('accueil.html', articles=db.recuperer_articles())

@app.route('/ajouter', methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        titre = request.form["titre"]
        contenu = request.form["contenu"]
        if titre and contenu:
            db.inserer_article(1, titre, contenu)
            return redirect(url_for('accueil'))

    return """
    <form method="post">
        Titre: <input name="titre"/><br/>
        Contenu: <textarea name="contenu"></textarea><br/>
        <input type="submit" value="Enregistrer"/>
    </form>
    """

@app.route('/supprimer/<int:id>')
def supprimer(id_article):
    db.supprimer_article(id_article)
    return redirect(url_for('accueil'))

app.run(debug="on")