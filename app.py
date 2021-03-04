from flask import Flask, url_for, request, redirect, render_template, session
from outils.data_base import DataBase
from outils.fonctions import liste_tags
from outils.settings import DB_DIR, HOST_IP

app = Flask(__name__, template_folder='templates')
app.secret_key = "dev"
db = DataBase(DB_DIR)

#page d'accueil
@app.route('/', methods=["GET", "POST"])
def accueil():
    return render_template('accueil.html', articles=db.recuperer_articles())

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["username"]
        mdp = request.form["password"]
        membre = db.recuperer_compte(login, mdp)
        verif = db.verif_pseudo(login)
        if verif is None:
            error = 'Identifiant incorrect.'
            return render_template('login.html', error=error)
        if membre is None:
            error = "Mot de passe incorrect."
            return render_template('login.html', error=error)
        # membre = None ou est un 2-tuple de la forme (id, mdp)
        if membre and membre[1] == mdp: # mieux: check_password_hash(membre[1], mdp)
            session.clear()
            # enregistrons quelques informations utiles dans l'objet session.
            session['mbrid'] = membre[0]
            session['login'] = login
            return redirect(url_for('accueil'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('accueil'))

@app.route('/inscription', methods=["GET", "POST"])
def inscrire():
    if request.method == "POST":
        login = request.form["username"]
        mdp = request.form["password"]
        membre = db.recuperer_compte(login, mdp)
        verif = db.verif_pseudo(login)
        if membre is not None:
            error = 'Vous êtes déjà inscrit.'
            return render_template('inscription.html', error=error)
        if verif is not None:
            error = 'Identifiant déjà pris.'
            return render_template('inscription.html', error=error)
        db.ajouter_membre(login, mdp)
        membre = (login, mdp)
        # commencer la session
        session.clear()
        # enregistrons quelques informations utiles dans l'objet session.
        session['mbrid'] = membre[0]
        session['login'] = login
        return redirect(url_for('accueil'))
    return render_template('inscription.html')

@app.route('/ajouter', methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        titre = request.form["titre"]
        contenu = request.form["contenu"]
        tags = liste_tags(request.form["tags"])
        auteur_id = db.get_membre_id(session['login'])
        if titre and contenu:
            db.inserer_article(auteur_id, titre, contenu)
            if tags:
                id = db.recuperer_id(auteur_id, titre, contenu)
                for tag in tags:
                    db.inserer_tag(id, tag)
            return redirect(url_for('accueil'))

    return """
    <form method="post">
        Titre*: <input name="titre"/><br/>
        Contenu*: <textarea name="contenu"></textarea><br/>
        Tags (séparés par des virgules): <input name="tags"/><br/>
        <input type="submit" value="Enregistrer"/>
    </form>
    """

@app.route('/supprimer/<int:id>')
def supprimer(id):
    db.supprimer_article(id)
    return redirect(url_for('accueil'))

# la suite sert juste de «bouche trou»

@app.route('/editer')
def editer():
    return redirect(url_for('accueil'))

app.run(host=HOST_IP)