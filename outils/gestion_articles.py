import sqlite3 as db

def recuperer_articles():  # renvoie une liste de tuples
    # de la forme (login, cree_le, titre, contenu)
    data_base = db.connect("mini_blog.db")
    with data_base as c:
        curs = c.execute(
            """SELECT articles.id AS id_article, login, cree_le, titre, contenu
                FROM membres JOIN articles
                ON membres.id = articles.auteur_id
                ORDER BY articles.cree_le DESC
            """
        )
        return curs.fetchall()

def inserer_article(auteur_id, titre, contenu):
    with db.connect("C:\\Users\\anais\\Downloads\\mini_blog.db") as c:
        curs = c.execute(
            """INSERT INTO articles (auteur_id, titre, contenu)
                VALUES (?, ?, ?)""",
            (auteur_id, titre, contenu)
        )
        c.commit()  # ne pas oublier de «valider» lorsqu'une table est modifiée.

def supprimer_article(id_article):
    with db.connect("C:\\Users\\UserPC\\Desktop\\projet web\\mini_blog.db") as c:
        curs = c.execute(
            """DELETE FROM articles WHERE id = ?""",
            (id_article,)
        )
        c.commit()