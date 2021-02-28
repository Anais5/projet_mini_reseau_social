from flask import url_for, request, redirect
from outils.gestion_articles import recuperer_articles, inserer_article, supprimer_article
from __main__ import app

@app.route('/', methods=["GET", "POST"])
def accueil():
    articles = [
        f"""
        <article>
            <h3 style="margin-bottom: 0">{titre}</h3>
            <p style="margin-top: 0; font-size: 80%">
            crée le {cree_le} par <em>{login}</em>
            </p>
            <p style="padding-left: 20px">{contenu}</p>
            <a href="{{ url_for('supprimer', id=id_article) }}">supprimer cet article</a>
            <hr/>
            </article>
        """
        for _, login, cree_le, titre, contenu in recuperer_articles()
    ]
    return f"""
    <nav><a href="{url_for('ajouter')}">Nouvel article</a></nav>
    """ + "\n".join(articles)

@app.route('/ajouter', methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        titre = request.form["titre"]
        contenu = request.form["contenu"]
        if titre and contenu:
            inserer_article(1, titre, contenu)
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
    supprimer_article(id_article)
    return redirect(url_for('accueil'))

