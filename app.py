from flask import Flask, url_for, request, redirect, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from outils.data_base import DataBase
from outils.fonctions import liste_tags, page_recherche_tags, separer_tags
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
        membre = db.recuperer_compte(login)
        id = db.get_membre_id(login)
        verif = db.verif_pseudo(login)
        if verif is None:
            error = 'Identifiant incorrect.'
            return render_template('login.html', error=error)
        if check_password_hash(membre[0][1], mdp) == False:
            error = "Mot de passe incorrect."
            return render_template('login.html', error=error)
        # membre = None ou est un 2-tuple de la forme (id, mdp)
        if check_password_hash(membre[0][1], mdp): # mieux: check_password_hash(membre[1], mdp)
            session.clear()
            # enregistrons quelques informations utiles dans l'objet session.
            membre = (id, login, mdp)
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
        membre = db.recuperer_mdp(login) 
        verif = db.verif_pseudo(login)
        id = db.get_membre_id(login)
        if membre is not None:
            error = 'Vous êtes déjà inscrit.'
            return render_template('inscription.html', error=error)
        if verif is not None:
            error = 'Identifiant déjà pris.'
            return render_template('inscription.html', error=error)
        hashed_value = generate_password_hash(mdp, method='pbkdf2:sha256')
        db.ajouter_membre(login, hashed_value)
        membre = (id, login, mdp)
        # commencer la session
        session.clear()
        # enregistrons quelques informations utiles dans l'objet session.
        session['mbrid'] = membre[0]
        session['login'] = login
        return redirect(url_for('accueil'))
    return render_template('inscription.html')


@app.route('/supprimer_compte', methods=["GET", "POST"])
def suppr_compte():
    auteur_id = db.get_membre_id(session['login'])
    db.supprimer_compte(auteur_id ,session['login'])
    logout()
    return redirect(url_for('accueil'))


@app.route('/ajouter', methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        titre = request.form["titre"]
        contenu = request.form["contenu"]
        tags = liste_tags(request.form["tags"])
        auteur_id = db.get_membre_id(session['login'])
        if not titre:
            error = "Veuillez remplir tous les champs marqué d'une étoile !"
            return render_template('ajout.html', error=error)
        if not contenu:
            error = "Veuillez remplir tous les champs marqué d'une étoile !"
            return render_template('ajout.html', error=error)
        if titre and contenu:
            db.inserer_article(auteur_id, titre, contenu)
            if tags:
                id = db.recuperer_id(auteur_id, titre, contenu)
                for tag in tags:
                    db.inserer_tag(id, tag)
            return redirect(url_for('accueil'))
    return render_template('ajout.html')

@app.route('/page_perso', methods=["GET", "POST"])
def page_perso():
    login = session['login']
    id = db.get_membre_id(login)
    return render_template('page_perso.html', user=login, mesarticles=db.recuperer_articles_membre(id))


@app.route('/supprimer/<int:id>')
def supprimer(id):
    db.supprimer_article(id)
    return redirect(url_for('accueil'))


@app.route('/recherche_membre', methods=["GET", "POST"])
def recherche_membre():
    if request.method == "POST":
        user = request.form["username"]
        id = db.get_membre_id(user)
        if id:
            return render_template('profil.html', articles=db.recuperer_articles_membre(id), user=user)
        else:
            error = f"Il n'y a pas de membre portant le pseudo {user} !"
            return render_template('profil.html', error=error)
    return render_template('profil.html')


@app.route('/recherche', methods=["GET", "POST"])
def recherche_tags():
    tags_existants = db.rechercher_tags()
    if request.method == "POST":
        recherche = []
        tag_chercher = request.form.getlist('tag')
        lt = []
        ltt = []
        print(tag_chercher)
        print(len(tag_chercher)) # test à effacer plus tard
        if len(tag_chercher) == 1:
            for tags in tag_chercher:
                lt.extend(tags.strip().split('/'))
                lt.remove('')
            listedarticles = db.recuperer_article_par_tag(lt[0])
            print(listedarticles)
            print(lt)
        else:
            listedarticles = []
            for tags in tag_chercher:
                lt.extend(tags.strip().split('/'))
                lt.remove('')
                ltt.extend(tags.strip().split('/'))
                ltt.remove('')
                for i in lt:
                    print(i)
                    print(lt)
                    listedarticles.extend(db.recuperer_article_par_tag(i))
                    print(listedarticles)
                    lt.pop(0)
                    print(i)
                    print(lt)
            print(lt)
            print(listedarticles) # test à effacer plus tard
            print(ltt)
            ltt = [', '.join(ltt)]
            print(ltt[0])
        for tag in tags_existants:
            t = None
            if t == None:
                recherche.append(tag)
        if tag_chercher == []:
            error = "Il n'y a aucuns tags selectionnés !"
            return render_template('resultat_tag.html', error=error)
        tags = "&".join(recherche)
        liste_tags = separer_tags(tags)
        liste_id = []
        liste_articles = []
        for tag in liste_tags:
            articles_id = db.recuperer_id_article(tag)
            for i in articles_id:
                i = i[0]
                liste_id.append(i)
        for id in liste_id:
            a = db.recuperer_article_par_id(id)
            liste_articles.append(a)
        if len(tag_chercher) == 1:
            return render_template('resultat_tag.html', articles=listedarticles, tags=lt[0])
        else:
            return render_template('resultat_tag.html', articles=listedarticles, tags=ltt[0])
    return page_recherche_tags(tags_existants)


app.run(host=HOST_IP, debug=True)