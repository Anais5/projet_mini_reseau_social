from flask import Flask, url_for, request, redirect, render_template, session
from outils.data_base import DataBase
from outils.settings import DATABASE, DB_NAME

app = Flask(__name__, template_folder='templates')
db = DataBase(DB_NAME, DATABASE)

#page d'accueil
@app.route('/', methods=["GET", "POST"])
def accueil():
    return render_template('accueil.html', articles=db.recuperer_articles())

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        mdp = request.form["mdp"]
        membre = db.recuperer_compte(login, mdp)
        # membre = None ou est un 2-tuple de la forme (id, mdp)
        if membre and membre[1] == mdp: # mieux: check_password_hash(membre[1], mdp)
            session.clear()
            # enregistrons quelques informations utiles dans l'objet session.
            session['mbrid'] = membre[0]
            session['login'] = login
            return redirect(url_for('accueil'))
    # si "GET" ou si l'utilisateur n'est pas reconnue
    return render_template(
        'login.html'
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('accueil'))

@app.route('/inscription', methods=["GET", "POST"])
def inscrire():
    if request.method == "GET":
        login = request.form["login"]
        mdp = request.form["mdp"]
        membre = db.recuperer_compte(login, mdp)
        # membre = None ou est un 2-tuple de la forme (id, mdp)
        if membre and membre[1] == mdp: # mieux: check_password_hash(membre[1], mdp)
            session.clear()
            # enregistrons quelques informations utiles dans l'objet session.
            session['mbrid'] = membre[0]
            session['login'] = login
            return redirect(url_for('accueil'))
    return render_template('inscription.html')

@app.route('/messages')
def inscription():
    return render_template('messagerie.html', articles=db.recuperer_articles())

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

# la suite sert juste de «bouche trou»


@app.route('/editer')
def editer():
    return redirect(url_for('accueil'))

app.run(debug="on")